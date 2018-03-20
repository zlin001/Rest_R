import numpy
def separate_aspect(sent,aspects_all,count_aspects_all):
    if sent['aspect'] in aspects_all:
        count_aspects_all[sent['aspect']] += 1.0
    else:
        count_aspects_all[sent['aspect']] = 1.0
        aspects_all[sent['aspect']] = 0.0
def separate_aspect_with_threshold(sent,aspects_threshold,aspects_filter,count_aspects_filter):
    if sent['aspect_confidence'] >= aspects_threshold[sent['aspect']]:
        if sent['aspect'] in aspects_filter:
            count_aspects_filter[sent['aspect']] += 1.0
        else:
            count_aspects_filter[sent['aspect']] = 1.0
            aspects_filter[sent['aspect']] = 0.0
def calculation_filter_with_threshold(aspects_threshold,aspects_filter,all_sent,count_aspects_filter):
    for sent in all_sent:
        dic_sent = eval(sent)
        if dic_sent['aspect_confidence'] >= aspects_threshold[dic_sent['aspect']]:
            if dic_sent['polarity'] == 'positive':
                aspects_filter[dic_sent['aspect']] += float(dic_sent['polarity_confidence'])
            elif dic_sent['polarity'] == 'negative':
                aspects_filter[dic_sent['aspect']] += (1.0 - float(dic_sent['polarity_confidence']))
    for aspect in aspects_filter:
        aspects_filter[aspect] = aspects_filter[aspect] / count_aspects_filter[aspect]
def calculation_threshold_aspect(aspects,all_sent,count_aspects):
    for sent in all_sent:
        dic_sent = eval(sent)
        aspects[dic_sent['aspect']] += float(dic_sent['aspect_confidence'])
    for aspect in aspects:
        aspects[aspect] = aspects[aspect] / count_aspects[aspect]
with open('sentiment.txt', 'rb') as f_sent:
    aspects_threshold = {}
    count_aspects_all = {}
    aspects_filter = {}
    count_aspects_filter = {}
    all_sent = f_sent.read().splitlines()
    for sent in all_sent:
        separate_aspect(eval(sent),aspects_threshold,count_aspects_all)
    calculation_threshold_aspect(aspects_threshold,all_sent,count_aspects_all)
    for sent in all_sent:
        separate_aspect_with_threshold(eval(sent),aspects_threshold,aspects_filter,count_aspects_filter)
    calculation_filter_with_threshold(aspects_threshold,aspects_filter,all_sent,count_aspects_filter)
print(aspects_filter)
