def separate_aspect(sent,aspects,count_aspects):
    if sent['aspect'] in aspects:
        count_aspects[sent['aspect']] += 1.0
    else:
        count_aspects[sent['aspect']] = 1.0
        aspects[sent['aspect']] = 0.0
#def calculation(aspects,all_sent,count_aspects):
#    for sent in all_sent:
#        dic_sent = eval(sent)
#        if dic_sent['polarity'] == 'positive':
#            aspects[dic_sent['aspect']] += float(dic_sent['polarity_confidence']) * float(dic_sent['aspect_confidence'])
#        elif dic_sent['polarity'] == 'negative':
#            aspects[dic_sent['aspect']] += (1.0 - float(dic_sent['polarity_confidence'])) * float(dic_sent['aspect_confidence'])
#    for aspect in aspects:
#        aspects[aspect] = aspects[aspect] / count_aspects[aspect]
def calculation_v2(aspects,all_sent,count_aspects):
    for sent in all_sent:
        dic_sent = eval(sent)
        if dic_sent['polarity'] == 'positive':
            aspects[dic_sent['aspect']] += float(dic_sent['polarity_confidence'])
        elif dic_sent['polarity'] == 'negative':
            aspects[dic_sent['aspect']] += (1.0 - float(dic_sent['polarity_confidence']))
    for aspect in aspects:
        aspects[aspect] = aspects[aspect] / count_aspects[aspect]
with open('sentiment.txt', 'rb') as f_sent:
    aspects = {}
    count_aspects = {}
    all_sent = f_sent.read().splitlines()
    for sent in all_sent:
        separate_aspect(eval(sent),aspects,count_aspects)
        test = eval(sent)
    calculation_v2(aspects,all_sent,count_aspects)
print(aspects)
print(count_aspects)
