from langchain_groq import ChatGroq


def query_enhancer(query: str) -> str:
    """Enhances the query by adding more context and information"""
    llm = ChatGroq(model="llama3-8b-8192")
    prompt = f"""   
    You are a helpful assistant that enhances the query by adding more context, information and NER tags in a proper format.
    The query is: {query}
    The response should be in the following format:
    [ enhanced_query_1, NER_tags_1 ], [ enhanced_query_2, NER_tags_2 ], [ enhanced_query_3, NER_tags_3 ]
    No extra text, just the response in the above format.
    """
    return llm.invoke(prompt).content


if __name__ == "__main__":
    print(query_enhancer("What is the new tax regime of India?"))
