import duckdb
import os

class DuckdbExtensionLoad:
    #func(bool(1))       # True
    # func(bool(0))       # False
    # func(bool("yes"))   # True，非空字符串都是 True
    # func(bool(""))      # False，空字符串是 False
    def __init__(self, is_memory: bool):
        # 初始化时传入的参数，存为类属性
        self.is_memory = is_memory
        self.amount = 0
    def process(self):
        # ==================== 配置 ====================
        # 修改为全小写，符合 PEP 8 局部变量规范
        #env_prefix = os.getenv("CONDA_PREFIX") or os.path.dirname(os.path.dirname(os.__file__))

        # 修改为全小写
        #extension_dir = os.path.join(env_prefix, "duckdb_extensions")

        # ==================== 初始化 ====================
        # 每次都从0开始
        amount = 1 if self.is_memory else -1
        print(f"金额: {amount}")
        # 全局变量，可以累计
        if self.is_memory:
            self.amount += 1
        else:
            self.amount -= 1
        print(f"金额: {self.amount}")

        print("当前工作目录:", os.getcwd())
        print("脚本所在目录:", os.path.dirname(os.path.abspath(__file__)))

        if self.is_memory:
            con = duckdb.connect(database=":memory:") #  # 或指定 .duckdb 文件路径(无法记住安装扩展）
        else:
            # data_dir = "/path/to/your/directory"
            # os.makedirs(data_dir, exist_ok=True)  # 确保目录存在
            # db_path = os.path.join(data_dir, "mydata.db")
            # con = duckdb.connect(database=db_path)
            db_path = os.path.join(os.getcwd(), "mydata.db")
            # con = duckdb.connect(database="mydata.duckdb") # 相对路径（当前工作目录下）
            con = duckdb.connect(database=db_path)

        # 设置扩展目录
        #con.execute(f"SET extension_directory = '{extension_dir}';")

        # 安装扩展
        #con.execute("INSTALL mysql;")
        #con.execute("INSTALL postgres;")
        #
        #print("扩展已安装到:", extension_dir)
        #con.close()
        #print(f"【支付服务提示】金额 {self.is_memory} 元处理中... 扩展已安装到: {extension_dir}")

        return con

# ==================== 扩展目录设置（打包后关键） ====================
def setup_extension_directory(con):
    """把扩展目录设置到 Conda 环境内部（推荐用于 conda-pack）"""
    # env_prefix = os.environ.get("CONDA_PREFIX")
    env_prefix = os.getcwd()
    # env_prefix = os.getenv("CONDA_PREFIX") or os.path.dirname(os.path.dirname(os.__file__))
    if env_prefix:
        extension_dir = os.path.join(env_prefix, "duckdb_extensions")
        os.makedirs(extension_dir, exist_ok=True)
        con.execute(f"SET extension_directory = '{extension_dir}';")
        print(f"✅ 扩展目录已设置为: {extension_dir}")
    else:
        print("⚠️ 未检测到 CONDA_PREFIX，使用默认扩展目录")

def install_or_load_extension(con, ext_name: str):
    try:

        # rows = con.execute("""
        #                    SELECT *
        #                    FROM duckdb_extensions()
        #                    """).fetchall()
        #
        # for row in rows:
        #     print(row)

        # result = con.execute(
        #     f"SELECT installed FROM duckdb_extensions() WHERE extension_name = '{ext_name}' ").fetchone()
        # is_installed = result is not None and result[0]
        # print(is_installed)

        # result = con.execute("""
        #                      SELECT installed
        #                      FROM duckdb_extensions()
        #                      WHERE extension_name = ?
        #                      """, [ext_name]).fetchone()
        #
        # if result is None:
        #     print("扩展不存在")
        # elif result[0]:
        #     print("已安装")
        # else:
        #     print("未安装")

        result = extension_installed(con, ext_name)

        if result and result[0] is True:
            print(f"✅ {ext_name} 已安装，直接加载")
            con.execute(f"LOAD {ext_name};")
        else:
            print(f"🔧 正在安装 {ext_name} ...")
            con.execute(f"INSTALL {ext_name};")
            con.execute(f"LOAD {ext_name};")
            print(f"✅ {ext_name} 安装完成")
    except Exception as e:
        print(f"❌ {ext_name} 处理失败: {e}")
        raise


def extension_installed(con, alias):
    row = con.execute("""
        SELECT installed
        FROM duckdb_extensions()
        WHERE list_contains(aliases, ?)
    """, [alias]).fetchone()

    #return row is not None and row[0]
    return row