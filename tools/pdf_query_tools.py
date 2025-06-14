from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.agents import tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import pymupdf4llm


@tool
def faqs_budget_2025_pdf_query(query: str) -> str:
    """Returns a related answer from the "FAQs of the Budget 2025" PDF which has all the faqs of the new tax laws and rules of the budget 2025, using semantic search from input query"""

    # llm = ChatGroq(model=llm_model)
    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    try:
        db = FAISS.load_local(
            "db/faiss_index_faqs_budget_2025",
            embeddings_model,
            allow_dangerous_deserialization=True,
        )
    except:
        raw_text = pymupdf4llm.to_markdown("tools/data/faqs-budget-2025.pdf")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=200,
        )
        texts = text_splitter.split_text(raw_text)

        db = FAISS.from_texts(texts, embeddings_model)
        db.save_local("db/faiss_index_faqs_budget_2025")

    retriever = db.as_retriever(k=4)
    result = retriever.invoke(query)

    return result


@tool
def finance_bill_2025_pdf_query(query: str) -> str:
    """Returns a related answer from the "Finance Bill 2025" PDF which has all the new tax laws and rules of the budget 2025, using semantic search from input query"""

    # llm = ChatGroq(model=llm_model)
    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    try:
        db = FAISS.load_local(
            "db/faiss_index_finance_bill_2025",
            embeddings_model,
            allow_dangerous_deserialization=True,
        )
    except:
        raw_text = pymupdf4llm.to_markdown("tools/data/Finance_Bill_2025.pdf")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=200,
        )
        texts = text_splitter.split_text(raw_text)

        db = FAISS.from_texts(texts, embeddings_model)
        db.save_local("db/faiss_index_finance_bill_2025")

    retriever = db.as_retriever(k=3)
    result = retriever.invoke(query)

    return result
