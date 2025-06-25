from google import genai
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from vectordb import *
import os

# Configure Gemini
GENAI_API = os.getenv("GENAI_API")
client = genai.Client(api_key=GENAI_API)


# RAG 
def ask_with_rag(vectorstore, question):
    # retreive the docs from vector db
    retrieved_docs = query_vectorstore(vectorstore, question)
    # Build context with titles
    context_blocks = []
    titles = []
    for doc in retrieved_docs:
        title = doc.metadata.get("title", "Unknown Title")
        content = doc.page_content
        context_blocks.append(f"Title: {title}\nContent:\n{content}")
        titles.append(title)
    
    context = "\n\n---\n\n".join(context_blocks)
    
    prompt = (
        f"Use the following news context to answer the question. "
        f"If the answer is not found, say you don't know.\n\n"
        f"{context}\n\n"
        f"Question: {question}\n\n"
        f"Answer:"
    )
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text, titles



if __name__ == "__main__":
    # load the vector db
    vectorstore = load_vectorstore()

    question = "How is Isreal's Econommy right now?"
    answer, sources = ask_with_rag(vectorstore, question)

    print("\nGemini's Answer:\n", answer)
    print("\nSources:")
    for i, title in enumerate(sources, 1):
        print(f"{i}. {title}")
