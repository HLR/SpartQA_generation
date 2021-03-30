
def change_words(text, rel_rand, shape_rand, size_rand, color_rand):
    
    text_f = size(color(shape(relation(text, rel_rand), shape_rand), color_rand), size_rand)

    
    return text_f

def change_words_ans(list_ans, rel_rand, shape_rand, size_rand, color_rand):
    for ind, word in enumerate(list_ans):
        if type(word) == str:
            list_ans[ind] = size(color(shape(relation_ans(word, rel_rand), shape_rand), color_rand), size_rand)
            
    
    return list_ans


def relation(text, rand):
    
    words = {'left': 'left side', 'right': 'right side', 'below': 'under', 'above': 'on the top of', 'near to': 'close to'}
    
    for ind, word in enumerate(words):
        if word in text and rand[ind]:
            text = text.replace(word, words[word])
            
    return text


def relation_ans(text, rand):
    
    words = {'left': 'left', 'right': 'right', 'below': 'under', 'above': 'top', 'near to': 'close to'}
    
    for ind, word in enumerate(words):
        if word in text and rand[ind]:
            text = text.replace(word, words[word])
            
    return text

def shape(text, rand):
    
    words = {'circle': 'oval', 'square': 'rectangle', 'triangle': 'diamond'}
    
    for ind, word in enumerate(words):
        if word in text and rand[ind]:
            text = text.replace(word, words[word])
            
    return text
    
def color(text, rand):
    
    words = {'blue': 'green', 'black': 'white', 'yellow': 'red'}
    
    for ind, word in enumerate(words):
        if word in text and rand[ind]:
            text = text.replace(word, words[word])
            
    return text

def size(text, rand):
    
    words = {'small': 'little', 'medium': 'midsize', 'big': 'large'}
    
    for ind, word in enumerate(words):
        if word in text and rand[ind]:
            text = text.replace(word, words[word])
            
    return text
