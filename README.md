# EduCompanion AI - 苏格拉底式智能助教

> 一个基于智谱AI GLM 模型的教育对话应用，通过苏格拉底式提问引导学生独立思考

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![Zhipu AI](https://img.shields.io/badge/Zhipu_AI-GLM%204-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## 📖 项目背景

在传统教育模式中，学生往往习惯于直接获取答案，而缺乏主动思考和批判性思维的训练。**EduCompanion AI** 旨在改变这一现状，通过模拟苏格拉底式教学方法，引导学生通过自我探索建立知识体系。

### 核心理念

- **不直接给出答案**：AI 助教不会提供现成的解决方案
- **苏格拉底式提问**：通过层次化的问题引导学生发现答案
- **学科专业化**：针对不同学科（STEM/文科/艺术）提供定制化的引导策略
- **流式交互体验**：实时响应，提升对话自然度

## 🏗️ 技术架构

```
EduCompanion AI/
├── app.py              # 主应用程序
├── requirements.txt    # 依赖包列表
├── README.md           # 本说明文档
└── .env                # 环境变量（用户自行创建）
```

### 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.8+ | 主要开发语言 |
| Streamlit | 1.28+ | Web 应用框架 |
| 智谱AI API | GLM-4 | 大语言模型服务 |
| python-dotenv | 1.0+ | 环境变量管理 |
| requests | 2.31+ | HTTP 请求处理 |

### 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                        Streamlit UI                          │
├──────────────┬──────────────────────────────────────────────┤
│   侧边栏     │              主对话区域                        │
│              │                                               │
│  • API Key   │   ┌─────────────┐    ┌─────────────┐         │
│  • 学科选择  │   │  User Msg   │    │  AI Msg     │         │
│  • 对话统计  │   │             │    │             │         │
│  • 使用提示  │   └─────────────┘    └─────────────┘         │
│              │                                               │
└──────────────┴──────────────────────────────────────────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │   智谱AI GLM API    │
                   │   (流式响应支持)    │
                   └─────────────────────┘
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd sutd-chat
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API Key

获取智谱AI API Key：
1. 访问 [智谱AI开放平台](https://open.bigmodel.cn/)
2. 注册/登录账号
3. 进入「API Keys」页面创建新密钥
4. 复制生成的 API Key

**方式一：环境变量（推荐）**

创建 `.env` 文件：
```bash
ZHIPU_API_KEY=xxxxxxxxxxxxxxxx
```

**方式二：应用内输入**

启动应用后在侧边栏手动输入 API Key。

### 4. 启动应用

```bash
streamlit run app.py
```

浏览器自动打开 `http://localhost:8501`

## ✨ 核心功能演示

### 1. 学科领域选择

侧边栏提供三个学科领域：

| 学科 | 图标 | 专注方向 |
|------|------|----------|
| 🔬 STEM | 🧪 | 逻辑推理、实验设计、批判性思维 |
| 📖 文科 | 📚 | 文本分析、论证构建、观点评估 |
| 🎨 艺术 | 🖌️ | 创意表达、审美判断、技法探索 |

### 2. 苏格拉底式对话流程

```
学生：为什么天空是蓝色的？

AI（STEM 模式）：
  这是一个很好的观察！🌤️
  你觉得光和颜色之间有什么关系呢？
  想象一下，当你看到彩虹时，是什么让它呈现出不同的颜色？

学生：光是很多颜色的混合吧...

AI：
  正确！👍
  那么当阳光穿过大气层时，不同颜色的光会发生什么？
  你有没有想过，为什么日落时天空会变成橙红色呢？
```

### 3. 流式输出

应用支持实时流式输出，让对话体验更加自然流畅：

```python
# 流式调用示例
response = requests.post(
    "https://open.bigmodel.cn/api/paas/v4/chat/completions",
    headers=headers,
    json={"stream": True, ...},
    stream=True
)

for line in response.iter_lines():
    if line.startswith(b'data: '):
        data = json.loads(line[6:])
        content = data['choices'][0]['delta']['content']
        yield content  # 逐字返回
```

### 4. 对话管理

- **清空对话**：一键清除所有历史记录
- **复制对话**：导出当前对话内容
- **重置会话**：恢复初始设置

## 🌐 部署到 Streamlit Cloud

Streamlit Cloud 提供免费的托管服务，以下是部署步骤：

### 1. 准备代码仓库

确保项目已推送到 GitHub：

```bash
git init
git add .
git commit -m "Initial commit: EduCompanion AI"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. 创建部署

1. 访问 [Streamlit Cloud](https://share.streamlit.io/)
2. 点击 "Deploy an app"
3. 关联你的 GitHub 账号
4. 选择 `sutd-chat` 仓库和 `main` 分支
5. 填写以下信息：

| 字段 | 值 |
|------|-----|
| Repository | `your-username/sutd-chat` |
| Branch | `main` |
| Main file path | `app.py` |
| App URL | `educompanion-ai` (可选自定义) |

### 3. 配置环境变量

在部署设置中添加 Secret：

1. 进入应用设置 → **Secrets** 标签
2. 点击 **+ Add new secret**
3. 添加以下环境变量：

```
ZHIPU_API_KEY = xxxxxxxxxxxxxxxx
```

### 4. 启动应用

点击 **Deploy** 按钮，等待几分钟即可访问：
```
https://educompanion-ai.streamlit.app
```

### 部署注意事项

- ✅ 确保 `requirements.txt` 版本兼容性
- ✅ API Key 通过 Secret 管理，不要硬编码
- ✅ 应用会自动检测 `ZHIPU_API_KEY` 环境变量
- ✅ 免费版有 60分钟/天的运行时长限制

## 📝 代码结构说明

### `app.py` 模块划分

```python
# 1. 页面配置
st.set_page_config(...)

# 2. 会话状态管理
def init_session_state(): ...

# 3. 侧边栏渲染
def render_sidebar(): ...

# 4. 系统提示词构建
def build_system_prompt(subject: str) -> str: ...

# 5. API 调用（流式）
def stream_glm_response(...): ...

# 6. 主界面渲染
def render_main_interface(): ...

# 7. 底部功能
def render_footer(): ...

# 8. 主入口
def main(): ...
```

### 关键函数说明

| 函数 | 功能 |
|------|------|
| `build_system_prompt()` | 根据学科定制苏格拉底式系统提示词 |
| `stream_glm_response()` | 流式调用智谱AI API，支持实时输出 |
| `render_sidebar()` | 渲染侧边栏，处理配置输入 |
| `render_main_interface()` | 渲染主聊天界面和对话流 |

## 🔒 安全与错误处理

### API Key 验证

```python
# 验证 API Key
if not api_key:
    raise ValueError("API Key 不能为空")
```

### 网络异常处理

```python
try:
    # API 调用
    response = requests.post(...)
except requests.exceptions.Timeout:
    raise ConnectionError("请求超时，请检查您的网络连接")
except requests.exceptions.ConnectionError:
    raise ConnectionError("网络连接失败，请检查您的网络设置")
```

## 📊 使用示例

### STEM 场景示例

**问题**：什么是相对论？

**AI 引导流程**：
1. 先问"你觉得时间和空间是什么关系？"
2. 引导学生思考运动对观测的影响
3. 用类比（如列车、电梯）帮助理解
4. 最终让学生自己总结相对论的核心思想

### 文科场景示例

**问题**：这首诗表达了什么情感？

**AI 引导流程**：
1. 问"哪几句诗让你有这样的感觉？"
2. 引导分析意象和修辞手法
3. 联系诗人的时代背景
4. 让学生对情感表达给出自己的解读

## 🎯 教学效果预期

使用 EduCompanion AI 进行学习时，学生可以：

- ✅ 培养独立思考和问题解决能力
- ✅ 提升批判性思维和逻辑推理水平
- ✅ 学会自我提问和自我反思
- ✅ 建立更深入的知识理解结构

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**作者**：[Your Name]
**课程**：人工智能赋能教育
**日期**：2026-04-09
