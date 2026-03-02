# GitHub 仓库管理

使用 `gh` CLI 和 Git 进行仓库创建、初始化和推送操作。

---

## 使用场景

- 创建新的 GitHub 仓库
- 初始化本地 Git 并关联到 GitHub
- 配置认证并推送代码
- 设置自动化提交

---

## 前提条件

- ✅ `gh` CLI 已安装（检查：`which gh`）
- ✅ 已登录 GitHub（检查：`gh auth status`）
- ✅ Git 已配置用户信息（`git config user.name/email`）

---

## 快速流程

### 1️⃣ 检查登录状态

```bash
gh auth status
```

如未登录，提示用户运行：
```bash
gh auth login
```

---

### 2️⃣ 创建仓库

```bash
gh repo create <仓库名> --public --description "<描述>"
```

参数：
- `--public` / `--private`：仓库可见性
- `--description`：仓库描述（可选）
- `--source=<本地路径> --push`：直接初始化并推送（本地已 git 时）

---

### 3️⃣ 配置 Git Remote

```bash
cd <本地路径>
git remote add origin git@github.com:<用户名>/<仓库名>.git
```

或使用 HTTPS（需配置 credential helper）：
```bash
git remote add origin https://github.com/<用户名>/<仓库名>.git
```

---

### 4️⃣ 初始化并提交

```bash
# 如未初始化
git init

# 添加所有文件
git add -A

# 首次提交
git commit -m "Initial commit: <描述>"
```

---

### 5️⃣ 推送到 GitHub

```bash
# 首次推送
git push -u origin master

# 后续推送
git push
```

---

## 常见问题

### SSH 认证失败

**症状**：`Permission denied (publickey)`

**解决**：
- 检查 SSH key：`ls -la ~/.ssh/ | grep id_rsa`
- 如无，生成：`ssh-keygen -t ed25519`
- 添加公钥到 GitHub：`cat ~/.ssh/id_ed25519.pub`

### HTTPS 推送需认证

**选项 A**：使用 GitHub CLI 认证
```bash
# gh auth token 获取 token
echo "https://<用户名>:<token>@github.com" > ~/.git-credentials
git config --global credential.helper store --file=~/.git-credentials
```

**选项 B**：使用 osxkeychain（macOS）
```bash
git config --global credential.helper osxkeychain
# 首次推送会弹出密码框
```

### 推送超时

**症状**：`Could't connect to server after 75020ms`

**解决**：检查网络，重试：
```bash
git push
```

---

## 完整示例

```bash
# 1. 检查登录
gh auth status

# 2. 创建仓库
gh repo create my-project --public --description "我的项目"

# 3. 进入本地目录并关联
cd ~/projects/my-project
git remote add origin git@github.com:username/my-project.git

# 4. 提交
git add -A
git commit -m "Initial commit"

# 5. 推送
git push -u origin master
```

---

## 用户信息参考

- **GitHub 用户**：NiklausTxt
- **邮箱**：tongxiaotong139@163.com
- **认证方式**：GitHub CLI (gh) 浏览器授权
- **默认分支**：master
