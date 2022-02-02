import json
from time import time
import pandas as pd
from related_values_generator import get_related_words
from operator import itemgetter

all_countries_json = open('searches/all_results.json')

all_countries = json.load(all_countries_json)

pragmatic_actions, positive_words, negative_words, hq, countries = itemgetter(
    'pragmatic_actions', 'positive_words', 'negative_words', 'hq','countries')(get_related_words())


dataframe_columns = ['Score Ratio','Norm','SS_POW','positive_words','negative_words','hq','pragmatic_actions']
regulation_scores_df:pd.DataFrame = pd.DataFrame(columns= dataframe_columns, index=[country for country, value in all_countries.items()])

for country_name, country_results in all_countries.items():
    
    positive_total = 0
    negative_total = 0
    country_hits = int(country_results['total_results'].replace(',',''))

    positive_words = country_results['positive']
    negative_words = country_results['negative']

    for positive_word, positive_hits in positive_words.items():
        positive_total += positive_hits

    for negative_word, negative_hits in negative_words.items():
        negative_total += negative_hits
    
    max = positive_total if positive_total>=negative_total else negative_total
    score_ratio = (positive_total - negative_total) / max
    norm = (positive_total+negative_total) / country_hits
    ss_pow = score_ratio * norm

    print('    score_ratio: ', score_ratio)
    print('    norm: ', norm)
    print('    ss_pow: ', ss_pow)

    regulation_scores_df.xs(country_name)[dataframe_columns[0]] = score_ratio
    regulation_scores_df.xs(country_name)[dataframe_columns[1]] = norm
    regulation_scores_df.xs(country_name)[dataframe_columns[2]] = ss_pow
    regulation_scores_df.xs(country_name)[dataframe_columns[3]] = ', '.join([str(pword) for pword in positive_words])
    regulation_scores_df.xs(country_name)[dataframe_columns[4]] = ', '.join([str(nword) for nword in negative_words])
    regulation_scores_df.xs(country_name)[dataframe_columns[5]] = hq
    regulation_scores_df.xs(country_name)[dataframe_columns[6]] = pragmatic_actions


with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print('FINAL: ', regulation_scores_df)

regulation_scores_df.to_csv('./regulation_score{}.csv'.format(int(time())))
