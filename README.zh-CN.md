# **discussions-to-blog-action**

一个 GitHub Action，可以将特定分类的 GitHub Discussions 转换为 Markdown 文件, 提交并推送到您的代码仓库中，方便集成到 Hugo 或 Jekyll 等静态网站生成器。

[**点击此处查看英文版文档**](README.md)  

[**博客仓demo**](https://github.com/zhanyeye/zhanyeye.github.io) | [**博客页面demo**](https://blog.readme.fun/)  

---

## **输入参数**

| 参数名称           | 描述                                                         | 是否必填 | 默认值                   |
|--------------------|------------------------------------------------------------|----------|---------------------------|
| `categories`       | 用逗号分隔的讨论分类列表，会将这些分类的讨论内容转换为 Markdown 文件（如 `Announcements, General`）。 | 是       | 无                       |
| `output_dir`       | 指定 Markdown 文件的保存目录。                                | 是       | `content/posts`           |
| `branch`           | 提交更新的目标分支名。                                       | 是       | 无                       |
| `commit_message`   | 提交时使用的消息内容。                                       | 否       | `Sync Discussions to Markdown` |

---

## **工作原理**

1. 从指定的 GitHub Discussion 分类中获取讨论内容。
2. 将讨论内容转换为 Markdown 文件，并保存到指定的 `output_dir` 目录中。
3. 使用 [`stefanzweifel/git-auto-commit-action`](https://github.com/stefanzweifel/git-auto-commit-action) 自动提交更改，并将更新推送到指定的 `branch`。
4. 整个流程全自动化，可与您的 GitHub 仓库无缝集成。

---

## **使用示例**

以下是一个简单的 GitHub Actions 工作流配置示例：

```yaml
name: Sync Discussions to Blog

on:
  discussion:  
    types: [created, edited, deleted]  

jobs:  
  sync-discussions-to-blog:  
    runs-on: ubuntu-latest  
    
    steps:  
      - name: Checkout repository  
        uses: actions/checkout@v3  

      - name: Sync Discussions  
        uses: zhanyeye/discussions-to-blog-action@main
        with:   
          categories: "Announcements, General"
          output_dir: "content/posts"
          branch: main
          commit_message: "Sync Discussions to Markdown"
```

---

### **参数说明**

#### **`categories`**
- **是否必填**：✅
- 指定一个用逗号分隔的讨论分类列表（如 `"Announcements, General"`）。在这些分类中的讨论内容将被转换为 Markdown 文件。

#### **`output_dir`**
- **是否必填**：✅
- 指定保存生成的 Markdown 文件的目录。例如，Hugo 博客通常会使用 `content/posts`。

#### **`branch`**
- **是否必填**：✅
- 指定用于提交更新的分支名称，例如 `main`。

#### **`commit_message`**
- **是否必填**：❌
- 自定义提交信息。如果未指定，将默认使用 `"Sync Discussions to Markdown"`。

---

## **功能亮点**

- **将讨论转换为 Markdown**：将 GitHub Discussions 中指定分类的内容转换为 Markdown 文件，并适配静态网站生成器（如 Hugo 或 Jekyll）。
- **自动化工作流**：整个流程自动化，无需人工干预，节省操作时间。
- **高可定制性**：支持自定义文件保存路径、目标分支及提交信息，轻松适配不同项目需求。
- **与 Git 无缝集成**：借助 [`stefanzweifel/git-auto-commit-action`](https://github.com/stefanzweifel/git-auto-commit-action)，提供轻量级的 Git 操作支持。

---

## **许可证**

本项目基于 [MIT 许可证](LICENSE)。

---

### **更新日志**

#### 新增功能：
- 使用 `stefanzweifel/git-auto-commit-action` 替代手动 Git 操作，简化了配置。
- 支持通过 `branch` 和 `commit_message` 输入参数定制提交及推送设置。
- 完善了 README 文档，增加对参数的详细说明，简化了使用指南。

---
