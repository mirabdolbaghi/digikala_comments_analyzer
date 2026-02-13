from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
from utility import split_token_to_limit
import numpy as np
from os import environ

def get_embeddeing_model():
    return SentenceTransformer(environ["EMBEDDING_MODEL"])
# MAX_TOKENS = model.max_seq_length

# 1. Load a pretrained Sentence Transformer model
def get_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained(environ["EMBEDDING_MODEL"])
    tokenizer.model_max_length = 512
    return tokenizer

def get_embeddings(sentences):
    model = get_embeddeing_model()
    tokenizer = get_tokenizer()
    embeddings = []
    for sentence in sentences:
        tokens = tokenizer.tokenize(sentence)
        if len(tokens)> tokenizer.model_max_length:
            split_sentence = split_token_to_limit(sentence,tokenizer)
            sentence_embeddings = model.encode(split_sentence)
            mean_embedding = np.array(sentence_embeddings).transpose().mean(axis=1)
            embeddings.append(mean_embedding)
        else:
            embeddings.append(model.encode(sentence))

    return embeddings
def similar_sentences(sentences,min_similrity = 0.8):
    model = get_embeddeing_model()
    embeddings = get_embeddings(sentences)
    similarities = model.similarity(embeddings, embeddings)
    similar_sentences=[]
    for i,sim_list in enumerate(similarities):
        for j,similarity in enumerate(sim_list):
            if i != j and similarity > min_similrity:
                similar_sentences.append((sentences[i],sentences[j],similarity))
    return similar_sentences
