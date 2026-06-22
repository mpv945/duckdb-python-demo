import os

import pandas as pd

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
    
    # 6. 关闭数据库连接
    # con.close() #

if __name__ == "__main__":
    main()
