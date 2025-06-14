# from langchain_core.messages import HumanMessage, AIMessage
# import os
# from dotenv import dotenv_values
# import streamlit as st
# from agent import agent
# from tools.query_enhancer import query_enhancer

# # ENVs = dotenv_values()

# try:
#     ENVs = dotenv_values(".env")  # for dev env
#     GROQ_API_KEY = ENVs["GROQ_API_KEY"]
# except:
#     ENVs = st.secrets  # for streamlit deployment
#     GROQ_API_KEY = ENVs["GROQ_API_KEY"]


# os.environ["GROQ_API_KEY"] = ENVs["GROQ_API_KEY"]
# os.environ["HUGGINGFACE_API_KEY"] = ENVs["HUGGINGFACE_API_KEY"]

# # create a Streamlit app

# # configure the layout
# st.set_page_config(
#     page_title="Tax Buddy👩‍💻 🗒️",
#     page_icon="🗒️",
#     layout="centered",
#     initial_sidebar_state="expanded",
# )

# st.title("Tax Buddy👩‍💻")
# # st.header("I am your legal chatbot assistant")
# initial_msg = """
#     #### Welcome!!!  I am your tax assistant chatbot👩‍💻
#     #### You can ask me any queries about the new tax regime of India
#     > NOTE: Currently I have only access to the FAQs of the budget 2025 and the Finance Bill 2025. So, I'll answer relevant queries only😇
#     """
# st.markdown(initial_msg)

# # very important step, if we dont use st.session_state then it will not store the history in streamlits browser session
# if "store" not in st.session_state:
#     st.session_state.store = []

# store = st.session_state.store

# for message in store:
#     if message.type == "ai":
#         avatar = "👩‍💻"
#     else:
#         avatar = "🗨️"
#     with st.chat_message(message.type, avatar=avatar):
#         st.markdown(message.content)


# # React to user input
# if prompt := st.chat_input("What is your query?"):
#     # Display user message in chat message container
#     st.chat_message("user", avatar="🗨️").markdown(prompt)
#     st.chat_message("👩‍💻").markdown("Thinking...")

#     enhanced_queries = query_enhancer(prompt)
#     print(f"enhanced_queries: {enhanced_queries}")
#     store.append(HumanMessage(content=f"prompt: {prompt}\n\nenhanced_queries: {enhanced_queries}"))
#     try:
#         response = AIMessage(content=agent(prompt))
#     except:
#         response = AIMessage(
#             content="Sorry, I am not able to answer your query due to high traffic (API Limit Exceeded)"
#         )
#     # response = AIMessage(content=agent(prompt))
#     store.append(response)

#     # Display assistant response in chat message container
#     st.chat_message("assistant", avatar="👩‍💻").markdown(response.content)
#####################################################################################################################################################################################################




# from langchain_core.messages import HumanMessage, AIMessage
# import os
# from dotenv import dotenv_values
# import streamlit as st
# from agent import agent
# from tools.query_enhancer import query_enhancer

# # Load environment variables
# try:
#     ENVs = dotenv_values(".env")  # for local dev
#     GROQ_API_KEY = ENVs["GROQ_API_KEY"]
# except Exception:
#     ENVs = st.secrets  # for Streamlit deployment
#     GROQ_API_KEY = ENVs["GROQ_API_KEY"]

# # Set API keys in OS env
# os.environ["GROQ_API_KEY"] = ENVs["GROQ_API_KEY"]
# os.environ["HUGGINGFACE_API_KEY"] = ENVs["HUGGINGFACE_API_KEY"]

# # Streamlit app configuration
# st.set_page_config(
#     page_title="Tax Buddy👩‍💻 🗒️",
#     page_icon="🗒️",
#     layout="centered",
#     initial_sidebar_state="expanded",
# )

# st.title("Tax Buddy👩‍💻")
# initial_msg = """
#     #### Welcome!!!  I am your tax assistant chatbot👩‍💻
#     #### You can ask me any queries about the new tax regime of India
#     > NOTE: Currently I have only access to the FAQs of the budget 2025 and the Finance Bill 2025. So, I'll answer relevant queries only😇
#     """
# st.markdown(initial_msg)

# # Initialize session history
# if "store" not in st.session_state:
#     st.session_state.store = []

# store = st.session_state.store

# # Render chat history
# for message in store:
#     avatar = "👩‍💻" if message.type == "ai" else "🗨️"
#     with st.chat_message(message.type, avatar=avatar):
#         st.markdown(message.content)

# # Handle new user input
# if prompt := st.chat_input("What is your query?"):
#     # Display user prompt
#     st.chat_message("user", avatar="🗨️").markdown(prompt)
#     # Show typing indicator
#     st.chat_message("assistant", avatar="👩‍💻").markdown("Thinking...")

#     # Enhance the query
#     enhanced_queries = query_enhancer(prompt)
#     print(f"enhanced_queries: {enhanced_queries}")

#     # Store the user message and enhanced queries
#     user_message = HumanMessage(content=f"prompt: {prompt}\n\n" +
#                                      f"enhanced_queries: {enhanced_queries}")
#     store.append(user_message)

#     # Call the agent with full conversation history for context
#     try:
#         response_text = agent(store)
#     except Exception:
#         response_text = "Sorry, I am not able to answer your query due to high traffic (API Limit Exceeded)"
#     response = AIMessage(content=response_text)

