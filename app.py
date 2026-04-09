"""
EduCompanion AI - 苏格拉底式智能助教
=====================================

基于智谱AI GLM 模型的教育对话应用，
通过苏格拉底式提问引导学生思考，而非直接给出答案。

技术栈: Python + Streamlit + 智谱AI API
作者: [Your Name]
日期: 2026-04-09
"""

import os
import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# ==========================================
# API 配置
# ==========================================
# 智谱AI海外版 Anthropic 兼容端点
ZHIPU_BASE_URL = os.getenv("ZHIPU_BASE_URL", "https://api.z.ai/api/anthropic")
ZHIPU_MODEL = os.getenv("ZHIPU_MODEL", "claude-3-sonnet-20240229")

# ==========================================
# 页面配置
# ==========================================
st.set_page_config(
    page_title="EduCompanion AI - 苏格拉底式智能助教",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 会话状态初始化
# ==========================================
def init_session_state():
    """初始化会话状态变量"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    if 'subject' not in st.session_state:
        st.session_state.subject = "STEM"
    if 'conversation_count' not in st.session_state:
        st.session_state.conversation_count = 0

init_session_state()

# ==========================================
# 侧边栏配置
# ==========================================
def render_sidebar():
    """
    渲染侧边栏配置界面
    - API Key 输入
    - 学科领域选择
    """
    st.sidebar.title("⚙️ 设置")

    # API Key 配置
    st.sidebar.markdown("### 🔑 API 配置")

    # 检查是否有配置的 API Key（来自 secrets）
    env_api_key = os.getenv("ZHIPU_API_KEY", "")
    has_configured_key = bool(env_api_key)

    # API Key 来源选择
    api_key_source = st.sidebar.radio(
        "API Key 来源",
        options=["使用配置的 API Key", "手动输入 API Key"],
        index=0 if has_configured_key else 1,
        help="默认使用部署配置的 API Key，也可以手动输入自己的密钥"
    )

    # 根据选择获取 API Key
    if api_key_source == "使用配置的 API Key":
        if has_configured_key:
            st.session_state.api_key = env_api_key
            st.sidebar.success("✅ 使用配置的 API Key")
        else:
            st.sidebar.error("❌ 未配置 API Key，请切换到手动输入")
            st.session_state.api_key = ""
    else:
        # 手动输入 API Key
        custom_api_key = st.sidebar.text_input(
            "智谱AI API Key",
            type="password",
            placeholder="请输入您的智谱AI API Key",
            value=st.session_state.api_key if st.session_state.api_key else "",
            help="手动输入的 API Key 仅在当前会话有效"
        )
        st.session_state.api_key = custom_api_key

        # 显示状态
        if custom_api_key:
            st.sidebar.success("✅ 手动 API Key 已配置")
        else:
            st.sidebar.warning("⚠️ 请输入 API Key")

    st.sidebar.divider()

    # 学科领域选择
    st.sidebar.markdown("### 📚 学科领域")

    subject_mapping = {
        "STEM": {
            "icon": "🔬",
            "description": "科学、技术、工程、数学",
            "focus": "逻辑推理、实验设计、批判性思维"
        },
        "文科": {
            "icon": "📖",
            "description": "文学、历史、哲学、社会科学",
            "focus": "文本分析、论证构建、观点评估"
        },
        "艺术": {
            "icon": "🎨",
            "description": "视觉艺术、音乐、设计、创作",
            "focus": "创意表达、审美判断、技法探索"
        }
    }

    # 渲染学科选择器
    selected_subject = st.sidebar.selectbox(
        "选择学习领域",
        options=list(subject_mapping.keys()),
        index=["STEM", "文科", "艺术"].index(st.session_state.subject)
    )

    st.session_state.subject = selected_subject

    # 显示当前学科信息
    current_subject = subject_mapping[selected_subject]
    st.sidebar.info(
        f"{current_subject['icon']} **{selected_subject}**\n\n"
        f"{current_subject['description']}\n\n"
        f"📌 关注重点：{current_subject['focus']}"
    )

    st.sidebar.divider()

    # 使用说明
    st.sidebar.markdown("### 💡 使用提示")
    st.sidebar.markdown("""
    1. **提问**：输入您想探讨的问题
    2. **思考**：AI 会通过提问引导您
    3. **回答**：给出您的思考和答案
    4. **深入**：继续探讨，深化理解

    > 我们采用苏格拉底式教学，不会直接给出答案，而是通过提问帮助您建立自己的理解。
    """)

    # 统计信息
    st.sidebar.markdown("### 📊 对话统计")
    st.sidebar.metric(
        "对话轮数",
        st.session_state.conversation_count,
        help="当前会话的对话总轮数"
    )

# ==========================================
# 系统提示词构建
# ==========================================
def build_system_prompt(subject: str) -> str:
    """
    根据选择的学科构建苏格拉底式系统提示词

    Args:
        subject: 学科领域 (STEM/文科/艺术)

    Returns:
        构建好的系统提示词
    """
    base_prompt = """你是一位苏格拉底式助教。你的核心原则是：

## 教学理念
1. **永不直接给出答案**：你的职责是引导学生独立思考，而非提供现成的解决方案
2. **通过提问引导**：使用苏格拉底式提问法，通过一系列有层次的问题帮助学生发现答案
3. **鼓励批判性思维**：引导学生质疑假设、分析逻辑、评估证据

## 交互规则
1. 首先理解学生的问题或困惑
2. 用简短的反问开始对话，引导学生反思
3. 根据学生的回答调整后续提问的难度和方向
4. 适时给予积极反馈，认可学生的思考过程
5. 避免长篇大论，保持对话的交互性

## 回复风格
- 简洁友好，使用对话式语言
- 使用表情符号增加亲和力（适当使用）
- 在关键处给予提示性引导
- 避免说教和评判

"""

    subject_prompts = {
        "STEM": """## STEM 学科专注点
- 引导学生建立严谨的逻辑推理
- 帮助学生设计实验验证思路
- 鼓励学生质疑科学假设
- 引导学生理解抽象概念与具体应用的关系

示例提问方式：
- "你认为...的原因是什么？"
- "如果...会发生什么变化？"
- "你能举一个具体的例子吗？"
- "这个现象和...有什么相似之处？"
""",
        "文科": """## 文科学科专注点
- 引导学生深入理解文本内涵
- 帮助学生构建有效的论证结构
- 鼓励学生从多角度分析问题
- 引导学生连接历史背景与当代意义

示例提问方式：
- "这个观点让你想起了什么？"
- "你认为作者想要表达什么？"
- "这个论证是否充分？为什么？"
- "从另一个角度看会怎样？"
""",
        "艺术": """## 艺术学科专注点
- 引导学生表达创作意图和情感
- 帮助学生分析作品的形式与内容
- 鼓励学生探索不同的表现手法
- 引导学生建立自己的审美判断

示例提问方式：
- "这幅作品给你什么感觉？"
- "为什么选择这种表现方式？"
- "如果改变...会产生什么效果？"
- "你希望观众感受到什么？"
"""
    }

    return base_prompt + subject_prompts.get(subject, subject_prompts["STEM"])

# ==========================================
# API 调用（流式）
# ==========================================
def stream_claude_response(messages: list, api_key: str, system_prompt: str):
    """
    调用智谱AI Anthropic 兼容 API 并返回流式响应

    Args:
        messages: 对话历史消息列表
        api_key: 智谱AI API Key
        system_prompt: 系统提示词

    Yields:
        流式文本内容

    Raises:
        ValueError: 当 API Key 无效时
        ConnectionError: 当网络连接失败时
        Exception: 其他 API 错误
    """
    try:
        # 验证 API Key
        if not api_key:
            raise ValueError("API Key 不能为空")

        # 初始化 Anthropic 客户端，使用智谱AI海外版端点
        client = Anthropic(
            api_key=api_key,
            base_url=ZHIPU_BASE_URL
        )

        # 调用 API 并流式返回响应
        with client.messages.stream(
            model=ZHIPU_MODEL,
            max_tokens=1024,
            system=system_prompt,
            messages=messages,
            temperature=0.7
        ) as stream:
            for text in stream.text_stream:
                yield text

    except ValueError as e:
        raise ValueError(f"配置错误: {str(e)}")
    except Exception as e:
        error_msg = str(e)
        if "authentication" in error_msg.lower() or "unauthorized" in error_msg.lower() or "invalid api key" in error_msg.lower():
            raise ValueError("API Key 验证失败，请检查您的密钥是否正确")
        elif "network" in error_msg.lower() or "connection" in error_msg.lower():
            raise ConnectionError("网络连接失败，请检查您的网络设置")
        elif "model" in error_msg.lower() and "not found" in error_msg.lower():
            raise ValueError("模型不存在，请检查模型配置")
        else:
            raise Exception(f"API 调用失败: {error_msg}")

# ==========================================
# 主界面渲染
# ==========================================
def render_main_interface():
    """渲染主聊天界面"""
    st.title("🎓 EduCompanion AI")
    st.markdown("**苏格拉底式智能助教 - 通过提问引导你发现答案**")

    # 显示学科标签
    subject_icons = {"STEM": "🔬", "文科": "📖", "艺术": "🎨"}
    st.markdown(
        f"<span style='background:#E8F4FD;padding:5px 15px;border-radius:15px;font-size:14px;'>"
        f"{subject_icons[st.session_state.subject]} 当前领域：{st.session_state.subject}</span>",
        unsafe_allow_html=True
    )

    st.divider()

    # 显示对话历史
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 用户输入区域
    if prompt := st.chat_input("请输入您想探讨的问题..."):
        # 检查 API Key
        if not st.session_state.api_key:
            st.error("⚠️ 请先在侧边栏配置您的 API Key")
            return

        # 添加用户消息
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)

        # 增加对话计数
        st.session_state.conversation_count += 1

        # 创建 AI 响应占位符
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            try:
                # 构建系统提示词
                system_prompt = build_system_prompt(st.session_state.subject)

                # 调用 API 获取流式响应
                response_generator = stream_claude_response(
                    messages=st.session_state.messages,
                    api_key=st.session_state.api_key,
                    system_prompt=system_prompt
                )

                # 流式显示响应
                for chunk in response_generator:
                    full_response += chunk
                    response_placeholder.markdown(full_response)

                # 添加 AI 消息到历史
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response
                })

            except ValueError as e:
                error_msg = f"❌ 配置错误：{str(e)}"
                response_placeholder.error(error_msg)
                st.error(error_msg)

            except ConnectionError as e:
                error_msg = f"❌ 网络错误：{str(e)}"
                response_placeholder.error(error_msg)
                st.error(error_msg)

            except Exception as e:
                error_msg = f"❌ 未知错误：{str(e)}"
                response_placeholder.error(error_msg)
                st.error(error_msg)

# ==========================================
# 底部功能栏
# ==========================================
def render_footer():
    """渲染底部功能栏"""
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        if st.button("🗑️ 清空对话历史", key="clear_history"):
            st.session_state.messages = []
            st.session_state.conversation_count = 0
            st.rerun()

    with col2:
        if st.button("📋 复制对话", key="copy_conversation"):
            conversation_text = "\n\n".join([
                f"**{msg['role'].upper()}**: {msg['content']}"
                for msg in st.session_state.messages
            ])
            st.toast("对话已复制到剪贴板（模拟）")

    with col3:
        if st.button("🔄 重置会话", key="reset_session"):
            st.session_state.messages = []
            st.session_state.conversation_count = 0
            st.session_state.subject = "STEM"
            st.rerun()

# ==========================================
# 主程序入口
# ==========================================
def main():
    """主程序入口"""
    # 渲染侧边栏
    render_sidebar()

    # 渲染主界面
    render_main_interface()

    # 渲染底部功能
    render_footer()

if __name__ == "__main__":
    main()
