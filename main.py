# 1. 从 目录名.文件名 中 导入 类名
import os
import argparse

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

def get_param(cli_value, env_key, default=None):
    """优先级: 命令行参数 > 环境变量 > 默认值"""
    if cli_value is not None:
        return cli_value
    return os.environ.get(env_key, default)

def main():
    print("--- 系统启动 ---")

    # 获取系统设置环境变量
    # 1. 命令行参数优先 python xx.py --db-host=192.168.1.1
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--db-host", default=None, help="数据库地址")
    # args = parser.parse_args()
    # # 2. 没传命令行参数,走环境变量  export DB_HOST=10.0.0.1 然后 python xx.py ，命令行和环境变量都没有,走默认值
    # db_host = get_param(args.db_host, "DB_HOST", "localhost")
    # print(f"使用配置: host={db_host}")

    # 进阶:用 argparse 直接对接环境变量(去掉手写的 get_param) argparse 本身支持把环境变量设成 default,这样可以省掉中间那层判断:
    parser = argparse.ArgumentParser()
    # parser.add_argument("--port", type=int)  # "5432" → 5432
    # parser.add_argument("--rate", type=float)  # "0.5"  → 0.5
    # parser.add_argument("--name", type=str)  # 默认就是 str,可以不写
    # parser.add_argument("--path", type=open)  # 直接打开文件,返回文件对象(不常用,容易资源泄露)
    parser.add_argument(
        "--output-data-dir",
        type=str,
        default=os.environ.get("OUTPUT_DATA_PATH", OUTPUT_DIR),  # 命令行没传时,直接退到环境变量再到默认值
    )
    # add_argument("--db-host", dest="host")  直接 args.host
    # argparse 里 --output-data-dir 这种长选项,命名里的 -(连字符)会自动转换成 _(下划线),变成属性名 args.output_data_dir。 位置参数(不带 -/--前缀的参数)直接用参数名本身作为属性名,不需要转换:
    args = parser.parse_args()
    print(f"获取到数据输出目录 : {args.output_data_dir} ")


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