#     # Store and display the agent response
#     store.append(response)
#     st.chat_message("assistant", avatar="👩‍💻").markdown(response.content)

#========================================================================================



# from langchain_core.messages import HumanMessage, AIMessage
# import os
# from dotenv import dotenv_values
# import streamlit as st
# from agent import agent
# from tools.query_enhancer import query_enhancer
# import io
# import contextlib

# # Load environment variables
# try:
#     ENVs = dotenv_values(".env")  # for local dev
#     GROQ_API_KEY = ENVs["GROQ_API_KEY"]
# except Exception:
#     ENVs = st.secrets  # for Streamlit deployment
#     GROQ_API_KEY = ENVs["GROQ_API_KEY"]

# # Set API keys in OS env
# os.environ["GROQ_API_KEY"] = ENVs["GROQ_API_KEY"]
# os.environ["HUGGINGFACE_API_KEY"] = ENVs["HUGGINGFACE_API_KEY"]

# # Streamlit app configuration
# st.set_page_config(
#     page_title="Tax Buddy👩‍💻 🗒️",
#     page_icon="🗒️",
#     layout="centered",
#     initial_sidebar_state="expanded",
# )

# st.title("Tax Buddy👩‍💻")
# initial_msg = """
#     #### Welcome!!!  I am your tax assistant chatbot👩‍💻
#     #### You can ask me any queries about the new tax regime of India
#     > NOTE: Currently I have only access to the FAQs of the budget 2025 and the Finance Bill 2025. So, I'll answer relevant queries only😇
#     """
# st.markdown(initial_msg)

# # Initialize session history
# if "store" not in st.session_state:
#     st.session_state.store = []

# store = st.session_state.store

# # Render chat history
# for message in store:
#     avatar = "👩‍💻" if message.type == "ai" else "🗨️"
#     with st.chat_message(message.type, avatar=avatar):
#         st.markdown(message.content)

# # Handle new user input
# if prompt := st.chat_input("What is your query?"):
#     # Display user prompt
#     st.chat_message("user", avatar="🗨️").markdown(prompt)
#     # Show typing indicator
#     st.chat_message("assistant", avatar="👩‍💻").markdown("Thinking...")

#     # Enhance the query
#     enhanced_queries = query_enhancer(prompt)
#     print(f"enhanced_queries: {enhanced_queries}")

#     # Store the user message and enhanced queries
#     user_message = HumanMessage(content=f"prompt: {prompt}\n\n" +
#                                      f"enhanced_queries: {enhanced_queries}")
#     store.append(prompt)

#     # Capture thought process and agent response
#     buf = io.StringIO()
#     with contextlib.redirect_stdout(buf):
#         try:
#             response_text = agent(prompt)
#         except Exception:
#             response_text = "Sorry, I am not able to answer your query due to high traffic (API Limit Exceeded)"
#     thought_log = buf.getvalue()

#     # Store the assistant's final response
#     response = AIMessage(content=response_text)
#     store.append(response)

#     # Display the assistant's thought process in a collapsible expander
#     with st.expander("Assistant's thought process", expanded=False):
#         st.text(thought_log)

#     # Display assistant response
#     st.chat_message("assistant", avatar="👩‍💻").markdown(response_text)


#========================================================================================



import re
from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import dotenv_values
import streamlit as st
import streamlit.components.v1 as components
from agent import agent
from tools.query_enhancer import query_enhancer
import io
import contextlib

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
    page_title="Tax Buddy👩‍💻 🗒️",
    page_icon="🗒️",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Tax Buddy👩‍💻")
initial_msg = """
    #### Welcome!!!  I am your tax assistant chatbot👩‍💻
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

# Handle new user input
if prompt := st.chat_input("What is your query?"):
    # Display user prompt
    st.chat_message("user", avatar="🗨️").markdown(prompt)

    # Create a placeholder for the blinking indicator
    placeholder = st.empty()
    with placeholder.container():
        with st.chat_message("assistant", avatar="👩‍💻"):
            components.html(
                """
                <div style="font-weight:bold; font-size:16px;font-family:cursive; color:#555;">
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

    # Enhance the query
    enhanced_queries = query_enhancer(prompt)
    print(f"enhanced_queries: {enhanced_queries}")

    # Store the user message and enhanced queries
    user_message = HumanMessage(content=f"Please use proper quotations from the PDFs when crafting your answer. prompt: {prompt}\n\n" +
                                     f"enhanced_queries: {enhanced_queries}")
    store.append(HumanMessage(content=prompt))

    # Capture thought process and agent response
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            response_text = agent(prompt)
        except Exception:
            response_text = "Sorry, I am not able to answer your query due to high traffic (API Limit Exceeded)"
    thought_log = buf.getvalue()
    cleaned_thought_log = re.sub(r"\x1B\[[0-?]*[ -/]*[@-~]", "", thought_log) # Clean up the thought log

    # Store the assistant's final response
    response = AIMessage(content=response_text)
    store.append(response)

    # Remove the blinking indicator
    placeholder.empty()

    # Display the assistant's thought process in a collapsible expander
    with st.expander("Assistant's thought process", expanded=False):
        st.text(cleaned_thought_log)

    # Display assistant response
    st.chat_message("assistant", avatar="👩‍💻").markdown(response_text)
