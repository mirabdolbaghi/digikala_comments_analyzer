from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline, BertForTokenClassification
from utility import split_token_to_limit
from os import environ

def get_sentiment_analyzer():
    return pipeline("sentiment-analysis", model=environ["SENTIMENT_MODEL"])
def get_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained(environ["SENTIMENT_MODEL"])
    tokenizer.model_max_length = 512
    return tokenizer


def get_sentiment_large_comment(comments,polarity):
    tokenizer = get_tokenizer()
    sentiment_analyzer = get_sentiment_analyzer()
    comments_sentiments= []
    for i,comment in enumerate(comments):
        tokens = tokenizer.tokenize(comment)
        if len(tokens)> tokenizer.model_max_length:
            split_comment = split_token_to_limit(comment,tokenizer)
            sent_result = sentiment_analyzer(split_comment)
            labels = {}
            for sent in sent_result:
                if sent['label'] not in labels:
                    labels[sent['label']]={
                        "label":sent['label'],
                        "count":1,
                        "score":sent['score']
                    }
                else:
                    labels[sent['label']]["count"]+=1
                    if labels[sent['label']]["score"] < sent['score']:
                        labels[sent['label']]["score"] = sent['score']
            labels = list(labels.values())
            if len(labels) > 1:
                labels = sorted(labels, key = lambda x: (x["count"], x["score"]), reverse = True)
            if polarity == "all":
                comments_sentiments.append((comment,labels[0]['label'],labels[0]['score']))
            elif polarity == labels[0]['label']:
                comments_sentiments.append((comment,labels[0]['label'],labels[0]['score']))
            del comments[i]
    return comments, comments_sentiments
def get_sentiment(comments,polarity="all"):   
    sentiment_analyzer = get_sentiment_analyzer()
    comments, comments_sentiments = get_sentiment_large_comment(comments,polarity)
    sent_result = sentiment_analyzer(comments)
    
    for sent, comment in zip(sent_result, comments):
        if polarity == "all":
            comments_sentiments.append((comment,sent['label'],sent['score']))
        elif polarity == sent['label']:
            comments_sentiments.append((comment,sent['label'],sent['score']))
    return comments_sentiments


def sentiment_score_board(comments_sentiments):
    board = {}
    for sentiment in comments_sentiments:
        if sentiment[1] not in board:
            board[sentiment[1]] = {
                "scores":[sentiment[2]]
            }
        else:
            board[sentiment[1]]["scores"].append(sentiment[2])
    response= []
    for label in board:
        response.append({
            "label":label,
            "count":len(board[label]["scores"]),
            "average score":sum(board[label]["scores"])/len(board[label]["scores"])
        })
    return response