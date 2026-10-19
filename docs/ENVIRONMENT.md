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

工作流在 Ubuntu 24.04 上构建网站，将 `dist/` 发布到 GitHub Pages。Python 版本由 `.python-version` 指定。

在 **Settings → Pages → Source** 中选择 **GitHub Actions**。工作流推送到 `main` 后，每次推送到该分支都会自动构建并发布。

也可在 **Actions → Deploy site → Run workflow** 中选择 `main`，手动发布。

网站：[leisuregensoul.github.io](https://leisuregensoul.github.io/)。

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

The workflow builds on Ubuntu 24.04 and deploys `dist/` to GitHub Pages. `.python-version` specifies the Python version.

Under **Settings → Pages → Source**, select **GitHub Actions**. Once the workflow is pushed to `main`, every push to that branch automatically builds and deploys the site.

To deploy manually, open **Actions → Deploy site → Run workflow** and select `main`.

Site: [leisuregensoul.github.io](https://leisuregensoul.github.io/).
