from __future__ import annotations

import streamlit as st

from rag.generate_answer import generate_answer


EXAMPLE_QUESTIONS = [
    "How do you evolve Magmar?",
    "What happens when a Pokemon is burned?",
    "What does Heavy-Duty Boots do?",
    "What is STAB in Pokemon battles?",
]


st.set_page_config(
    page_title="Pokemon RAG Assistant",
    page_icon="P",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Source+Sans+3:wght@400;600;700&display=swap');

        :root {
            --bg: #090d14;
            --panel: rgba(18, 25, 38, 0.86);
            --panel-strong: #151d2c;
            --text: #f4f7fb;
            --muted: #a8b3c7;
            --accent: #ffcb05;
            --accent-2: #2f6db5;
            --line: rgba(255,255,255,0.12);
            --success: #4ade80;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(47,109,181,0.32), transparent 34rem),
                radial-gradient(circle at 85% 10%, rgba(255,203,5,0.13), transparent 28rem),
                linear-gradient(135deg, #090d14 0%, #101623 52%, #080b11 100%);
            color: var(--text);
            font-family: 'Source Sans 3', sans-serif;
        }

        section[data-testid="stSidebar"] {
            background: rgba(11, 16, 26, 0.92);
            border-right: 1px solid var(--line);
        }

        .block-container {
            max-width: 1160px;
            padding-top: 2.2rem;
            padding-bottom: 4rem;
        }

        h1, h2, h3 {
            font-family: 'Space Grotesk', sans-serif;
            letter-spacing: -0.04em;
        }

        .hero {
            border: 1px solid var(--line);
            background:
                linear-gradient(135deg, rgba(21,29,44,0.96), rgba(13,18,29,0.82)),
                radial-gradient(circle at 88% 18%, rgba(255,203,5,0.22), transparent 14rem);
            border-radius: 30px;
            padding: 2rem;
            box-shadow: 0 24px 80px rgba(0,0,0,0.35);
            position: relative;
            overflow: hidden;
        }

        .hero:after {
            content: "";
            position: absolute;
            right: -5rem;
            bottom: -5rem;
            width: 14rem;
            height: 14rem;
            border-radius: 50%;
            border: 34px solid rgba(255,255,255,0.04);
        }

        .eyebrow {
            color: var(--accent);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.16em;
            font-size: 0.78rem;
            margin-bottom: 0.4rem;
        }

        .hero-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(2.2rem, 5.2vw, 4.2rem);
            line-height: 1;
            font-weight: 700;
            max-width: 760px;
            margin-bottom: 1rem;
        }

        .hero-copy {
            color: var(--muted);
            font-size: 1.08rem;
            max-width: 680px;
            margin-bottom: 1.2rem;
        }

        .metric-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.8rem;
            margin-top: 1.2rem;
        }

        .pill {
            border: 1px solid var(--line);
            border-radius: 999px;
            padding: 0.55rem 0.85rem;
            background: rgba(255,255,255,0.055);
            color: var(--muted);
            font-size: 0.92rem;
        }

        .answer-card, .source-card {
            border: 1px solid var(--line);
            background: rgba(15, 22, 34, 0.88);
            border-radius: 24px;
            padding: 1.35rem;
            box-shadow: 0 16px 44px rgba(0,0,0,0.24);
        }

        .answer-card {
            border-left: 5px solid var(--accent);
            min-height: 4.75rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .results-shell {
            min-height: 0;
            margin-top: 0.35rem;
        }

        .evidence-shell {
            min-height: 0;
            margin-top: 1rem;
        }

        .section-label {
            color: var(--accent);
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 1.5rem;
            margin: 1.35rem 0 0.8rem;
        }

        .question-panel {
            margin: 1.35rem 0 1.15rem;
        }

        .search-label {
            color: #dbe7ff;
            font-size: 1rem;
            font-weight: 700;
            margin: 0.75rem 0 0.55rem;
        }

        .stTextInput {
            margin-bottom: 0;
        }

        div[data-testid="stTextInput"] input {
            border-radius: 14px;
            border: 1px solid rgba(168,179,199,0.22);
            background: rgba(255,255,255,0.075);
            color: white;
            height: 3.15rem;
            min-height: 3.15rem;
            font-size: 1.02rem;
            line-height: 1.2;
            padding: 0.65rem 1rem 1.5rem 1rem;
            box-shadow: none;
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: rgba(255,203,5,0.7);
            box-shadow: 0 0 0 3px rgba(255,203,5,0.09);
        }

        div[data-testid="stButton"] {
            margin-top: 0.25rem;
            margin-bottom: 0.45rem;
        }

        div[data-testid="stButton"] button {
            border-radius: 999px;
            border: 0;
            min-height: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--accent), #ff9f1c);
            color: #111827;
            box-shadow: 0 12px 30px rgba(255,203,5,0.18);
        }

        .small-muted {
            color: var(--muted);
            font-size: 0.94rem;
        }

        .score {
            color: var(--success);
            font-weight: 700;
        }

        .stAlert {
            margin-top: 1rem;
        }

        @media (max-width: 900px) {
            .block-container {
                padding-left: 1.1rem;
                padding-right: 1.1rem;
            }

            .hero {
                padding: 1.45rem;
                border-radius: 24px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


if "question" not in st.session_state:
    st.session_state.question = EXAMPLE_QUESTIONS[0]

if "answer" not in st.session_state:
    st.session_state.answer = None

if "retrieved_chunks" not in st.session_state:
    st.session_state.retrieved_chunks = []


with st.sidebar:
    st.markdown("### Retrieval Settings")
    st.caption("Tune how much context the RAG system sends into the answer step.")
    top_k = st.slider("Top-k retrieved chunks", min_value=1, max_value=6, value=3)
    max_context_chunks = st.slider(
        "Max context chunks",
        min_value=1,
        max_value=8,
        value=4,
        help="Includes retrieved chunks plus nearby chunks to reduce chunk-boundary misses.",
    )
    max_new_tokens = st.slider("Max answer tokens", min_value=50, max_value=300, value=160)
    st.markdown("---")
    st.markdown("### Dataset")
    st.markdown(
        """
        <div class="small-muted">
        Pokemon battle, item, weather, type, and evolution guides.
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">FAISS + Local LLM</div>
        <div class="hero-title">Pokemon RAG Assistant</div>
        <div class="hero-copy">
            Ask a Pokemon question, retrieve the most relevant dataset chunks,
            and generate an answer grounded in the retrieved context.
        </div>
        <div class="metric-row">
            <div class="pill">14 source documents</div>
            <div class="pill">61 FAISS chunks</div>
            <div class="pill">384-dim embeddings</div>
            <div class="pill">Context-only answers</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="question-panel">', unsafe_allow_html=True)

example_cols = st.columns(len(EXAMPLE_QUESTIONS))
for col, example in zip(example_cols, EXAMPLE_QUESTIONS):
    if col.button(example):
        st.session_state.question = example

st.markdown('<div class="search-label">What would you like to know?</div>', unsafe_allow_html=True)
search_col, button_col = st.columns([5, 1.25], vertical_alignment="bottom")
with search_col:
    question = st.text_input(
        "Question",
        key="question",
        label_visibility="collapsed",
        placeholder="Example: What does Heavy-Duty Boots do?",
    )

with button_col:
    ask_clicked = st.button("Search", type="primary", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

if ask_clicked:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching FAISS and generating a grounded answer..."):
            answer, retrieved_chunks = generate_answer(
                question.strip(),
                top_k=top_k,
                max_context_chunks=max_context_chunks,
                max_new_tokens=max_new_tokens,
            )
            st.session_state.answer = answer
            st.session_state.retrieved_chunks = retrieved_chunks

st.markdown('<div class="results-shell">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Final Answer</div>', unsafe_allow_html=True)
if st.session_state.answer:
    st.markdown(
        f"""
        <div class="answer-card">
            {st.session_state.answer}
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div class="answer-card">
            <strong>Ready when you are.</strong><br>
            Choose an example or type your own question, then run the RAG search.
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="evidence-shell">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Retrieved Evidence</div>', unsafe_allow_html=True)
if st.session_state.retrieved_chunks:
    for rank, (score, record) in enumerate(st.session_state.retrieved_chunks, start=1):
        metadata = record["metadata"]
        title = (
            f"{rank}. {metadata['filename']} | "
            f"Chunk {metadata['chunk_index']} | Score {score:.4f}"
        )
        with st.expander(title, expanded=rank <= 2):
            st.markdown(
                f"""
                <div class="source-card">
                    <div class="small-muted">
                        Source: <strong>{metadata['filename']}</strong>
                        &nbsp; | &nbsp;
                        Chunk: <strong>{metadata['chunk_index']}</strong>
                        &nbsp; | &nbsp;
                        Similarity: <span class="score">{score:.4f}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.text(record["text"])
else:
    st.markdown(
        """
        <div class="source-card small-muted">
            Retrieved chunks will appear here after a search.
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)
