import html
from typing import Any

import streamlit as st
from dotenv import load_dotenv


load_dotenv()

st.set_page_config(
    page_title="Violet | Travel Copilot",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

        :root {
            --violet: #6d3df5;
            --violet-deep: #3f237f;
            --ink: #211b35;
            --muted: #68617b;
            --line: #ded8eb;
            --paper: #ffffff;
            --app-bg: #f4f2f8;
            --chat-bg: #eeebf5;
            --input-bg: #ffffff;
            --input-line: #cfc5e5;
            --placeholder: #817992;
            --assistant-bg: #ffffff;
            --user-bg: #e9e1ff;
            --coral: #ff765c;
            --mint: #1eae9f;
        }

        html,
        body,
        button,
        input,
        textarea,
        [class*="css"],
        [data-testid="stAppViewContainer"],
        [data-testid="stSidebar"] {
            font-family: 'DM Sans', sans-serif;
            color: var(--ink) !important;
        }

        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"] {
            background: var(--app-bg) !important;
            color: var(--ink) !important;
        }

        [data-testid="stHeader"] {
            background: var(--app-bg) !important;
        }

        [data-testid="stSidebar"] {
            background: var(--paper) !important;
            border-right: 1px solid var(--line);
        }

        [data-testid="stSidebar"] > div:first-child {
            padding: 1.35rem 1.1rem 1.5rem;
        }

        .block-container {
            max-width: 1240px;
            padding: 1.35rem clamp(1rem, 3vw, 3.6rem) 3rem;
        }

        .block-container p,
        .block-container li,
        .block-container label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label {
            color: var(--ink);
        }

        .violet-brand {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            margin-bottom: 2.2rem;
        }

        .brand-mark {
            display: grid;
            place-items: center;
            width: 2.4rem;
            height: 2.4rem;
            border-radius: 0.85rem;
            background: var(--violet);
            color: white;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.2rem;
            font-weight: 800;
            box-shadow: 0 8px 18px rgba(109, 61, 245, 0.2);
        }

        .brand-name {
            color: var(--ink);
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.15rem;
            font-weight: 800;
            letter-spacing: 0;
        }

        .brand-note {
            color: var(--muted);
            font-size: 0.72rem;
            margin-top: 0.12rem;
        }

        .sidebar-label {
            color: #a19ab2;
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            margin: 1.4rem 0 0.65rem;
            text-transform: uppercase;
        }

        .sidebar-tip {
            border: 1px solid var(--line);
            border-radius: 0.75rem;
            background: #faf8ff;
            color: var(--muted);
            font-size: 0.78rem;
            line-height: 1.55;
            padding: 0.75rem 0.8rem;
        }

        .sidebar-tip strong {
            color: var(--violet-deep);
        }

        .main-topline {
            align-items: center;
            display: flex;
            justify-content: space-between;
            margin-bottom: 1.2rem;
        }

        .eyebrow {
            color: var(--violet);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }

        .status-pill {
            align-items: center;
            background: #effaf7;
            border: 1px solid #ccefe9;
            border-radius: 999px;
            color: #168b7f;
            display: inline-flex;
            font-size: 0.74rem;
            font-weight: 700;
            gap: 0.4rem;
            padding: 0.42rem 0.7rem;
        }

        .status-dot {
            background: var(--mint);
            border-radius: 50%;
            display: inline-block;
            height: 0.42rem;
            width: 0.42rem;
        }

        .hero {
            align-items: stretch;
            background: var(--violet-deep);
            border-radius: 1.15rem;
            color: white;
            display: flex;
            justify-content: space-between;
            min-height: 220px;
            overflow: hidden;
            padding: clamp(1.3rem, 3vw, 2.15rem);
            position: relative;
        }

        .hero:after {
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 50%;
            content: '';
            height: 240px;
            position: absolute;
            right: -75px;
            top: -95px;
            width: 240px;
        }

        .hero-copy {
            max-width: 620px;
            position: relative;
            z-index: 1;
        }

        .hero-kicker {
            color: #d9cdff;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            margin-bottom: 0.7rem;
        }

        .hero h1 {
            color: white;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: clamp(1.75rem, 4vw, 3.1rem);
            letter-spacing: 0;
            line-height: 1.08;
            margin: 0;
            max-width: 590px;
        }

        .hero p {
            color: #eee9ff;
            font-size: 0.94rem;
            line-height: 1.6;
            margin: 0.85rem 0 0;
            max-width: 500px;
        }

        .hero-stamp {
            align-self: flex-end;
            background: var(--coral);
            border-radius: 1rem;
            color: white;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.8rem;
            font-weight: 800;
            line-height: 1.15;
            margin: 0 1rem 0 1.5rem;
            padding: 1rem;
            position: relative;
            transform: rotate(4deg);
            width: 106px;
            z-index: 1;
        }

        .hero-stamp span {
            display: block;
            font-size: 1.65rem;
            margin-bottom: 0.25rem;
        }

        .section-heading {
            align-items: baseline;
            display: flex;
            justify-content: space-between;
            margin: 1.75rem 0 0.8rem;
        }

        .section-heading h2 {
            color: var(--ink);
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.05rem;
            letter-spacing: 0;
            margin: 0;
        }

        .section-heading span {
            color: var(--muted);
            font-size: 0.77rem;
        }

        .prompt-card {
            background: var(--assistant-bg);
            border: 1px solid var(--line);
            border-radius: 0.85rem;
            min-height: 94px;
            padding: 0.95rem 1rem;
        }

        .prompt-icon {
            font-size: 1.25rem;
            line-height: 1;
            margin-bottom: 0.55rem;
        }

        .prompt-card strong {
            color: var(--ink);
            display: block;
            font-size: 0.84rem;
            line-height: 1.35;
        }

        .prompt-card small {
            color: var(--muted);
            display: block;
            font-size: 0.73rem;
            line-height: 1.35;
            margin-top: 0.28rem;
        }

        [data-testid="stChatMessage"] {
            background: var(--assistant-bg) !important;
            border: 1px solid var(--line);
            border-radius: 0.9rem;
            margin-bottom: 0.75rem;
            padding: 0.9rem 1rem;
        }

        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
            background: var(--user-bg) !important;
            border-color: #d4c5ff;
        }

        [data-testid="stChatMessageContent"],
        [data-testid="stChatMessageContent"] p,
        [data-testid="stChatMessageContent"] li,
        [data-testid="stChatMessageContent"] strong {
            color: var(--ink) !important;
            font-size: 0.91rem;
            line-height: 1.65;
        }

        [data-testid="stChatInput"] {
            background: var(--chat-bg) !important;
            border: 1px solid var(--line);
            border-radius: 1rem;
            margin-top: 0.6rem;
            padding: 0.65rem 0.75rem 0.75rem;
        }

        [data-testid="stChatInput"] form,
        [data-testid="stChatInput"] > div,
        [data-testid="stChatInput"] [data-baseweb="textarea"] {
            background: var(--input-bg) !important;
            border-radius: 0.72rem !important;
        }

        [data-testid="stChatInput"] textarea,
        [data-testid="stChatInput"] input {
            background: var(--input-bg) !important;
            border: 1px solid var(--input-line) !important;
            border-radius: 0.72rem !important;
            color: var(--ink) !important;
            caret-color: var(--violet) !important;
            min-height: 58px;
            opacity: 1 !important;
        }

        [data-testid="stChatInput"] textarea::placeholder,
        [data-testid="stChatInput"] input::placeholder {
            color: var(--placeholder) !important;
            opacity: 1 !important;
        }

        [data-testid="stChatInput"] textarea:focus,
        [data-testid="stChatInput"] input:focus {
            border-color: var(--violet) !important;
            box-shadow: 0 0 0 3px rgba(109, 61, 245, 0.14) !important;
        }

        [data-testid="stChatInput"] button {
            background: var(--violet) !important;
            border: 1px solid var(--violet) !important;
            border-radius: 0.62rem !important;
            color: white !important;
        }

        [data-testid="stChatInput"] button:hover {
            background: var(--violet-deep) !important;
            border-color: var(--violet-deep) !important;
        }

        .empty-chat {
            border: 1px dashed #d9d0ec;
            border-radius: 0.9rem;
            color: var(--muted);
            margin: 1.2rem 0 0.9rem;
            padding: 1rem 1.1rem;
            text-align: center;
        }

        .empty-chat strong {
            color: var(--ink);
            display: block;
            margin-bottom: 0.28rem;
        }

        .source-box {
            background: #faf9fd;
            border-left: 3px solid var(--violet);
            border-radius: 0 0.65rem 0.65rem 0;
            margin-top: 0.7rem;
            padding: 0.75rem 0.85rem;
        }

        .source-title {
            color: var(--ink);
            font-size: 0.78rem;
            font-weight: 700;
            line-height: 1.4;
        }

        .source-meta {
            color: var(--muted);
            font-size: 0.7rem;
            margin-top: 0.28rem;
        }

        .footer-note {
            color: #aaa4b8;
            font-size: 0.72rem;
            padding-top: 1rem;
            text-align: center;
        }

        .stButton > button {
            background: var(--paper) !important;
            border: 1px solid var(--input-line) !important;
            border-radius: 0.7rem;
            color: var(--ink) !important;
            font-size: 0.82rem;
            font-weight: 700;
            min-height: 2.55rem;
        }

        .stButton > button:hover {
            background: #f5f1ff !important;
            border-color: var(--violet) !important;
            color: var(--violet-deep) !important;
        }

        .stButton > button[kind="primary"] {
            background: var(--violet) !important;
            border-color: var(--violet) !important;
            color: white !important;
        }

        .stButton > button[kind="primary"]:hover {
            background: var(--violet-deep) !important;
            border-color: var(--violet-deep) !important;
            color: white !important;
        }

        [data-testid="stSidebar"] .stButton > button {
            background: var(--paper) !important;
            color: var(--ink) !important;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background: #f5f1ff !important;
            color: var(--violet-deep) !important;
        }

        [data-testid="stMarkdownContainer"] a {
            color: var(--violet-deep) !important;
        }

        @media (max-width: 760px) {
            .hero {
                min-height: auto;
            }

            .hero-stamp {
                display: none;
            }

            .main-topline {
                margin-top: 0.35rem;
            }

            .section-heading {
                margin-top: 1.35rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_brand() -> None:
    st.markdown(
        """
        <div class="violet-brand">
            <div class="brand-mark">V</div>
            <div>
                <div class="brand-name">Violet</div>
                <div class="brand-note">travel knowledge, made easy</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sources(sources: list[dict[str, Any]]) -> None:
    if not sources:
        return

    with st.expander(f"✦ Nguồn tham khảo · {len(sources)} tài liệu", expanded=False):
        for index, source in enumerate(sources, 1):
            metadata = source.get("metadata", {})
            title = metadata.get("title", "Tài liệu du lịch")
            doc_type = metadata.get("doc_type", "knowledge")
            score = source.get("score")
            score_text = f" · match {float(score):.2f}" if isinstance(score, (int, float)) else ""
            st.markdown(
                f"""
                <div class="source-box">
                    <div class="source-title">{index}. {html.escape(str(title))}</div>
                    <div class="source-meta">{html.escape(str(doc_type))}{score_text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def get_generation_answer(query: str, top_k: int) -> dict[str, Any]:
    """Keep the existing generation TODO as a lazy integration point."""
    try:
        from src.task10_generation import generate_with_citation

        return generate_with_citation(query, top_k=top_k)
    except Exception:
        return {
            "answer": (
                "Violet đã nhận câu hỏi của bạn. Pipeline generation hiện chưa sẵn sàng "
                "hoặc chưa có đủ cấu hình trong `.env`, nên mình chưa thể xác minh câu trả lời."
            ),
            "sources": [],
            "retrieval_source": "none",
        }


def get_streaming_generation(query: str, top_k: int):
    from src.task10_generation import stream_generation_with_citation

    return stream_generation_with_citation(query, top_k=top_k)


inject_styles()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "suggested_query" not in st.session_state:
    st.session_state.suggested_query = ""

with st.sidebar:
    render_brand()
    st.markdown('<div class="sidebar-label">Workspace</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-tip"><strong>Violet</strong> giúp bạn khám phá thông tin '
        "du lịch, chính sách và điểm đến từ kho tài liệu của nhóm.</div>",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-label">Retrieval settings</div>', unsafe_allow_html=True)
    top_k = st.slider("Số chunks", 3, 10, 5, help="Số đoạn tài liệu dùng để tạo câu trả lời.")

    st.markdown('<div class="sidebar-label">Mood hôm nay</div>', unsafe_allow_html=True)
    travel_mood = st.selectbox(
        "Chọn mood",
        ["Chill cuối tuần", "Đi sâu văn hoá", "Ăn là ghiền", "Plan thật nhanh"],
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-label">Session</div>', unsafe_allow_html=True)
    if st.button("↻  Làm mới cuộc trò chuyện", use_container_width=True):
        st.session_state.messages = []
        st.session_state.suggested_query = ""
        st.rerun()

    st.caption(f"Đang ở mood: {travel_mood}")

st.markdown(
    """
    <div class="main-topline">
        <div class="eyebrow">Violet / travel knowledge assistant</div>
        <div class="status-pill"><span class="status-dot"></span> đang hoạt động</div>
    </div>
    <section class="hero">
        <div class="hero-copy">
            <div class="hero-kicker">✦ Đi đâu cũng có câu trả lời</div>
            <h1>Khám phá Việt Nam<br>theo cách của bạn.</h1>
            <p>Hỏi Violet về điểm đến, chính sách du lịch, văn hoá địa phương và những điều đáng trải nghiệm tiếp theo.</p>
        </div>
        <div class="hero-stamp"><span>✈</span>let's<br>go somewhere</div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-heading">
        <h2>Gợi ý để bắt đầu</h2>
        <span>chạm một ý tưởng, Violet sẽ lo phần còn lại</span>
    </div>
    """,
    unsafe_allow_html=True,
)

prompt_columns = st.columns(3, gap="small")
prompt_data = [
    ("📍", "Ninh Bình có gì hay?", "Điểm đến nổi bật và trải nghiệm nên thử"),
    ("🍜", "Ăn gì ở miền Bắc?", "Gợi ý món địa phương đáng để săn"),
    ("🧭", "Lên plan 2 ngày", "Một lịch trình gọn, vui, không vội"),
]
for column, (icon, title, description) in zip(prompt_columns, prompt_data):
    with column:
        st.markdown(
            f"""
            <div class="prompt-card">
                <div class="prompt-icon">{icon}</div>
                <strong>{title}</strong>
                <small>{description}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Hỏi Violet", key=f"prompt_{title}", use_container_width=True):
            st.session_state.suggested_query = title
            st.rerun()

st.markdown(
    """
    <div class="section-heading">
        <h2>Cuộc trò chuyện</h2>
        <span>hỏi tự nhiên như đang nhắn tin</span>
    </div>
    """,
    unsafe_allow_html=True,
)

if not st.session_state.messages:
    st.markdown(
        """
        <div class="empty-chat">
            <strong>Violet đang nghe đây.</strong>
            Bắt đầu với một câu hỏi về nơi bạn muốn đi, điều bạn muốn biết hoặc chuyến đi bạn đang mơ.
        </div>
        """,
        unsafe_allow_html=True,
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            render_sources(message.get("sources", []))

query = st.chat_input(
    "Ví dụ: Cuối tuần này nên khám phá gì ở Ninh Bình?",
    key="chat_input",
)
query = query or st.session_state.suggested_query
st.session_state.suggested_query = ""

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Violet đang lục tìm những mảnh ghép phù hợp..."):
            try:
                token_stream, sources = get_streaming_generation(query, top_k)
                answer = st.write_stream(token_stream)
                result = {
                    "answer": answer,
                    "sources": sources,
                    "retrieval_source": sources[0].get("retrieval_method", "none")
                    if sources else "none",
                }
            except Exception:
                result = get_generation_answer(query, top_k)
                answer = result.get("answer", "Mình chưa tìm được câu trả lời phù hợp từ kho tài liệu hiện có.")
                sources = result.get("sources", [])
                st.markdown(answer)
        render_sources(sources)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
            "retrieval_source": result.get("retrieval_source", "none"),
        }
    )

st.markdown(
    '<div class="footer-note">Violet chỉ trả lời dựa trên kho tài liệu đã được cung cấp.</div>',
    unsafe_allow_html=True,
)
