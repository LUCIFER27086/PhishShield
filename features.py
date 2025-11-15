def analyze_url(url):
    """
    Extract structuralnad lexical features from a url
    (Suspicious words, IP-based URL, domain analysis, etc.)

    """
    features={}
    return features

def analyze_email(text):
    """
    extract lingusitic and sentiment based features from email text.
    (Like urgency words, sentiment score, link count and stuff)

    """
    features = {}
    return features

def calculate_score(features):
    """
    compute phishing probability scorebased on the extracted features
    """
    score = 0
    verdict = "Pending"
    return score, verdict

def visualize_result(features, score, verdict):
    """
    Generate visual graph and save it under screenshots/.
    """
    pass