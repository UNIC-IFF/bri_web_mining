# params:
# hq
# country to search for
# positive words array
# negative words array
# neatral words array
from related_values import pragmatic_actions, positive_words, negative_words


def get_related_words(pragmatic_actions=pragmatic_actions, positive_words=positive_words, negative_words=negative_words):

    related_items = {'pragmatic_actions': pragmatic_actions,
                     "positive_words": positive_words, "negative_words": negative_words}

    return related_items
