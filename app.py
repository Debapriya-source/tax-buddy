import torch
import os


from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import dotenv_values
import streamlit as st
import streamlit.components.v1 as components
from agent import agent
from tools.query_enhancer import query_enhancer

# Prevent Streamlit’s watcher from examining torch.classes
torch.classes.__path__ = []  # or point to a valid folder if needed

# Load environment variables
try:
    ENVs = dotenv_values(".env")  # for local dev
    GROQ_API_KEY = ENVs["GROQ_API_KEY"]
except Exception:
    ENVs = st.secrets  # for Streamlit deployment
    GROQ_API_KEY = ENVs["GROQ_API_KEY"]

# Set API keys in OS env
os.environ["GROQ_API_KEY"] = ENVs["GROQ_API_KEY"]
os.environ["HUGGINGFACE_API_KEY"] = ENVs["HUGGINGFACE_API_KEY"]

# Streamlit app configuration
st.set_page_config(
    page_title="Tax Buddy 👩‍💻 🗒️",
    page_icon="🗒️",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Tax Buddy 👩‍💻")
initial_msg = """
    #### Welcome!!!  I am your tax assistant chatbot 👩‍💻
    #### You can ask me any queries about the new tax regime of India
    > NOTE: Currently I have only access to the FAQs of the budget 2025 and the Finance Bill 2025. So, I'll answer relevant queries only😇
    """
st.markdown(initial_msg)

# Initialize session history
if "store" not in st.session_state:
    st.session_state.store = []

store = st.session_state.store

# Render chat history
for message in store:
    avatar = "👩‍💻" if message.type == "ai" else "🗨️"
    with st.chat_message(message.type, avatar=avatar):
        st.markdown(message.content)

if prompt := st.chat_input("What is your query?"):
    # 1) Show user message
    st.chat_message("user", avatar="🗨️").markdown(prompt)

    # 2) Blinking “Thinking…” indicator
    placeholder = st.empty()
    with placeholder.container():
        with st.chat_message("assistant", avatar="👩‍💻"):
            components.html(
                """
                <div style="font-weight:bold; font-size:16px; font-family:cursive; color:#555;">
                  <span class="blinking">Thinking...</span>
                </div>
                <style>
                  .blinking { animation: blink-animation 2.5s ease-in-out infinite; }
                  @keyframes blink-animation {
                    0%, 90%, 100% { opacity: 1; }
                    50% { opacity: 0; }
                  }
                </style>
                """,
                height=40,
            )

    # 3) Enhance & store user message
    # Enhance the query
    enhanced_queries = query_enhancer(prompt)
    print(f"enhanced_queries: {enhanced_queries}")

    # Store the user message and enhanced queries
    final_user_query = f"Please use proper quotations (such as any section no. or specific lines etc.) from the PDFs when crafting your answer (references should be strictly from the PDFs only). Add a proper disclaimer. prompt: {prompt}\n\nenhanced_queries: {enhanced_queries}.\n\nNOTE: Do not include anything in final response, from inside the <think></think> section"
    user_message = HumanMessage(content=final_user_query)
    store.append(HumanMessage(content=prompt))

    # 4) Call agent() and unpack final answer + partial reasoning
    answer, partial = agent(final_user_query)

    print(f"Final answer: {answer}")
    print(f"Partial reasoning: {partial}")

    # 5) Remove blinking
    placeholder.empty()

    # 6) Show partial thoughts as Markdown inside the expander

    with st.expander("Reasoning", expanded=False):
        # 1) Scoped CSS for only this expander
        st.markdown(
            """
            <style>
            /* Only target elements inside this expander */
            .streamlit-expanderContent .md-container h3 {
                color: #2E86AB;
                margin-bottom: 0.25em;
            }
            .streamlit-expanderContent .md-container p {
                font-style: italic;
                margin-top: 0.5em;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        # 2) Render the reasoning blob as Markdown inside a container div
        st.markdown(
            f"""
            <div class="md-container">
            {partial}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 7) Store & display final answer
    store.append(AIMessage(content=answer))
    st.chat_message("assistant", avatar="👩‍💻").markdown(answer)
