import json
from related_values_generator import get_related_words
from operator import itemgetter
from utils import api_search_engine
import pandas as pd
import time

time0 = time.time()

pragmatic_actions, positive_words, negative_words, hq, countries = itemgetter(
    'pragmatic_actions', 'positive_words', 'negative_words', 'hq','countries')(get_related_words())

dataframe_columns = ['Score Ratio','Norm','SS_POW','positive_words','negative_words','hq','pragmatic_actions']
regulation_scores_df:pd.DataFrame = pd.DataFrame(columns= dataframe_columns, index=[country for country in countries])

dictionary_country:dict = {}
all_countries_results:dict = {}

for country in countries:
    print('Country: ', country)
    # for action in pragmatic_actions:
    print('Country: ', country.upper())
    print('    action: ', hq.upper())

    positive_total = 0
    negative_total = 0
    country_hits = None
    country_path = 'searches/{}'.format(country)

    result = api_search_engine(query=country, action=hq)

    results_json = json.dumps(result, indent=4)

    country_hits = int(result["searchInformation"]["totalResults"])
    
    print('    TOTAL RESULTS: {}\n'.format(json.dumps(
        result["searchInformation"]["formattedTotalResults"])))

    # with open('searches/total_results{}_{}.json'.format(hq, country), "w") as file:
    #     file.write(results_json)
    
    with open('searches/total_results/{}.json'.format(country), "w") as file:
        file.write(results_json)

    dictionary_country[country] = {'total_results':result["searchInformation"]["formattedTotalResults"]}
    print('dictionary_country[country]', dictionary_country[country])
    dictionary_country[country]['positive']={}
    dictionary_country[country]['negative']={}
    # with open('searches/total_results_hits{}_{}.json'.format(hq, country), "w") as file:
    #     file.write("total-hits":results_json['searchInformation']["totalResults"])

    for positive_word in positive_words:

        query = 'intext:{} ~{} ~{}'.format(
            country.lower(), positive_word, pragmatic_actions)
        # print('positive hq: ', hq)
        # print('positive word: ', positive_word)
        # print('positive query: ', query)
        positive_result = api_search_engine(
            query=query, action=hq, country=country, word=positive_word, keyword='positive')

        postive_word_hits = int(
            positive_result["searchInformation"]["totalResults"])
        positive_total = positive_total + postive_word_hits

        prev_pos = dictionary_country[country]['positive']
        new_pos = {positive_word : postive_word_hits}
        dictionary_country[country]['positive'] = {**prev_pos, **new_pos}


        # with open('searches/positive_results{}_{}.json'.format(positive_word, country), 'w') as file:
        #     file.write(json.dumps(positive_result, indent=4))

        # with open('searches/positive_results_hits{}_{}.json'.format(positive_word, country), "w") as file:
        #     file.write({"total-hits":results_json['searchInformation']["totalResults"]})
            

    for negative_word in negative_words:
        query = 'intext:{} ~{} ~{}'.format(
            country.lower(), negative_word, pragmatic_actions)

        negative_result = api_search_engine(
            query=query, action=hq, country=country, word=negative_word, keyword='negative')
        
        # print('negative hq: ', hq)
        # print('negative_word: ', negative_word)
        # print('negative query: ', query)

        negative_word_hits = int(
            negative_result["searchInformation"]["totalResults"])

        negative_total = negative_total + negative_word_hits

        # with open('searches/negative_results{}_{}.json'.format(negative_word, country), 'w') as file:
        #     file.write(json.dumps(negative_result, indent=4))

        prev_neg = dictionary_country[country]['negative']
        new_neg = {negative_word : negative_word_hits}
        dictionary_country[country]['negative'] = {**prev_neg, **new_neg}

    max = positive_total if positive_total >= negative_total else negative_total
    score_ratio = (positive_total - negative_total) / max
    norm = (positive_total+negative_total) / country_hits
    ss_pow = score_ratio * norm

    print('country: ', country)
    print('country hits type: ', type(country_hits))

    regulation_scores_df.xs(country)[dataframe_columns[0]] = score_ratio
    regulation_scores_df.xs(country)[dataframe_columns[1]] = norm
    regulation_scores_df.xs(country)[dataframe_columns[2]] = ss_pow
    regulation_scores_df.xs(country)[dataframe_columns[3]] = ', '.join([str(pword) for pword in positive_words])
    regulation_scores_df.xs(country)[dataframe_columns[4]] = ', '.join([str(nword) for nword in negative_words])
    regulation_scores_df.xs(country)[dataframe_columns[5]] = hq
    regulation_scores_df.xs(country)[dataframe_columns[6]] = pragmatic_actions

    dictionary_country[country]['score_ratio'] = score_ratio
    dictionary_country[country]['norm'] = norm
    dictionary_country[country]['ss_pow'] = ss_pow
    dictionary_country[country]['hq'] = hq
    dictionary_country[country]['pragmatic_actions'] = pragmatic_actions
    dictionary_country[country]['max'] = max
    dictionary_country[country]['positive_total'] = positive_total
    dictionary_country[country]['negative_total'] = negative_total
    dictionary_country[country]['country_hits'] = country_hits  
    
    # using list comprehension
# listToStr = ' '.join([str(elem) for elem in s])


    print('    ***FINAL RESULTS****\n    Score Ratio: {}\n    Norm: {}\n    SS_POW: {}\n    ******************'.format(
                                                                            score_ratio, norm, ss_pow))
    # regulation_scores_df[country] = regulation_scores_df.loc[country]
    # regulation_scores_df.append(pd.Series(data=ss_pow, index=[country]), ignore_index=True)
    all_countries_results = {**all_countries_results , **dictionary_country}
    with open('searches/{}.json'.format(country),'w') as file:
        file.write(json.dumps(dictionary_country))
    
    with open('searches/all_results.json','w') as file:
        file.write(json.dumps(all_countries_results))
    # dictionary_country
    dictionary_country={}
    time.sleep(1)

    # regulation_scores_df.append({country:ss_pow}, ignore_index=True)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print('FINAL: ', regulation_scores_df)

regulation_scores_df.to_csv('./regulation_score.csv')

final_time = time.time() - time0 

print('final time: ', final_time)
