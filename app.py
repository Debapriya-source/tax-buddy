import hashlib
import torch
import os


from langchain_core.messages import HumanMessage, AIMessage
from dotenv import dotenv_values
import streamlit as st
from agent import agent
from tools.query_enhancer import query_enhancer

# Prevent Streamlit's watcher from examining torch.classes
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

# Add sidebar for chat history management
with st.sidebar:
    st.header("Chat History")
    if st.button("Clear Chat History", type="secondary"):
        st.session_state.store = []
        st.rerun()

    # Show chat history count
    st.write(f"Messages: {len(st.session_state.store)}")

    # Show recent context indicator
    if len(st.session_state.store) > 0:
        st.info(
            "💡 The assistant can now reference previous conversation when you ask follow-up questions!"
        )

    # Option to download chat history
    if st.session_state.store:
        chat_history_text = ""
        for i, message in enumerate(st.session_state.store):
            role = "User" if message.type == "human" else "Assistant"
            chat_history_text += f"{role}: {message.content}\n\n"

        st.download_button(
            label="Download Chat History",
            data=chat_history_text,
            file_name="tax_buddy_chat_history.txt",
            mime="text/plain",
        )

# Render chat history
for message in st.session_state.store:
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
def get_cached_response(query_hash, query, _chat_history):
    """
    Get cached response for a query, or run the agent if not cached.
    Note: _chat_history is prefixed with _ to exclude it from hashing
    """
    answer, partial = agent(query, _chat_history)
    return answer, partial


# Initialize cached agent
cached_agent = get_agent()

if prompt := st.chat_input("What is your query?"):
    # Add user message to history immediately
    st.session_state.store.append(HumanMessage(content=prompt))

    # Display user message
    st.chat_message("user", avatar="🗨️").markdown(prompt)

    # Show thoughts for each step
    with st.status("Processing your query...", expanded=True) as status:
        st.write("🤔 Enhancing your query...")
        enhanced_queries = cached_query_enhancer(prompt)
        print(f"Enhanced Queries: {enhanced_queries}")

        st.write("🔍 Processing enhanced query...")

        final_user_query = (
            f"user_prompt: {prompt}\n\nenhanced_queries: {enhanced_queries}."
        )
        # Get chat history (excluding the current message)
        chat_history = st.session_state.store[:-1]  # Exclude the current user message

        # Cache responses - create hash without chat history to avoid cache misses
        query_hash = hashlib.md5(final_user_query.encode()).hexdigest()
        st.write("💭 Generating response...")

        # Pass chat history to the agent (it will create the lookup tool internally)
        answer, partial = get_cached_response(
            query_hash, final_user_query, chat_history
        )

        status.update(label="Response generated!", state="complete", expanded=False)

    # Limit chat history to 100 messages
    if len(st.session_state.store) >= 100:
        st.session_state.store = st.session_state.store[-100:]

    # Add AI response to history
    st.session_state.store.append(AIMessage(content=answer))

    # Show reasoning and response
    with st.expander("Reasoning", expanded=False):
        st.markdown(partial, unsafe_allow_html=True)
    # Display assistant response
    with st.chat_message("assistant", avatar="👩‍💻"):
        st.markdown(answer)
