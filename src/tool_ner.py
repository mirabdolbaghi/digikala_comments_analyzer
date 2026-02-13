from transformers import AutoTokenizer
from transformers import AutoModelForTokenClassification  # for pytorch
from transformers import pipeline
from utility import split_token_to_limit
from os import environ

# model_name_or_path = "HooshvareLab/bert-base-parsbert-ner-uncased"  

# tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)

# model = AutoModelForTokenClassification.from_pretrained(model_name_or_path)  # Pytorch
# # model = TFAutoModelForTokenClassification.from_pretrained(model_name_or_path)  # Tensorflow

# nlp = pipeline("ner", model=model, tokenizer=tokenizer)
# example = "در سال ۲۰۱۳ درگذشت و آندرتیکر و کین برای او مراسم یادبود گرفتند."

# ner_results = nlp([example])
# print(ner_results)
def get_ner_analyzer():
    # return pipeline("ner", model=model_name_or_path)
    tokenizer = AutoTokenizer.from_pretrained(environ["NER_MODEL"])
    model = AutoModelForTokenClassification.from_pretrained(environ["NER_MODEL"])  # Pytorch
    return pipeline("ner", model=model, tokenizer=tokenizer)
def get_tokenizer():
    return AutoTokenizer.from_pretrained(environ["NER_MODEL"])


def get_ner_comments(comments):
    tokenizer = get_tokenizer()
    ner_analyzer = get_ner_analyzer()
    tokenizer.model_max_length = 512
    comments_ners= {}
    for comment in comments:
        tokens = tokenizer.tokenize(comment)
        if len(tokens)> tokenizer.model_max_length:
            split_comment = split_token_to_limit(comment,tokenizer)
            for comment in split_comment:
                ner_result = ner_analyzer(comment)
                for ner in ner_result:
                    if ner['entity'] not in comments_ners:
                        comments_ners[ner['entity']] = {ner['word']}
                    else:
                        comments_ners[ner['entity']].add(ner['word'])
        else:
            ner_result = ner_analyzer(comment)
            for ner in ner_result:
                for ner in ner_result:
                    if ner['entity'] not in comments_ners:
                        comments_ners[ner['entity']] = {ner['word']}
                    else:
                        comments_ners[ner['entity']].add(ner['word'])
    return comments_ners
