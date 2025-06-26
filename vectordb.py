import psycopg2
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from db_utils import get_articles_and_features


# Convert to LangChain Documents
def convert_to_documents(records):
    """
    Converts database records into LangChain Document objects.

    Args:
        records (list of tuples): Each record should contain:
            (article_id, title, content, people, orgs, locs, dates, groups, events, sentiment)

    Returns:
        list[Document]: List of LangChain Documents with content and metadata for vectorization.
    """
    docs = []
    for row in records:
        article_id, title, content, people, orgs, locs, dates, groups, events, sentiment = row
        metadata = {
            "title": title,
            "people": ", ".join(people) if people else "",
            "organizations": ", ".join(orgs) if orgs else "",
            "locations": ", ".join(locs) if locs else "",
            "dates": ", ".join(dates) if dates else "",
            "geopolitical_groups": ", ".join(groups) if groups else "",
            "sentiment": sentiment if sentiment is not None else "",
        }
        docs.append(Document(page_content=content, metadata=metadata))
    return docs



#  Store in Chroma Vector Store
def store_documents(docs, persist_dir="./chroma_rag"):
    """
    Stores LangChain documents in a Chroma vector database using sentence embeddings.

    Args:
        docs (list[Document]): List of LangChain Documents to store.
        persist_dir (str): Directory path to persist the vector DB.

    Returns:
        Chroma: The initialized and persisted vector store.
    """
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(docs, embedding=embeddings, persist_directory=persist_dir)
    vectorstore.persist()
    return vectorstore



#  Retrieve
def query_vectorstore(vectorstore, question):
    """
    Retrieves relevant documents from the vector store based on the user's question.

    Args:
        vectorstore (Chroma): A loaded or stored Chroma vector database.
        question (str): The natural language query.

    Returns:
        list[Document]: Retrieved documents relevant to the query.
    """
    retriever = vectorstore.as_retriever()
    docs = retriever.invoke(question)
    return docs



def load_vectorstore(persist_dir="./chroma_rag"):
    """
    Loads a persisted Chroma vector store from the specified directory.

    Args:
        persist_dir (str): Directory where the vector store was saved.

    Returns:
        Chroma: The loaded vector database instance.
    """
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    return vectorstore



if __name__ == "__main__":
    articles = get_articles_and_features()
    documents = convert_to_documents(articles)
    vectorstore = store_documents(documents)

    question = "What recent political events happened in Europe?"
    retrieved_docs = query_vectorstore(vectorstore, question)

    for i, doc in enumerate(retrieved_docs):
        print(f"\n--- Document {i+1} ---")
        print("Title:", doc.metadata["title"])
        print("Content Snippet:", doc.page_content[:500])
