# 运行环境 / Environment

[中文](#中文) · [English](#english)

## 中文

### 本地

使用 `.python-version` 指定的 Python 3.12。在仓库根目录创建并激活虚拟环境：

```sh
python3.12 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell 中使用 `py -3.12 -m venv .venv` 和 `.venv\Scripts\Activate.ps1`。

安装依赖、构建和预览命令见 [README](../README.md#build)。修改内容后重新构建，再刷新浏览器。

### GitHub Actions

工作流使用标准 Ubuntu 24.04 运行器，读取 `.python-version`，安装 `requirements.txt` 中的依赖并执行构建。

工作流位于 GitHub 默认分支后，从 **Actions → Build site → Run workflow** 手动运行。工作流只构建网站，不执行发布。

## English

### Local

Use Python 3.12 as specified in `.python-version`. Create and activate a virtual environment from the repository root:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
```

In Windows PowerShell, use `py -3.12 -m venv .venv` and `.venv\Scripts\Activate.ps1` respectively.

See the [README](../README.md#build) for dependency installation, build, and preview commands. Rebuild after editing content, then refresh the browser.

### GitHub Actions

The workflow uses a standard Ubuntu 24.04 runner, reads `.python-version`, installs dependencies from `requirements.txt` and builds the site.

With the workflow on the repository’s default branch, run it from **Actions → Build site → Run workflow**. The workflow builds the site without deploying it.
