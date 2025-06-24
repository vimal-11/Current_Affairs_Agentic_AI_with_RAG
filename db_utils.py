import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

# === CONFIG ===
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
XML_PATH = "data/article.xml"  


# === CONNECT TO DATABASE ===
def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    

# === CREATE TABLE IF NOT EXISTS ===
def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id SERIAL PRIMARY KEY,
            title TEXT,
            author TEXT,
            description TEXT,
            source_name TEXT,
            published_at TIMESTAMP,
            url TEXT UNIQUE,
            full_content TEXT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Table 'articles' is created successfully.")


def create_table_features():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS features (
            id SERIAL PRIMARY KEY,
            article_id INTEGER UNIQUE REFERENCES articles(id) ON DELETE CASCADE,
            people TEXT[],
            organizations TEXT[],
            locations TEXT[],
            dates TEXT[],
            geopolitical_groups TEXT[],
            event_sentences TEXT[],
            sentiment REAL
        );
    ''')
    conn.commit()
    conn.commit()
    conn.close()
    print("Table 'features' is created successfully.")
    

def insert_article(data):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO articles (title, author, description, source_name, published_at, url, full_content)
            VALUES (%s, %s, %s, %s, %s, %s, %s) 
            ON CONFLICT (url) DO NOTHING
            RETURNING id;
        """, (
            data["title"], data["author"], data["description"], data["source_name"],
            data["published_at"], data["url"], data["full_content"]
        ))
        result = cur.fetchone()
        if result:
            article_id = result[0]
        else:
            # Get the existing article's ID if conflict occurred
            cur.execute("SELECT id FROM articles WHERE url = %s", (data["url"],))
            article_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return article_id
    except Exception as e:
        print(f"Error inserting article: {e}")
        conn.rollback()
        return None
        
        

def read_articles():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    cur.close()
    conn.close()
    return articles


def update_article(article_id, updated_data):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE articles
        SET title = %s, author = %s, description = %s, source_name = %s,
            published_at = %s, url = %s, full_content = %s
        WHERE id = %s
    """, (
        updated_data["title"], updated_data["author"], updated_data["description"],
        updated_data["source_name"], updated_data["published_at"],
        updated_data["url"], updated_data["full_content"], article_id
    ))
    conn.commit()
    cur.close()
    conn.close()


def delete_article(article_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM articles WHERE id = %s", (article_id,))
    conn.commit()
    cur.close()
    conn.close()



def insert_feature(article_id, data):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO features (
            article_id, people, organizations, locations, dates,
            geopolitical_groups, event_sentences, sentiment
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (article_id) DO NOTHING;
    """, (
        article_id,
        data["people"],
        data["organizations"],
        data["locations"],
        data["dates"],
        data["geopolitical_groups"],
        data["event_sentences"],
        data["sentiment"]
    ))
    conn.commit()
    cur.close()
    conn.close()


def read_features():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM features")
    features = cur.fetchall()
    cur.close()
    conn.close()
    return features


def update_feature(feature_id, data):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE features
        SET people = %s,
            organizations = %s,
            locations = %s,
            dates = %s,
            geopolitical_groups = %s,
            event_sentences = %s,
            sentiment = %s
        WHERE id = %s
    """, (
        data["people"],
        data["organizations"],
        data["locations"],
        data["dates"],
        data["geopolitical_groups"],
        data["event_sentences"],
        data["sentiment"],
        feature_id
    ))
    conn.commit()
    cur.close()
    conn.close()


def delete_feature(feature_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM features WHERE id = %s", (feature_id,))
    conn.commit()
    cur.close()
    conn.close()




def search_articles(query):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.title, a.full_content, f.people, f.organizations
        FROM articles a
        JOIN features f ON a.id = f.article_id
        WHERE a.full_content ILIKE %s OR f.people @> %s;
    """, (f"%{query}%", [query]))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
