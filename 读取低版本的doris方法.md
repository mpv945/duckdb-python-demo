
# 如果不想编写复杂的 SQL 语句，建议配合 SQLAlchemy 等 ORM（对象关系映射）库使用。它允许你直接用 Python 类来操作 MySQL 数据库，开发效率更高。


在 Python 中直接读取 MySQL 的几千万条数据时，如果一次性加载（如使用传统的 pd.read_sql），极易触发 OOM（内存溢出）。
最科学的生产级架构是：利用 MySQL 游标进行流式分批拉取（Streaming Fetch），结合 PyArrow 的 RecordBatch 或 Polars 的 LazyFrame 接入 DuckDB 进行极速的高效处理，最后流式写入本地 Parquet 文件。
下面为您提供两种最常用的生产级流式处理方案（推荐方案一）。
------------------------------
## 准备工作：安装依赖
我们需要使用 pymysql 或 mysql-connector-python 来建立支持流式查询的服务器端游标。

pip install duckdb polars pyarrow pymysql

------------------------------
## 方案一：MySQL 流式读取 + PyArrow + DuckDB（推荐：内存最稳健）
核心逻辑：使用 pymysql.cursors.SSCursor（服务器端游标）让 MySQL 逐行或逐批返回数据，Python 侧用 PyArrow 将每批数据打包成 RecordBatch 写入 Parquet。接着用 DuckDB 挂载这些 Parquet 直接进行高性能 SQL 分析。

import pymysqlimport pyarrow as paimport pyarrow.parquet as pqimport duckdb
# 1. 数据库连接配置db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'my_large_db',
    'charset': 'utf8mb4'
}
# 2. 定义 PyArrow 的 Schema（必须与 MySQL 返回的列名和类型对应，提升效率）# 假设处理的是订单表arrow_schema = pa.schema([
    ('order_id', pa.int64()),
    ('user_id', pa.int64()),
    ('amount', pa.float64()),
    ('create_time', pa.timestamp('ms'))
])
BATCH_SIZE = 100_000  # 每批处理 10 万条output_parquet = "mysql_large_data.parquet"
# 3. 开始流式拉取并写入 Parquet# 使用 SSCursor (Server-Side Cursor) 关键：数据留在 MySQL 内存中，Python 分批取conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.SSCursor)
try:
    with conn.cursor() as cursor:
        cursor.execute("SELECT order_id, user_id, amount, create_time FROM my_huge_table")
        
        # 开启 Parquet 流式写入器
        with pq.ParquetWriter(output_parquet, arrow_schema, compression='SNAPPY') as writer:
            while True:
                # 分批从网络流中获取数据
                rows = cursor.fetchmany(BATCH_SIZE)
                if not rows:
                    break
                
                # 将元组列表高效转换为 PyArrow RecordBatch
                # zip(*rows) 将 [(1, 2), (3, 4)] 转为 [(1, 3), (2, 4)] 列式结构
                columns = list(zip(*rows))
                batch = pa.RecordBatch.from_arrays(
                    [pa.array(col) for col in columns], 
                    schema=arrow_schema
                )
                
                # 流式写入磁盘，内存立刻释放
                writer.write_batch(batch)
                print(f"已成功流式落盘 {len(rows)} 条数据...")
finally:
    conn.close()
# 4. 使用 DuckDB 直接对落盘的 Parquet 进行极速 OLAP 分析
print("--- 开始使用 DuckDB 进行高性能分析 ---")con = duckdb.connect()
# DuckDB 零拷贝读取 Parquet，支持并行和谓词下推res = con.query(f"""
    SELECT 
        user_id, 
        SUM(amount) AS total_spend,
        COUNT(*) AS order_count
    FROM '{output_parquet}'
    GROUP BY user_id
    HAVING total_spend > 5000
    LIMIT 10""").pl()  # 直接转成 Polars DataFrame 打印或后续处理

print(res)

------------------------------
## 方案二：MySQL 分片 + Polars + DuckDB（适合有自增主键、并发处理）
核心逻辑：如果你的 MySQL 表有一个自增的递增主键（如 id），可以使用 Polars 的 read_sql 自带的分片（Partitioning）机制。Polars 会自动在后台并发/分批建立多个连接去拉取不同范围的 id，然后无缝对接 DuckDB。

import polars as plimport duckdb
# 1. 构建标准数据库连接 URI# 注意：Polars 底层使用 connectorx 或 adbc，速度极快connection_uri = "mysql://root:password@localhost:3306/my_large_db"
# 2. 使用 Polars 分片流式读取# 假设主键是 id，从 1 到 50,000,000，分成 50 个分片并发分批拉取# 这样可以完全避免一条大 SQL 锁死 MySQL 或是让 Python 内存撑爆
print("开始多线程分批读取 MySQL...")pl_lazy_df = pl.read_sql(
    query="SELECT id, user_id, amount FROM my_huge_table",
    connection_uri=connection_uri,
    partition_column="id",
    partition_num=50,      # 分成 50 批
    iter_batches=True      # 返回一个迭代器，实现真正意义上的流式分批
)
# 3. 配合 DuckDB 处理每个 Polars 分片con = duckdb.connect()
for i, batch_df in enumerate(pl_lazy_df):
    # batch_df 是一个当前批次的 Polars DataFrame
    print(f"正在处理第 {i+1} 个 Polars 数据批次，数据量: {len(batch_df)}")
    
    # 每次将当前批次注入 DuckDB 的临时表或进行增量聚合
    # 在 DuckDB 中直接引用变量名 'batch_df'
    con.execute("""
        CREATE OR REPLACE TEMP TABLE current_chunk AS SELECT * FROM batch_df;
    """)
    
    # 在这里执行你的分析或清洗逻辑，例如增量写入一个 DuckDB 永久表
    if i == 0:
        con.execute("CREATE TABLE final_summary AS SELECT user_id, SUM(amount) as sub_total FROM current_chunk GROUP BY user_id")
    else:
        con.execute("""
            INSERT INTO final_summary 
            SELECT user_id, SUM(amount) as sub_total FROM current_chunk GROUP BY user_id
        """)
# 4. 最终在 DuckDB 中做二次合并final_res = con.query("""
    SELECT user_id, SUM(sub_total) AS total_amount 
    FROM final_summary 
    GROUP BY user_id 
    ORDER BY total_amount DESC 
    LIMIT 5""").pl()

print("最终聚合分析结果：")
print(final_res)

------------------------------
## 生产环境闭坑总结

   1. MySQL 端的压力：方案一采用的 SSCursor 会在查询期间占用 MySQL 该连接的缓存，不要在拉取过程中写复杂的 Python 耗时业务逻辑，应该“快拉快写”（快速转成 PyArrow 写入本地 Parquet），把计算留给后面的 DuckDB。
   2. 网络带宽瓶颈：几千万条数据通过网络从 MySQL 传输到 Python 耗时主要在网络 I/O。建议将此 Python 脚本部署在与 MySQL 同一内网/局域网的服务器上运行。
   3. 数据类型映射：MySQL 的 DateTime 类型在转入 PyArrow 时，如果包含 0000-00-00 这种非法时间会报错。建议在 SQL 中使用 COALESCE 或转换成字符串先拉出来，再交给 DuckDB 清洗。

为了帮您选择最佳的具体配置，请问您的 MySQL 表是否有递增的自增主键（如 ID）？另外，这些数据读取出来后，最终是要做报表分析、还是写进另一个数据库/文件？


