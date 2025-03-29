# **discussions-to-blog-action**

A GitHub Action that syncs GitHub Discussions from specific categories into Markdown files, making it easy to
incorporate the discussions into static site generators like Hugo or Jekyll. Additionally, this action commits and
pushes the changes to your repository.

[**Read this in Chinese (简体中文)**](README.zh-CN.md)

[**Blog Repository Demo**](https://github.com/zhanyeye/zhanyeye.github.io) | [**Blog Page Demo
**](https://blog.readme.fun/)

---

## **Inputs**

| Input Name       | Description                                                                                                    | Required | Default                        |
|------------------|----------------------------------------------------------------------------------------------------------------|----------|--------------------------------|
| `categories`     | A comma-separated list of discussion categories to convert to Markdown posts (e.g., `Announcements, General`). | Yes      | N/A                            |
| `output_dir`     | Directory where the Markdown files will be saved.                                                              | Yes      | `content/posts`                |
| `branch`         | The branch to which changes should be committed and pushed.                                                    | Yes      | N/A                            |
| `commit_message` | The commit message for the changes.                                                                            | No       | `Sync Discussions to Markdown` |

---

## **How It Works**

1. The action fetches discussions from the specified GitHub categories.
2. It converts those discussions into Markdown files and saves them in the defined `output_dir`.
3. It stages, commits, and pushes the updated Markdown files to the specified `branch` using the [
   `stefanzweifel/git-auto-commit-action`](https://github.com/stefanzweifel/git-auto-commit-action).
4. The entire workflow is automated and integrates seamlessly into your GitHub repository.

---

## **Example Usage**

Here’s how you can use this action in your GitHub Actions workflow file:

```yaml
name: Sync Discussions to Blog

on:
  discussion:
    types: [ created, edited, deleted ]

jobs:
  sync-discussions-to-blog:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Sync Discussions
        uses: zhanyeye/discussions-to-blog-action@v1
        with:
          categories: "Announcements, General"
          output_dir: "content/posts"
          branch: main
          commit_message: "Sync Discussions to Markdown"
```

---

### **Inputs Breakdown**

#### **`categories`**

- Required: ✅
- A comma-separated list of discussion categories to process (e.g., `"Announcements, General"`). Discussions within
  these categories will be converted into Markdown posts.

#### **`output_dir`**

- Required: ✅
- Specifies the directory in your repository where the Markdown files will be output. For example, Hugo blogs usually
  use `content/posts`.

#### **`branch`**

- Required: ✅
- The branch where the changes (new or updated Markdown files) will be committed and pushed. This parameter ensures the
  ability to commit directly to a specific branch (e.g., `main`).

#### **`commit_message`**

- Required: ❌
- The message that will accompany the commit. Defaults to `"Sync Discussions to Markdown"` if not provided.

---

## **Features**

- **Discussion-to-Markdown Conversion**: Transform GitHub Discussions from specified categories into Markdown files,
  formatted for use in static site generators like Hugo or Jekyll.
- **Hands-Free Automation**: Completely automates the process of syncing, converting, committing, and pushing the
  generated files to your repository.
- **Customizable**: Allows you to control where the files are saved, which branch they’re pushed to, and how the commit
  messages are formatted.
- **Seamless Git Integration**: Uses [`stefanzweifel/git-auto-commit-action`](https://github.com/stefanzweifel/git-auto-commit-action) for lightweight and
  feature-complete Git handling.

---

## **License**

This project is licensed under the [MIT License](LICENSE).

---

### **What’s New?**

#### Updated Features:

- Replaced manual Git handling with `stefanzweifel/git-auto-commit-action`, simplifying the action.
- Added customizable inputs for committing and pushing changes (`branch` and `commit_message`).
- README now reflects these updates, breaking down parameters and making setup instructions clearer.

---