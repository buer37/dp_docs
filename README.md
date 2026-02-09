# 学习

Penn

---

## 在线访问 / 部署到 GitHub

### 方式一：在 GitHub 上直接看

把仓库推送到 GitHub 后，在网页上打开任意 `.md` 文件即可在线阅读（GitHub 会渲染 Markdown）。

### 方式二：用 GitHub Pages 做成文档站

1. **在仓库设置里开启 Pages**  
   仓库 → **Settings** → **Pages** → **Source** 选择 **GitHub Actions**。

2. **改成本人信息（可选）**  
   编辑根目录 `mkdocs.yml`，把 `site_url` 和 `repo_url` 里的 `YOUR_USERNAME` 换成你的 GitHub 用户名。

3. **推送代码**  
   推送到 `main` 或 `master` 后，Actions 会自动构建并发布。  
   完成后访问：`https://<你的用户名>.github.io/dp_docs/`。