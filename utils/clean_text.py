# -*- coding: utf-8 -*-

import nltk

def split_paragraphs(paragraphs, max_words=1850):
    """Split paragraphs longer than `max_words` words into multiple paragraphs"""
    split_paragraphs = []
    for paragraph in paragraphs:
        words = paragraph.split(' ')
        if len(words) > max_words:
            print("Very long pragraphs detected. Splitting it into two seperate paragraphs.")
            sentences = nltk.tokenize.sent_tokenize(paragraph)
            half = len(sentences) // 2
            split_paragraphs.append(' '.join(sentences[:half]))
            split_paragraphs.append(' '.join(sentences[half:]))
        else:
            split_paragraphs.append(paragraph)
    return split_paragraphs

# print(split_paragraphs(paragraphs, max_words=1850))