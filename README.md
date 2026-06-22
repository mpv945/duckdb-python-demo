conda create -n duckdb-python-demo python=3.14 -y
conda activate duckdb-python-demo 【退出 conda deactivate】
conda install -c conda-forge duckdb 
pandas pyarrow numpy Polars 数据分析核心库
scipy statsmodels 统计分析
matplotlib plotly pyecharts 图表库
openpyxl xlsxwriter  [ Excel报表,xlsxwriter生成复杂报表更强。]
reportlab  PDF报表
streamlit dash [BI报表/Dashboard【dash】]
requests HTTP 请求爬虫（最常见）登录态处理: session = requests.Session()  session.post(login_url)  session.get(data_url)
beautifulsoup4 lxml   HTML 解析
Playwright playwright-stealth Selenium 【UI页面自动化】


如果你需要在 **Windows、macOS、Linux** 上统一管理 Python 环境，推荐直接使用 **Miniconda**（轻量）或者 **Anaconda**（自带大量科学计算库）。

## 一、安装 Conda

### 方案1：Miniconda（推荐）

体积小，只安装 Conda 和 Python。

官方下载：

[Miniconda 官方下载页](https://docs.conda.io/en/latest/miniconda.html?utm_source=chatgpt.com)

### Windows

下载：

* Miniconda3 Windows x86_64 Installer

安装时建议：

```text
✓ Just Me
✓ Register Miniconda as default Python
✓ Add shortcut
✗ Add Miniconda to PATH
```

安装完成后打开：

```cmd
Anaconda Prompt
```

验证：

```bash
conda --version
```

---

### macOS

Intel：

```bash
bash Miniconda3-latest-MacOSX-x86_64.sh
```

Apple Silicon(M1/M2/M3)：

```bash
bash Miniconda3-latest-MacOSX-arm64.sh
```

安装完成：

```bash
source ~/.bashrc
# 或
source ~/.zshrc
```

验证：

```bash
conda --version
```

---

### Linux

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

bash Miniconda3-latest-Linux-x86_64.sh
```

重新加载：

```bash
source ~/.bashrc
```

验证：

```bash
conda --version
```

---

## 二、初始化 Shell

安装后执行：

```bash
conda init
```

或者指定：

```bash
conda init bash
conda init zsh
conda init powershell
```

重新打开终端即可。

---

# 三、为不同项目创建独立环境

这是 Conda 最重要的用途。

例如：

```text
project-a
  Python 3.10

project-b
  Python 3.12

project-c
  Python 3.9
```

完全互不影响。

---

## 创建环境

### Python 3.10

```bash
conda create -n project-a python=3.10
```

### Python 3.12

```bash
conda create -n project-b python=3.12
```

### Python 3.9

```bash
conda create -n project-c python=3.9
```

---

## 查看环境

```bash
conda env list
```

示例：

```text
base
project-a
project-b
project-c
```

---

## 进入环境

```bash
conda activate project-a
```

提示符变为：

```text
(project-a) $
```

---

## 退出环境

```bash
conda deactivate
```

---

# 四、安装项目依赖

进入环境：

```bash
conda activate project-a
```

安装：

```bash
pip install django
```

或者：

```bash
conda install numpy
```

查看：

```bash
pip list
```

---

# 五、项目目录绑定环境（推荐）

例如：

```text
workspace/
├── project-a
├── project-b
└── project-c
```

创建对应环境：

```bash
conda create -n project-a python=3.10
conda create -n project-b python=3.12
```

进入项目：

```bash
cd project-a

conda activate project-a
```

这样项目与环境名称保持一致。

---

# 六、把环境放到项目目录（强烈推荐团队协作）

默认环境在：

```text
Windows
C:\Users\用户名\miniconda3\envs

Linux
~/miniconda3/envs

Mac
~/miniconda3/envs
```

也可以直接创建到项目目录：

```bash
conda create --prefix ./venv python=3.12
```

目录：

```text
project-a/
├── src
├── requirements.txt
└── venv
```

激活：

Linux/macOS：

```bash
conda activate ./venv
```

Windows：

```cmd
conda activate .\venv
```

优点：

* 项目自包含
* 删除项目即可删除环境
* CI/CD方便
* Docker方便

---

# 七、导出环境

项目开发完成：

```bash
conda env export > environment.yml
```

生成：

```yaml
name: project-a
channels:
  - defaults

dependencies:
  - python=3.10
  - numpy
  - pandas
```

---

# 八、导入环境

团队成员：

```bash
conda env create -f environment.yml
```

或者：

```bash
conda env update -f environment.yml
```

---

# 九、VS Code 自动切换 Conda 环境

安装：

[VS Code 官方网站](https://code.visualstudio.com?utm_source=chatgpt.com)

安装 Python 插件：

[Python Extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python&utm_source=chatgpt.com)

打开项目：

```text
Ctrl + Shift + P

Python: Select Interpreter
```

选择：

```text
project-a
project-b
```

即可。

---

# 十、生产环境最佳实践

对于多个项目，推荐结构：

```text
/workspace
├── ai-platform
│   ├── environment.yml
│   └── source
│
├── live-stream
│   ├── environment.yml
│   └── source
│
└── vod-system
    ├── environment.yml
    └── source
```

创建：

```bash
conda env create -f environment.yml
```

激活：

```bash
conda activate ai-platform
```

导出：

```bash
conda env export --from-history > environment.yml
```

这里的 `--from-history` 很重要，它只记录你主动安装的包，不会把系统依赖全部导出，生成的环境文件更干净，更适合团队协作和跨平台部署。

对于企业开发、Docker、CI/CD 场景，通常推荐：

```text
项目目录
    ↓
environment.yml
    ↓
conda env create
    ↓
VS Code/PyCharm
```

而不是手工逐个安装依赖。这样 Windows、macOS、Linux 三个平台都能保持一致的开发环境。


如果你已经使用 Conda 管理环境，那么推荐：

```text
Conda 管理 Python 环境
        ↓
uv 管理依赖安装
        ↓
国内镜像加速
```

目前（2026年）`uv` 的安装速度通常比 `pip` 快 10~100 倍。

---

# 一、pip 加速

## 临时使用镜像

### 清华源

```bash
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 阿里云

```bash
pip install requests -i https://mirrors.aliyun.com/pypi/simple/
```

### 腾讯云

```bash
pip install requests -i https://mirrors.cloud.tencent.com/pypi/simple/
```

---

## 全局配置

### Linux/macOS

创建：

```bash
mkdir -p ~/.pip

cat > ~/.pip/pip.conf <<EOF
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
timeout = 60
EOF
```

验证：

```bash
pip config list
```

---

### Windows

创建文件：

```text
%APPDATA%\pip\pip.ini
```

内容：

```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
timeout = 60
```

查看：

```powershell
pip config list
```

---

# 二、安装 uv

`uv` 是由 [Astral 官方网站](https://astral.sh?utm_source=chatgpt.com) 开发的 Rust 版 Python 包管理工具。

官方文档：

[uv 官方文档](https://docs.astral.sh/uv/?utm_source=chatgpt.com)

---

## Linux/macOS

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

验证：

```bash
uv --version
```

---

## Windows

PowerShell：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

验证：

```powershell
uv --version
```

---

# 三、uv 与 Conda 配合

例如：

```bash
conda create -n ai python=3.12
conda activate ai
```

安装依赖：

```bash
uv pip install fastapi
```

注意：

```text
uv 不替代 conda 环境
uv 替代 pip 安装
```

推荐：

```text
Conda
  └─ 环境管理

uv
  └─ 包安装
```

---

# 四、配置 uv 国内镜像

## 临时

```bash
uv pip install requests \
  --index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 全局配置

Linux/macOS：

```bash
mkdir -p ~/.config/uv
```

```toml
# ~/.config/uv/uv.toml

index-url = "https://pypi.tuna.tsinghua.edu.cn/simple"
```

Windows：

```text
%APPDATA%\uv\uv.toml
```

```toml
index-url = "https://pypi.tuna.tsinghua.edu.cn/simple"
```

---

## 环境变量方式

Linux/macOS：

```bash
export UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
```

Windows：

```powershell
setx UV_INDEX_URL "https://pypi.tuna.tsinghua.edu.cn/simple"
```

查看：

```bash
uv config list
```

---

# 五、uv 创建项目

类似 Node.js 的 npm。

创建：

```bash
uv init myproject

cd myproject
```

生成：

```text
myproject
├── pyproject.toml
├── README.md
└── src
```

---

## 安装依赖

```bash
uv add fastapi
```

自动更新：

```toml
dependencies = [
    "fastapi"
]
```

---

## 开发依赖

```bash
uv add --dev pytest
```

---

## 删除依赖

```bash
uv remove fastapi
```

---

# 六、uv 锁定版本

生成锁文件：

```bash
uv lock
```

产生：

```text
uv.lock
```

类似：

```text
package-lock.json
pnpm-lock.yaml
Cargo.lock
```

---

安装：

```bash
uv sync
```

自动按照锁文件恢复环境。

---

# 七、最快的企业级方案

推荐目录结构：

```text
project/
├── pyproject.toml
├── uv.lock
├── .venv
└── src/
```

创建：

```bash
uv init
```

创建虚拟环境：

```bash
uv venv
```

激活：

Linux/macOS

```bash
source .venv/bin/activate
```

Windows

```cmd
.venv\Scripts\activate
```

安装：

```bash
uv add fastapi sqlalchemy redis
```

同步：

```bash
uv sync
```

---

# 八、uv 比 pip 快的原因

pip 安装过程：

```text
解析依赖
 ↓
下载包
 ↓
下载依赖
 ↓
安装
```

单线程、反复解析。

uv：

```text
Rust实现
 ↓
并发下载
 ↓
全局缓存
 ↓
并发解析
 ↓
硬链接复用
```

因此：

```text
pip install torch
    1~5分钟

uv pip install torch
    10~30秒
```

（具体取决于网络和镜像源）

---

# 九、推荐的现代 Python 开发方式

新项目推荐直接使用 uv，不一定需要 Conda：

```bash
# 创建项目
uv init live-stream

cd live-stream

# 创建虚拟环境
uv venv

# 安装依赖
uv add fastapi uvicorn redis sqlalchemy

# 安装开发工具
uv add --dev pytest black ruff mypy

# 生成锁文件
uv lock

# 恢复环境
uv sync
```

对于你的直播/VOD后台项目（FastAPI、Redis、MySQL、MinIO、FFmpeg等），推荐：

```text
uv
 + pyproject.toml
 + uv.lock
 + .venv
```


uv --version
配置 uv 国内镜像加速：
在 Windows 系统变量中添加以下环境变量，以便在下载 Python 核心和第三方依赖包时加速：
变量名：UV_PIP_INDEX_URL  变量值：https://tsinghua.edu.cn
变量名：UV_PYTHON_INSTALL_MIRROR（用于加速下载 Python 版本）变量值：https://huaweicloud.com
$env:UV_PIP_INDEX_URL = "https://tsinghua.edu.cn"
$env:UV_PYTHON_INSTALL_MIRROR = "https://huaweicloud.com"
读取变量：$env:变量名
 删除变量：Remove-Item Env:\变量名
查看本地和网络上可用的 Python 版本：
为当前用户设置：[System.Environment]::SetEnvironmentVariable("变量名", "变量值", "User")
为所有用户（系统级，需管理员权限）设置：[System.Environment]::SetEnvironmentVariable("变量名", "变量值", "Machine")
永久删除变量：将“变量值”设置为空字符串即可: [System.Environment]::SetEnvironmentVariable("变量名", "", "User")
由于 macOS 和 Linux 环境的系统变量配置在 Shell 配置文件中，建议直接将国内镜像源写入你的 ~/.zshrc 或 ~/.bashrc 中。
   1. 打开配置文件（以 zsh 为例，如果是 Linux 且用 bash 请将 zshrc 替换为 bashrc）：
   nano ~/.zshrc
   2. 在文件末尾添加以下两行（使用清华大学和华为云镜像）：
   # uv 依赖包下载加速
   export UV_PIP_INDEX_URL="https://tsinghua.edu.cn"# uv 下载 Python 核心版本加速
   export UV_PYTHON_INSTALL_MIRROR="https://huaweicloud.com"
   3. 保存并退出（在 nano 中按 Ctrl + O 确认保存，再按 Ctrl + X 退出），然后刷新配置：
   source ~/.zshrc
   
只有在需要大量科学计算库（如 TensorFlow、PyTorch、CUDA、OpenCV 编译版）时，再考虑使用 Conda 管理底层环境，依赖安装仍优先使用 `uv`。


先安装轻量Miniconda 【https://www.anaconda.com/docs/getting-started/miniconda/main】
https://www.anaconda.com/download/success 【选择 Miniconda】大小94mb
Windows下载：访问 Miniconda 官网 下载 Windows 64-bit 安装包。安装：双击运行，勾选 "Add Miniconda3 to my PATH environment variable"（或安装后通过快捷方式打开 "Anaconda Prompt"）。

1. 打开终端测试窗口Windows：点击键盘 Win 键，在搜索栏输入 Anaconda Prompt 或 Miniconda Prompt 并打开。
macOS / Linux：直接打开系统自带的 Terminal（终端）。
2. 依次运行以下三条基础命令
① 检查 Conda 版本： conda --version
② 检查当前环境列表：conda env list
③ 尝试创建一个测试环境（终极验证）：conda create -n test_install python=3.10 -y
清理测试环境（验证完后可以删掉）：conda env remove -n test_install -y

在终端或 Anaconda Prompt 中执行以下命令：
# 添加官方核心基础包镜像
conda config --add channels https://tsinghua.edu.cn
# 添加最常用的第三方开源包镜像（很多数据分析工具都在这里）
conda config --add channels https://tsinghua.edu.cn
# 设置在下载时显示包的来源网址（方便确认是否成功走了解速通道）
conda config --set show_channel_urls yes
删除：conda config --remove channels https://tsinghua.edu.cn
验证：conda config --show-sources
如果安装软件报错
To accept these channels' Terms of Service, run the following commands:
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/msys2
1. 同意 Anaconda 服务条款（ToS）直接运行以下三条官方提示的命令，解除权限限制：【只要执行了第 1 步的 conda tos accept，这个阻断报错就会彻底消失。】
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/msys2

# 1. 恢复 Conda 的默认源设置（清除所有之前乱掉的自定义 channels）
conda config --remove-key channels 【# 移除错误的清华主页地址： conda config --remove channels https://tsinghua.edu.cn】
# 重新添加正确的国内镜像源（确保末尾带斜杠/）
                                      conda config --add channels https://tsinghua.edu.cn
                                      conda config --add channels https://aliyun.com
                                      conda config --add channels https://bfsu.edu.cn
                                     conda config --add channels https://sjtu.edu.cn
# 真确配置
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge
清理 Conda 缓存
conda clean --all -y
# 3. 再次确认当前的生效配置
conda config --show-sources
重新尝试安装 conda-pack
# 代理
proxy_servers:
  http: http://user:password@proxy.company.com:8080
  https: http://user:password@proxy.company.com:8080

conda config --set proxy_servers.http http://127.0.0.1:7890
conda config --set proxy_servers.https http://127.0.0.1:7890
conda install -c conda-forge conda-pack -y
更新： conda update -n base -c conda-forge conda
下载完删除：conda config --remove-key proxy_servers

## 2. 安装 uv
uv 是由 Astral 开发的极速 Python 包管理工具，支持跨平台一键安装：
## Windows (PowerShell)
powershell -c "irm https://astral.sh | iex"
## macOS & Linux
curl -LsSf https://astral.sh | sh
uv 会自动读取 pip 的全局配置。在终端执行以下命令设置全局 PyPI 镜像：
uv pip config set global.index-url https://tsinghua.edu.cn

https://duckdb.org/install/?platform=windows&environment=python
扩展：http://extensions.duckdb.org 【https://duckdb.org/docs/current/extensions/installing_extensions】
默认情况下，扩展程序安装在用户的主目录下：~/.duckdb/extensions/duckdb_version/platform_name/     【路径duckdb_version将等于该版本的版本标签。对于每日构建的 DuckDB 版本，该路径将等于构建的短 Git 哈希值。】
要更改 DuckDB 存储其扩展的默认位置，请使用以下extension_directory配置选项：SET extension_directory = '/path/to/your/extension/directory';
要指定多个用于加载扩展的目录（例如，用于包管理器或物理隔离环境），请使用以下extension_directories选项：SET extension_directories = ['/usr/lib/duckdb/extensions', '/opt/duckdb/extensions'];
请注意，设置配置选项的值home_directory不会影响扩展程序的位置。
从显式路径安装扩展程序：INSTALL 'path/to/httpfs.duckdb_extension'; 或者：LOAD 'path/to/httpfs.duckdb_extension';

一步一步创建 DuckDB 分析项目
https://duckdb.org/docs/current/clients/python/overview 【Python version: DuckDB requires Python 3.9 or newer.】
pip install duckdb 或者 conda install python-duckdb -c conda-forge
创建一个独立的 Python 环境（DuckDB 官方要求 Python 3.9+，此处推荐使用 3.10）：
创建干净环境并安装依赖 conda search python --full-name[查看远程版本】
conda create -n duckdb-python-demo python=3.14 -y
conda activate duckdb-python-demo 【退出 conda deactivate】
由于后续需要离线移植，我们必须在当前激活的 Conda 环境中安装 conda-pack 核心工具。同时使用 uv 快速安装 duckdb 及其常用的数据分析辅助库（如 pandas 和 pyarrow）：
# 安装离线打包工具
conda install -c conda-forge conda-pack -y
# 使用 uv 加速安装 DuckDB 及其数据栈
conda install -c conda-forge duckdb pandas pyarrow 优先 【conda-forge能安装，就不执行：uv pip install duckdb pandas pyarrow】
在项目目录中创建一个名为 analysis.py 的脚本。该脚本将创建一个持久化数据库，并演示如何加载内存数据及导出分析结果：
import duckdb
import pandas as pd

def main():
    print("--- 正在初始化 DuckDB 持久化数据库 ---")
    # 1. 创建或连接到本地持久化数据库文件
    con = duckdb.connect("offline_analytics.db") #
    
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
    analysis_df.to_csv("summary_report.csv", index=False)
    print("\n[成功] 报告已导出至 'summary_report.csv'")
    
    # 6. 关闭数据库连接
    con.close() #

if __name__ == "__main__":
    main()

测试：python "D:\run_duckdb.py"
切换目录后再运行（最清晰）假设你按之前建议把环境解压到 C:\myproject_env，项目代码在 D:\myproject_package：
cd /d "D:\myproject_package"
"C:\myproject_env\python.exe" run_duckdb.py

第四步：打包环境并移植到内网离线服务器
conda-pack 可以将整个 Python 环境连同二进制依赖完整打成压缩包。注意：外网打包机的操作系统和 CPU 架构必须与内网目标服务器完全一致（例如：均未 Linux x86_64）。
1. 在外网电脑上打包环境在激活的目标环境终端下，执行打包命令：
# 将名为 duckdb_env 的环境打包为 duckdb_env.tar.gz
进去先安装
conda activate duckdb-python-demo
pip list   # 或 conda list,确认 duckdb 等依赖都在里面
然后退出虚拟环境
conda deactivate
确认没问题后再回到 base 执行打包命令
确认你在 base 环境下安装。一定要先确认提示符是 (base),再执行安装:
conda activate base
conda install -c conda-forge conda-pack（前面安装了可以跳过）
测试：conda-pack --help
开始打包：conda-pack -n duckdb-python-demo -o duckdb-python-demo.tar.gz
2. 将文件传输至内网使用 U 盘、光盘或安全网闸，将以下文件复制到内网离线服务器：
duckdb_env.tar.gz（环境压缩包）
analysis.py（分析脚本）
3. 在内网服务器上解压与恢复环境在内网服务器的目标目录下，执行以下命令：
# 创建目标环境目录
mkdir -p my_offline_env
# 解压环境到该目录
tar -xzf duckdb_env.tar.gz -C my_offline_env
# 激活该离线环境（无需内网安装 Conda）
source my_offline_env/bin/activate
4. 运行分析环境激活后，直接在内网运行您的 DuckDB 分析脚本：
python analysis.py




