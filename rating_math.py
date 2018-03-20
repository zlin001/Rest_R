import numpy
# The idea is only accepted the review who's aspect_confidence is higher than threshold(avg of all), then
# we add the polarity_confidence for positive, 1 - polarity_confidence for negative
# Note:
# sent is one sentiment
# all sent is all sentiment
# aspects_all (for all aspect) = aspects_threshold (after calculation)
# count_aspects_all is the total number for each group with out threshold
# aspects_filter is the dictionary after we did the threshold
# count_aspects_filter is the dictionary after we did the threshold
# This function is use to separate aspect in different group of dict
def separate_aspect(sent,aspects_all,count_aspects_all):
    # check the condition if the aspect already existed in the aspects_all(this is the aspect with out threshold)
    if sent['aspect'] in aspects_all:
        # when it found, we add the amount of count (how many review is related to this group)
        count_aspects_all[sent['aspect']] += 1.0
    else:
        # if not, we initialize them.
        count_aspects_all[sent['aspect']] = 1.0
        aspects_all[sent['aspect']] = 0.0
#this function is going to separate the aspects with threshold
def separate_aspect_with_threshold(sent,aspects_threshold,aspects_filter,count_aspects_filter):
    # this is similar to separate_aspect but it has condition which it must higher than threshold, in order to add into dic
    if sent['aspect_confidence'] >= aspects_threshold[sent['aspect']]:
        if sent['aspect'] in aspects_filter:
            count_aspects_filter[sent['aspect']] += 1.0
        else:
            count_aspects_filter[sent['aspect']] = 1.0
            aspects_filter[sent['aspect']] = 0.0
# this function will calculation the rating after we filter out the review that below threshold
def calculation_filter_with_threshold(aspects_threshold,aspects_filter,all_sent,count_aspects_filter):
    # go over all each sent
    for sent in all_sent:
        # we need to convert to dictionary
        dic_sent = eval(sent)
        # check the threshold
        if dic_sent['aspect_confidence'] >= aspects_threshold[dic_sent['aspect']]:
            # if postive
            if dic_sent['polarity'] == 'positive':
                # we add polarity_confidence to coressponding aspect
                aspects_filter[dic_sent['aspect']] += float(dic_sent['polarity_confidence'])
            # if negative
            elif dic_sent['polarity'] == 'negative':
                # we add 1 - polarity_confidence (this mean the postive) to coressponding aspect
                aspects_filter[dic_sent['aspect']] += (1.0 - float(dic_sent['polarity_confidence']))
    # we avergae them with count_aspects_filter for each aspect
    for aspect in aspects_filter:
        aspects_filter[aspect] = aspects_filter[aspect] / count_aspects_filter[aspect]
# this is function to calculation of aspect_confidence, to find the threshold
def calculation_threshold_aspect(aspects,all_sent,count_aspects):
    # go over all sent
    for sent in all_sent:
        # convert the dictionary
        dic_sent = eval(sent)
        # add aspect_confidence to coressponding aspect
        aspects[dic_sent['aspect']] += float(dic_sent['aspect_confidence'])
    # we average them, which it is our threshold
    for aspect in aspects:
        aspects[aspect] = aspects[aspect] / count_aspects[aspect]
def convert_deci_star(aspects_filter,aspects_star):
    for aspect in aspects_filter:
        if aspects_filter[aspect] < 0.2:
            aspects_star[aspect] = 1
        elif aspects_filter[aspect] < 0.4:
            aspects_star[aspect] = 2
        elif aspects_filter[aspect] < 0.6:
            aspects_star[aspect] = 3
        elif aspects_filter[aspect] < 0.8:
            aspects_star[aspect] = 4
        elif aspects_filter[aspect] < 1:
            aspects_star[aspect] = 5
# we use file processing, since the amount of runs of API is limit and it takes a long time
with open('sentiment.txt', 'rb') as f_sent:
    # dictionary for threshold of each aspect
    aspects_threshold = {}
    # dictionary for total amount of each aspect
    count_aspects_all = {}
    # dictionary for rating of each aspect after threshold
    aspects_filter = {}
    # dictionary for total amount of each aspect after threshold
    count_aspects_filter = {}
    # we get the all sent from file
    all_sent = f_sent.read().splitlines()
    # we go over it
    for sent in all_sent:
        # we first separate the aspect and find the total amount of reivew related to aspect
        separate_aspect(eval(sent),aspects_threshold,count_aspects_all)
    # then we calculation the threshold
    calculation_threshold_aspect(aspects_threshold,all_sent,count_aspects_all)
    # we go over again
    for sent in all_sent:
        # we separate the aspect and find the total amout of review related to aspect after threshold
        separate_aspect_with_threshold(eval(sent),aspects_threshold,aspects_filter,count_aspects_filter)
    # then we calculation the rating with threshold and filter version of aspect and count
    calculation_filter_with_threshold(aspects_threshold,aspects_filter,all_sent,count_aspects_filter)
    aspect_star = {}
    convert_deci_star(aspects_filter,aspect_star)
print(aspects_filter)
print(aspect_star)
