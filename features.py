import spacy 
import re
from textblob import TextBlob
from collections import Counter

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


def extract_features(article_text):
    """
    Extracts linguistic and semantic features from a news article using spaCy and TextBlob.

    Features extracted:
        - Named entities: people, organizations, locations, dates, geopolitical groups
        - Conflict-related event sentences
        - Overall sentiment polarity (float)

    Args:
        article_text (str): The full article text to analyze.

    Returns:
        dict: A dictionary containing extracted features:
    """
    doc = nlp(article_text)
    # Named Entities
    people = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    organizations = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    locations = [ent.text for ent in doc.ents if ent.label_ in ("GPE", "LOC")]
    dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    geopolitical_groups = [ent.text for ent in doc.ents if ent.label_ == ("NORP", "ORG")] 
    
    # Events (approximate by extracting sentences with conflict verbs)
    conflict_verbs = ["attack", "bombard", "protest", "retreat", "occupy", "strike", "evacuate"]
    event_sentences = [sent.text for sent in doc.sents if any(v in sent.text.lower() for v in conflict_verbs)]
    
    # Sentiment (overall article sentiment polarity)
    sentiment = TextBlob(article_text).sentiment.polarity
    
    return {
        "people": list(set(people)),
        "organizations": list(set(organizations)),
        "locations": list(set(locations)),
        "dates": list(set(dates)),
        "geopolitical_groups": list(set(geopolitical_groups)),
        "event_sentences": event_sentences,
        "sentiment": sentiment,
    }



def preprocess_features(features):
    """
    Cleans and standardizes the extracted features for database insertion.
    
    Args:
        features (dict): Raw extracted feature dictionary from extract_features.

    Returns:
        dict: Cleaned and preprocessed features in the same structure.
    """
    def clean_list(x):
        return list(set(filter(None, x)))  # Remove duplicates and empty strings

    return {
        "people": clean_list(features.get("people", [])),
        "organizations": clean_list(features.get("organizations", [])),
        "locations": clean_list(features.get("locations", [])),
        "dates": clean_list(features.get("dates", [])),
        "geopolitical_groups": clean_list(features.get("geopolitical_groups", [])),
        "event_sentences": clean_list(features.get("event_sentences", [])),
        "sentiment": features.get("sentiment", 0.0)
    }
