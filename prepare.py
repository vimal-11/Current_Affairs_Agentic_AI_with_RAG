from utils import parse_xml, extract_article_content_from_xml
from features import extract_features, preprocess_features
import db_utils

XML_PATH = "data/article.xml"

articles = parse_xml(XML_PATH)

# create tables
# db_utils.create_table()
# db_utils.create_table_features()

for article in articles:
    # Insert article and get its ID
    try:
        article_id = db_utils.insert_article(article)
    except Exception as e:
        print(f"Error occurred: {e}")
    raw_features = extract_features(str(article["full_content"]))
    features = preprocess_features(raw_features)
    if all(len(features[field]) == 0 for field in [
        "people", "organizations", "locations", "dates", "geopolitical_groups", "event_sentences"
    ]) and features["sentiment"] == 0.0:
        continue  # skip irrelevant entries

    # Insert features into DB
    db_utils.insert_feature(article_id, features)

