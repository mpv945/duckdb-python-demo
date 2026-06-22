# 1. 从 目录名.文件名 中 导入 类名
import os

from biz_modules.data_processing.install_extension import DuckdbExtensionLoad
# 从文件名中 直接 导入方法 （定义在文件下的，非类名下的函数引用）
from biz_modules.data_processing.install_extension import (
    setup_extension_directory,
    install_or_load_extension
)

from biz_modules.data_processing.run_duckdb import process_data


EXT_MAP = {
    "mysql": "mysql_scanner",
    "postgres": "postgres_scanner",
}


OUTPUT_DIR = os.path.join(os.getcwd(), "output","data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    print("--- 系统启动 ---")

    # 2. 实例化类（调用 __init__ 方法，传入金额 199.0）
    # 此时 service 就是一个创建好的“支付宝服务对象”  变量符合小写规则才不会警告
    # duckdb_extension_load = DuckdbExtensionLoad(True) # True/False
    # duckdb_extension_load = DuckdbExtensionLoad(is_memory=False)
    duckdb_extension_load = DuckdbExtensionLoad(is_memory=True)
    # 3. 通过对象调用里面的方法
    con = duckdb_extension_load.process()
    try:
        setup_extension_directory(con)
        ext = EXT_MAP.get("mysql", "mysql")
        print("扩展名称映射：{}".format(ext))
        install_or_load_extension(con, "mysql")
        install_or_load_extension(con, "postgres")

        install_or_load_extension(con, "excel")
        install_or_load_extension(con, "fts")
        install_or_load_extension(con, "httpfs")
        install_or_load_extension(con, "iceberg") # 更新扩展 UPDATE EXTENSIONS;

        # 处理数据
        process_data(con,OUTPUT_DIR)

    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        con.close()


if __name__ == "__main__":
    main()