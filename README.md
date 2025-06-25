
# 🗞️ Current Affairs RAG Pipeline

A Retrieval-Augmented Generation (RAG) system for exploring current affairs using extracted features and LLMs. This project integrates:

- **PostgreSQL** for structured storage  
- **Chroma** vector database for semantic retrieval  
- **Sentence Transformers** for dense embeddings  
- **Google Gemini (2.5 Flash)** for final response generation  
- Rich metadata including people, locations, dates, and sentiment

---

## 📁 Project Structure

```
Current_Affairs_RAG/
│
├── data/                   # Raw or preprocessed XML or news files
├── collect.py              # collects data from NEWS API and process it
├── db_utils.py             # Extracts and connects to PostgreSQL
├── features.py             # NER, sentiment, dates, etc.
├── prepare.py              # extract features and stores in Postgres
├── vectordb.py             # Embeds & stores documents in Chroma
├── rag.py                  # Main RAG retrieval and LLM generation
├── utils.py                # utility functions for working with JSON and XML
├── requirements.txt        # requirements
└── README.md               # You are here
```

---

## 🚀 Features

- Collects news data from News API and processing XML
- Stores news data and rich NLP features in **PostgreSQL**
- Embeds news articles using **MiniLM Sentence Transformers**
- Stores dense vectors using **Chroma Vector DB**
- Retrieves semantically relevant articles for a user query
- Uses **Google Gemini 2.5 Flash** API to generate answers
- Shows **document source titles** along with each answer

---

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Dependencies include:

- `langchain`
- `langchain-community`
- `sentence-transformers`
- `chromadb`
- `psycopg2`
- `google-generativeai`
- `tqdm`, `nltk`, `spacy` etc.

---

## 🧱 Step-by-Step Workflow

### 1. 🗃️ Data Preparation

Collects news data from News API, converts into XML

```bash
python collect.py
```

This will:
- collect news data from APIs
- convert them into XML
- extract raw content by using XPath

---


### 2. 🗃️ Feature Extraction

Extract features (NER, sentiment, dates) from raw news content and store them in PostgreSQL.

```bash
python prepare.py
```

This will:
- Parse XML current affairs articles
- Extract:
  - `People`, `Organizations`, `Locations`
  - `Events`, `Dates`, `Sentiment`
- Store results in a PostgreSQL schema:
  - `articles (id, title, content)`
  - `features (article_id, people, orgs, ...)`

---

### 3. 🧠 Embed & Store in Chroma Vector DB

```bash
python vectordb.py
```

This will:
- Fetch articles + features from PostgreSQL using `get_articles_and_features()`
- Convert them to LangChain `Document` objects
- Embed content using: `sentence-transformers/all-MiniLM-L6-v2`
- Store the vectors in persistent Chroma DB (`./chroma_rag/`)

> 💡 This step is **only needed once**. You don't need to re-run unless the data changes.

---

### 4. 🔍 Query with Retrieval-Augmented Generation (RAG)

```bash
python rag.py
```

This script:
- Loads your stored vector DB
- Retrieves top-k relevant documents based on your question
- Sends them + question as prompt to **Google Gemini 2.5 Flash**
- Displays:
  - 📝 Final LLM-generated answer
  - 📚 Titles of source documents used

Sample query:

```python
question = "How is Isreal's Econommy right now?"
```

Example output:

```
Answer:
Israel's economy is currently under significant strain due to multiple conflicts, with high military spending and labor shortages...

Sources:
- "Can Israel's economy withstand multiple conflicts?"
- "Israel's economy proves resilient in the face of multiple conflicts"
```

---

## 🧪 Google Gemini API Setup

Use Gemini 2.5 Flash via `google.generativeai`:

```python
from google import genai

client = genai.Client(api_key="YOUR_API_KEY")
response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Your prompt here"
)
```

---

## 🧠 Model Details

### Embeddings

| Component | Model |
|----------|--------|
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector DB | `Chroma` (stored locally) |

### LLM

| Component | Model |
|----------|--------|
| Generator | `gemini-2.5-flash` via `google.generativeai` |

---

## 📌 Environment Variables (optional)

If preferred, use `.env` to store secrets:

```env
GENAI_API=your_gemini_api_key
DB_NAME=your_db_name
...
```

---


## ✍️ Credits

Built By:
- Vimalaadithan Bharathi Sivakumar
- Ceren Özdel
- Mrityunjoy Bhattacharya

---


For queries or ideas, feel free to reach out!
