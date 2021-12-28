import json
from related_values_generator import get_related_words
from operator import itemgetter
from utils import api_search_engine

search_for = ['Cyprus']

pragmatic_actions, positive_words, negative_words = itemgetter(
    'pragmatic_actions', 'positive_words', 'negative_words')(get_related_words())

for country in search_for:
    print('Country: ', country)

    positive_total = None
    negative_total = None
    country_hits = None

    for action in pragmatic_actions:
        print('Country: ', country.upper())
        print('    action: ', action.upper())

        result = api_search_engine(query=country, action=action)

        results_json = json.dumps(result, indent=4)

        country_hits = int(result["searchInformation"]["totalResults"])

        print('    TOTAL RESULTS: {}\n'.format(json.dumps(
            result["searchInformation"]["formattedTotalResults"])))

        with open('total_results{}.json'.format(action), "w") as file:
            file.write(results_json)

        for positive_word in positive_words:

            query = 'intext:{} ~{} ~({})'.format(
                country.lower(), positive_word, action)
            positive_result = api_search_engine(
                query=query, action=action, country=country, word=positive_word, keyword='positive')

            positive_total = int(
                positive_result["searchInformation"]["totalResults"])

            with open('positive_results{}.json'.format(positive_word), 'w') as file:
                file.write(json.dumps(positive_result, indent=4))

        for negative_word in negative_words:
            query = 'intext:{} ~{} ~({})'.format(
                country.lower(), negative_word, action)

            negative_result = api_search_engine(
                query=query, action=action, country=country, word=positive_word, keyword='negative')

            negative_total = int(
                negative_result["searchInformation"]["totalResults"])

            with open('negative_results{}.json'.format(positive_word), 'w') as file:
                file.write(json.dumps(positive_result, indent=4))

    max = positive_total if positive_total >= negative_total else negative_total
    score_ratio = (positive_total + negative_total) / max
    norm = (positive_total+negative_total) / country_hits
    ss_pow = score_ratio * norm

    print('    ***FINAL RESULTS****\n    Score Ratio: {}\n    Norm: {}\n    SS_POW: {}\n    ******************'.format(
                                                                            score_ratio, norm, ss_pow))
