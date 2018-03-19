aspects = {}
count_aspects = {}
def separate_aspect(sent):
    if sent['aspect'] in aspects:
        count_aspects[sent['aspect']] += 1
    else:
        count_aspects[sent['aspect']] = 1
        aspects[sent['aspect']] = 0

with open('sentiment.txt', 'rb') as f_sent:
    all_sent = f_sent.read().splitlines()
    for sent in all_sent:
        separate_aspect(eval(sent))
