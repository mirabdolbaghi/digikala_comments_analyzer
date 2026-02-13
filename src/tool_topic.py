from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from parsivar import Normalizer
from os import environ

def comments_topics(comments):
    comments = clean_stopwords_from_comments(comments)
    persian_model = SentenceTransformer(environ["EMBEDDING_MODEL"])
    topic_model = BERTopic(
        embedding_model=persian_model,
        language="persian",
        calculate_probabilities=True,
        verbose=True
    )
    topic_model.fit_transform(comments)
    return topic_model.get_topics()

def get_persian_stop_words():
    normalizer = Normalizer()
    with open("stopwords.txt", "r", encoding="utf-8") as f:
        lines_set = {normalizer.normalize(line.strip()) for line in f if line.strip()}
        return lines_set
def clean_stopwords_from_comments(comments):
    normalizer = Normalizer()
    clean_comments=[]
    stop_words = get_persian_stop_words()
    for comment in comments:
        comment = normalizer.normalize(comment)
        words = comment.split()
        for i,word in enumerate(words):
            if word in stop_words:
                del words[i]
        if len(words) > 1:
            clean_comments.append(" ".join(words))
    return clean_comments
