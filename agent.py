import logging
import io
import contextlib
import re
import warnings

from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.messages import BaseMessage
from typing import List

from tools.react_prompt_template import get_prompt_template
from tools.pdf_query_tools import (
    faqs_budget_2025_pdf_query,
    finance_bill_2025_pdf_query,
)
from tools.web_search_query_tools import search_tax_websites
from tools.chat_history_tool import create_chat_history_tool


def fallback_chat(
    query: str, thoughts: str, fallback_model: str = "llama-3.3-70b-versatile"
) -> str:
    """Continue from partial thoughts on a cheaper/fallback model."""
    llm = ChatGroq(model=fallback_model, temperature=0.1)

    messages = [
        {"role": "system", "content": "You are a fallback tax assistant."},
        {"role": "system", "content": f"Original query: {query}"},
        {"role": "system", "content": f"Partial reasoning so far:\n{thoughts}"},
        {
            "role": "user",
            "content": "Based on the above, give a final answer with proper references(from the partial thoughts) and disclaimer.",
        },
    ]
    try:
        return llm.invoke(messages).content
    except Exception as err:
        try:
            llm_default = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)
            return llm_default.invoke(messages).content
        except Exception as err:
            logging.error(str(err))
        logging.error("Fallback model also failed", exc_info=True)
        return f"⚠️ Sorry, even the fallback failed: {err}"


def agent(query: str, chat_history: List[BaseMessage] = None) -> tuple[str, str]:
    warnings.filterwarnings("ignore", category=FutureWarning)

    # — Primary LLM & tools setup —
    llm = ChatGroq(model="deepseek-r1-distill-llama-70b")

    # Create tools including chat history lookup
    tools = [
        faqs_budget_2025_pdf_query,
        finance_bill_2025_pdf_query,
        search_tax_websites,
    ]

    # Add chat history tool if history exists
    if chat_history:
        chat_history_tool = create_chat_history_tool(chat_history)
        tools.append(chat_history_tool)

    prompt = get_prompt_template()
    react_agent = create_react_agent(llm, tools, prompt)

    cb_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    executor = AgentExecutor(
        name="tax-buddy-executor",
        agent=react_agent,
        tools=tools,
        return_intermediate_steps=True,
        verbose=True,
        handle_parsing_errors="pass",
        early_stopping_method="force",  # force returns a string
        max_iterations=6,  # Increased to allow for chat history lookup
        callback_manager=cb_manager,
    )

    # — Capture everything the agent prints —
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            instructions = """
                You are a tax assistant with access to tax documents and chat history.
                
                IMPORTANT: If the user's question seems to reference previous conversation 
                (uses words like "that", "it", "previous", "earlier", "above", or asks follow-up questions),
                use the chat_history_lookup tool to get context before answering.
                
                Examples of when to use chat_history_lookup:
                - "Tell me more about that"
                - "What about the previous question?"
                - "Can you explain it further?"
                - "What did you say about deductions?"
                - Any question that lacks clear context
                
                Instructions:
                - Provide proper facts and references (section numbers, specific lines, URLs) from PDFs/websites
                - Add a proper disclaimer in the final response
                - If using chat history, acknowledge the previous context in your response
                """
            result = executor.invoke({"input": query, "instructions": instructions})
        except Exception:
            logging.exception("AgentExecutor.invoke failed")
            result = {"output": "", "intermediate_steps": []}

    trace = buf.getvalue()
    output = (result.get("output") or "").strip()

    # — Clean out parser-error noise from the raw trace —
    clean_lines = [
        line
        for line in trace.splitlines()
        if not line.lstrip().startswith("Invalid Format:")
    ]

    # — Keep the last 25 meaningful lines as partial reasoning —
    if clean_lines:
        partial = "\n".join(clean_lines[-25:])
    else:
        partial = trace or "No partial reasoning available."

    # — Decide final answer, or fallback if no output / early stop —
    if not output or any(
        phrase in output.lower()
        for phrase in ("stopped due to iteration limit", "stopped due to time limit")
    ):
        final = fallback_chat(
            query=query, thoughts=partial, fallback_model="qwen/qwen3-32b"
        )
    else:
        final = output

    # 1) Compile a pattern to capture anything between <think> and </think>
    think_pat = re.compile(r"<think>(.*?)</think>", re.DOTALL)

    # 2) Extract all thought‐blocks into a list
    m = think_pat.search(final)
    thoughts = m.group(1).strip() if m else ""

    # 3) Strip out those blocks (tags+content) from the raw text
    clean_text = think_pat.sub("", final)

    return clean_text, partial + thoughts
