import os

import pandas as pd

import pyarrow.fs as fs
import pyarrow.orc as orc

def process_data(con, output_path):
    print("--- 正在初始化 DuckDB 持久化数据库 ---")
    # 1. 创建或连接到本地持久化数据库文件
    # con = duckdb.connect("offline_analytics.db") #
    
    # 2. 准备一份测试数据（模拟 Pandas DataFrame 导入）
    df = pd.DataFrame({
        "user_id":[1,2,3],
        "sales": [250.5, 550.0, 120.0],
        "region": ["North", "South", "North"]
    })
    
    # 3. 将 Pandas DataFrame 注册并写入 DuckDB 本地表
    con.sql("CREATE TABLE IF NOT EXISTS sales_data AS SELECT * FROM df")
    
    # 4. 执行 SQL 聚合分析
    print("\n--- 执行 SQL 聚合分析结果 ---")
    result_rel = con.sql("""
        SELECT region, SUM(sales) AS total_sales, COUNT(user_id) AS user_count
        FROM sales_data
        GROUP BY region
    """)
    result_rel.show() #
    
    # 5. 将结果转换回 Pandas DataFrame 并导出为本地 CSV
    analysis_df = result_rel.df() #

    analysis_df.to_csv(os.path.join(output_path, "summary_report.csv"), index=False)
    print("\n[成功] 报告已导出至 'summary_report.csv'")

    # MySQL
    con.execute("""
    ATTACH '
    host=192.168.1.10
    port=3306
    user=root
    password=123456
    database=sales'
    AS mysql_db
    (TYPE mysql)
    """)

    # PostgreSQL
    con.execute("""
    ATTACH '
    host=192.168.1.20
    port=5432
    user=postgres
    password=123456
    dbname=dw'
    AS pg_db
    (TYPE postgres)
    """)

    # S3 以后： s3://warehouse/ 实际上就是：http://192.168.1.100:9000/warehouse/
    # 例如 AWS： MinIO 一般需要：URL_STYLE path 否则很多 MinIO 会报：NoSuchBucket
    # con.execute("""
    # CREATE SECRET (
    #     TYPE S3,
    #     KEY_ID 'AKIAxxxxxxxx',
    #     SECRET 'xxxxxxxx',
    #     REGION 'ap-southeast-1'
    # )
    # """)
    # con.execute("""
    # CREATE SECRET (
    # TYPE s3,
    # KEY_ID 'xxxx',
    # SECRET 'yyyy',
    # ENDPOINT '192.168.1.100:9000',
    # USE_SSL FALSE,
    # URL_STYLE 'path',
    # REGION 'ap-east-1'
    # )
    # """)
    # httpfs 是可自动加载的扩展,通常不用手动 INSTALL/LOAD
    con.execute("""
        CREATE OR REPLACE SECRET s3_secret (
            TYPE S3,
            KEY_ID '你的AccessKey',
            SECRET '你的SecretKey',
            ENDPOINT '你的s3地址:9000',   -- 比如 MinIO,不带 http(s):// 前缀
            URL_STYLE 'path',           -- 自建存储几乎都要这个
            USE_SSL false,              -- 如果是 http 而非 https
            REGION 'us-east-1'          -- 大部分自建存储不校验,填默认值即可
            SCOPE 's3://bucket-A'       -- 之后查询 s3://bucket-A/something 这样的路径时,s3_secret 会被自动选中用于该请求。 可以配置多个
            SCOPE ['s3://bucket-A', 's3://bucket-C/some-prefix'] 关联多个，不写 SCOPE 时的默认行为:不指定 scope 会用默认 scope,对 S3 来说就是 [s3://, s3n://, s3a://],也就是匹配所有 s3 路径。
        );
    """)
    # con.execute("INSTALL httpfs; LOAD httpfs;")
    # con.execute("SET s3_region='us-east-1';")
    # con.execute("SET s3_url_style='path';")
    # con.execute("SET s3_endpoint='你的s3地址:9000';")  # 注意不带 http://
    # con.execute("SET s3_access_key_id='你的AccessKey';")
    # con.execute("SET s3_secret_access_key='你的SecretKey';")
    # con.execute("SET s3_use_ssl=false;")  # 如果是 http
    # 直接查询parquet
    # df = con.execute("SELECT * FROM read_parquet('s3://your-bucket/path/to/data.parquet')").df()
    # print(df)

    # 写csv
    # 查询结果是一个 Relation,直接调用 write_csv
    # conn.sql("SELECT * FROM my_table").write_csv(
    #     "output.csv",
    #     sep="\t",
    #     header=True,
    #     quotechar='"',
    #     compression="gzip"
    # )
    # 方法二:COPY TO(SQL 风格,更灵活)
    con.execute("""
        COPY (SELECT * FROM read_parquet('data.parquet'))
        TO 'output.csv' (
        FORMAT CSV,
        HEADER true,           -- 是否写表头
        DELIMITER ',',         -- 分隔符,改成 '\t' 就是 TSV
        QUOTE '"',             -- 引号字符
        ESCAPE '"',            -- 转义字符
        NULL 'NULL',           -- NULL 值如何表示,默认是空字符串
        DATEFORMAT '%Y-%m-%d', -- 日期格式
        COMPRESSION 'gzip'     -- 可选: gzip / zstd,文件名建议加上 .gz 后缀
    )
    """)
    # 写到自建 S3 上(延续前面的配置)
    # con.execute("""
    #     COPY (SELECT * FROM my_table)
    #     TO 's3://your-bucket/output/result.csv' (FORMAT CSV, HEADER true)
    # """)
    # 大数据量分片导出 如果数据量大,想按目录分片输出多个 CSV(而不是一个巨大文件),可以用 PARTITION_BY 或 PER_THREAD_OUTPUT:
    # con.execute("""
    #     COPY (SELECT * FROM my_table)
    #     TO 's3://your-bucket/output/'
    #     (FORMAT CSV, HEADER true, PER_THREAD_OUTPUT true)
    # """)
    # 或者按某个字段分区(类似 Hive 分区目录结构):
    # con.execute("""
    #     COPY (SELECT * FROM my_table)
    #     TO 's3://your-bucket/output/'
    #     (FORMAT CSV, HEADER true, PARTITION_BY (year, month))
    # """)
    # 直接导出 DataFrame
    # import pandas as pd
    # df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    # con.sql("SELECT * FROM df").write_csv("output.csv")

    # 输出
    con.execute("""
    COPY (
    SELECT
        o.order_id,
        o.amount,
        c.name,
        p.city
    FROM mysql_db.orders o
    JOIN pg_db.customer c
    ON o.customer_id=c.id
    LEFT JOIN read_csv_auto('city.csv') p
    ON c.city_code=p.code
    )
    TO
    's3://warehouse/order_result'
    (
    FORMAT PARQUET,
    COMPRESSION ZSTD,
    PARTITION_BY(order_date)
    )
    """)

    # 读取 xlsx
    df = con.sql("""
                 SELECT *
                 FROM read_xlsx('employee.xlsx')
                 """).df()
    # SELECT *
    # FROM
    # read_xlsx(
    #     'employee.xlsx',
    #     sheet='Sheet1' 读取多个 Sheet
    #     range='A1:H100' 读取指定区域
    #     header = false 如果没有 Header：忽略 Header 默认：第一行 是列名
    #     types = { 指定列类型
    #         phone: 'VARCHAR',
    #         age: 'INTEGER'
    #
    #     }
    # );

    # 多sheet页读取
    # sheets = [
    #     "Sheet1",
    #     "Sheet2",
    #     "Sheet3"
    # ]
    # sql = "\nUNION ALL\n".join([
    #     f"""
    #     SELECT *,
    #            '{sheet}' AS sheet_name
    #     FROM read_xlsx(
    #         'sales.xlsx',
    #         sheet='{sheet}'
    #     )
    #     """
    #     for sheet in sheets
    # ])
    #df = con.sql(sql).df()
    # 旧版 xls : pip install xlrd [import xlrd]
    # book = xlrd.open_workbook("test.xls")
    # sheet = book.sheet_by_index(0)
    # data = []
    # for i in range(sheet.nrows):
    #     data.append(sheet.row_values(i))
    # df = pd.DataFrame(data[1:], columns=data[0])
    # con.register("xls_table", df)
    # con.sql("""
    #         SELECT *
    #         FROM xls_table
    #         """)

    # 写 xlsx [多个 Sheet] COPY ... → temp1.xlsx , COPY ... → temp2.xlsx  或者使用 openpyxl 合并多个 Sheet。
    # con.execute("""
    # COPY (
    # SELECT *
    # FROM orders
    # )
    # TO 'orders.xlsx'
    # WITH (
    # FORMAT xlsx
    # SHEET '订单' 可 指定 Sheet
    # )
    # """)

    # 读取 Iceberg(duckdb 只能读取）
    # 读取 Iceberg
    # df = con.sql("""
    #              SELECT *
    #              FROM iceberg_scan(
    #                      's3://warehouse/sales/metadata/v2.metadata.json'
    #                   )
    #              """).df()
    # 读取 Iceberg
    # con.sql("""
    #         SELECT customer_id,
    #                sum(amount)
    #         FROM iceberg_scan(
    #                 's3://warehouse/sales/metadata/v2.metadata.json'
    #              )
    #         WHERE order_date='2026-06-01'
    #         GROUP BY customer_id
    #         ORDER BY 2 DESC
    #         """)
    # 查看 Schema
    # DESCRIBE
    # SELECT *
    # FROM
    # iceberg_scan(
    #
    #     's3://warehouse/order/metadata/v2.metadata.json'
    #
    # );
    # 查看 Snapshot
    # SELECT *
    # FROM
    # iceberg_metadata(
    #     's3://warehouse/order/metadata/v2.metadata.json'
    #
    # );
    # 读取指定 Snapshot
    # SELECT *
    # FROM
    # iceberg_scan(
    #     's3://warehouse/order/metadata/v2.metadata.json',
    #     snapshot_id=912381273981273
    # );

    # ORC文件
    # 1. 配置自建 S3 兼容存储连接
    s3 = fs.S3FileSystem(
        access_key="你的AccessKey",
        secret_key="你的SecretKey",
        endpoint_override="http://你的s3地址:9000",  # 比如 MinIO 默认 9000
        scheme="http",  # 如果是 https 就改成 "https"
        # 大部分自建存储(MinIO/Ceph)用 path-style,不用改 force_virtual_addressing
    )
    # 2. 直接用文件系统对象打开远端 ORC 文件读取(不落地到本地磁盘)
    with s3.open_input_file("your-bucket/path/to/data.orc") as f:
        table = orc.ORCFile(f).read()
    # 3. 注册进 DuckDB 查询
    # conn = duckdb.connect()
    con.register("orc_view", table)
    print(con.execute("SELECT * FROM orc_view LIMIT 10").df())

    # 6. 关闭数据库连接
    # con.close() #
