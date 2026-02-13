def split_token_to_limit(comment,tokenizer):
    clean_comments = []
    words = comment.split()
    words_halflength = int(len(words)/2)

    split_words = [words[:words_halflength],words[words_halflength:]]
    for words in split_words:
        c =" ".join(words)
        if len(tokenizer.tokenize(c)) > tokenizer.model_max_length:
            clean_comments += split_token_to_limit(c,tokenizer)
        else: 
            clean_comments.append(c)
    return clean_comments