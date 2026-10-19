# 架构 / Architecture

[中文](#中文) · [English](#english)

## 中文

### 构建

读取 `content/` → 解析页面信息和 Markdown → 使用 `templates/` 渲染 → 写入 `dist/`。

Markdown 文件以 YAML 页面信息开头，必须提供纯文本 `title`。模板生成一级标题，正文标题从二级开始。正文使用 CommonMark，原始 HTML 按文本处理。解析器通过独立接口接入。

构建时校验标题、转义页面信息。所有页面渲染成功后替换 `dist/`，清除旧输出。`dist/` 不纳入 Git，构建与发布分开。

### 语言与路径

中文放在 `content/`，网址从 `/` 开始；其他语言放在 `content/<language>/`，网址使用对应前缀，如 `/en/`。新增语言需在生成器的 `LANGUAGES` 中添加代码和名称，其目录专用于该语言。

`content/index.md` 是必需的中文首页。`index.md` 对应所在目录，其他 Markdown 文件生成同名目录。

去掉语言目录后，路径相同的文件互为译文。页面只链接已有译文。内部文档则在同一文件中分别编排完整的中文和英文。

### 链接与资源

相对 Markdown 链接从源文件所在目录解析，转换为页面网址。以 `/` 开头的链接按站内网址检查。外部链接保持原样。

查询参数和锚点原样保留，不检查页面内的锚点是否存在。

`assets/` 复制到 `dist/assets/`，资源链接转换为 `/assets/...`。缺失或未发布的本地目标会使构建失败。资源不支持符号链接，`.gitkeep` 不进入输出。

## English

### Build

Read `content/` → Parse metadata and Markdown → Render with `templates/` → Write to `dist/`.

Markdown files start with YAML metadata and require a plain-text `title`. The template renders an H1; body headings start at H2. The parser uses CommonMark, treats raw HTML as text, and connects through a separate interface.

The build validates titles and escapes metadata. After all pages render successfully, it replaces `dist/`, removing stale output. `dist/` is excluded from Git. Build and deployment are separate.

### Languages and paths

Chinese content lives in `content/` and uses URLs starting at `/`. Other languages live in `content/<language>/` and use the matching URL prefix, such as `/en/`. Add each language code and name to the generator’s `LANGUAGES` mapping; its directory is reserved for that language.

`content/index.md` is the required Chinese homepage. Each `index.md` maps to its directory; other Markdown files create directories named after their file stems.

Files with matching paths after removing the language directory are translations of each other. Pages link only to existing translations. Internal documents keep complete Chinese and English sections in the same file.

### Links and assets

Relative Markdown links resolve from the source file’s directory and become page URLs. Links starting with `/` are checked against site URLs. External links remain unchanged.

Query strings and fragments are preserved. Anchors within pages are not checked.

`assets/` is copied to `dist/assets/`, and asset links become `/assets/...`. Missing or unpublished local targets fail the build. Asset symlinks are unsupported; `.gitkeep` is excluded from output.
