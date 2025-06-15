import hashlib
import torch
import os


from langchain_core.messages import HumanMessage, AIMessage
from dotenv import dotenv_values
import streamlit as st
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


# Cached functions at the top
@st.cache_resource
def get_agent():
    return agent


@st.cache_data(ttl=3600, show_spinner=False)
def cached_query_enhancer(prompt):
    return query_enhancer(prompt)


@st.cache_data(ttl=1800, show_spinner=False)
def get_cached_response(query_hash, query):
    """
    Get cached response for a query, or run the agent if not cached.
    """
    answer, partial = agent(query)
    return answer, partial


# Initialize cached agent
cached_agent = get_agent()


if prompt := st.chat_input("What is your query?"):
    st.chat_message("user", avatar="🗨️").markdown(prompt)

    # Show thoughts for each step
    st.write("🤔 Enhancing your query...")
    enhanced_queries = cached_query_enhancer(prompt)
    print(f"Enhanced Queries: {enhanced_queries}")

    st.write("🔍 Processing enhanced query...")
    final_user_query = f"user_prompt: {prompt}\n\nenhanced_queries: {enhanced_queries}."

    # Cache responses
    query_hash = hashlib.md5(final_user_query.encode()).hexdigest()
    st.write("💭 Generating response...")
    answer, partial = get_cached_response(query_hash, final_user_query)
    # Manage history size
    if len(store) >= 20:
        store = store[-18:]

    store.append(HumanMessage(content=prompt))

    store.append(AIMessage(content=answer))

    # Show reasoning and response
    with st.expander("Reasoning", expanded=False):
        st.markdown(partial, unsafe_allow_html=True)

    st.chat_message("assistant", avatar="👩‍💻").markdown(answer)
