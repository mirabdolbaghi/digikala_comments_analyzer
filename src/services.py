from db import CommentDB
from tool_sentiment import get_sentiment,sentiment_score_board
from tool_topic import comments_topics
from tool_ner import get_ner_comments
from tool_similarity import similar_sentences
from llm import analyze_dissatisfactionـcomment
from crawler import digikala_category_comments 
def crawl_digikala_comments(category):
    comments = digikala_category_comments(category)
    db = CommentDB()
    db.delete_all_comment()
    db.create_comments_batch(comments)
def analyze_negative_comments():
    db = CommentDB()
    all_comments = db.get_all_comments()
    negative_comments = get_sentiment([c[0] for c in all_comments],"not_recommended")
    # reducing comment because of llm context length 
    negative_comments = negative_comments[:10]
    return analyze_dissatisfactionـcomment([c[0] for c in negative_comments])

def sentiment_analyze_comments():
    db = CommentDB()
    all_comments = db.get_all_comments()
    comments_sentiments = get_sentiment([c[0] for c in all_comments])
    return sentiment_score_board(comments_sentiments)
    
def comments_topic_modeling():
    db = CommentDB()
    all_comments = db.get_all_comments()
    topics = comments_topics([c[0] for c in all_comments])
    return topics

def comments_ner():
    db = CommentDB()
    all_comments = db.get_all_comments()
    ners = get_ner_comments([c[0] for c in all_comments])
    return ners

def find_similar_comments():
    db = CommentDB()
    all_comments = db.get_all_comments()[:100]
    similar_comments = similar_sentences([c[0] for c in all_comments])
    return similar_comments
