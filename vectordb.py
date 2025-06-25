import psycopg2
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from db_utils import get_articles_and_features

# Convert to LangChain Documents
def convert_to_documents(records):
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

# 3. Store in Chroma Vector Store
def store_documents(docs, persist_dir="./chroma_rag"):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(docs, embedding=embeddings, persist_directory=persist_dir)
    vectorstore.persist()
    return vectorstore

# 4. Retrieve
def query_vectorstore(vectorstore, question):
    retriever = vectorstore.as_retriever()
    docs = retriever.invoke(question)
    return docs


def load_vectorstore(persist_dir="./chroma_rag"):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    return vectorstore


if __name__ == "__main__":
    articles = get_articles_and_features()
    print(articles)
    documents = convert_to_documents(articles)
    print("\n\n", documents)
    vectorstore = store_documents(documents)

    question = "What recent political events happened in Europe?"
    retrieved_docs = query_vectorstore(vectorstore, question)

    for i, doc in enumerate(retrieved_docs):
        print(f"\n--- Document {i+1} ---")
        print("Title:", doc.metadata["title"])
        print("Content Snippet:", doc.page_content[:500])
