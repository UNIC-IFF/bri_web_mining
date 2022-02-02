#!/usr/bin/python

import sys, getopt
import pandas as pd
from time import time

def main(argv):

    ground_truth = ''
    corr_calc = ''
    column_to_calculate = ''
    corr_method=''

    try:
        opts, args = getopt.getopt(argv,"g:c:b:m:",["gtruthFile=","corrFile=","columnCalc=","method="])
    except getopt.GetoptError:
        print('test.py -g <ground_truth> -c <correlation_variant> -b <based column calculation> -m <method>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -g <ground_truth> -c <correlation_variant> -b <based column calculation -m <method>')
            sys.exit()
        elif opt in ("-g", "--gtruthFile"):
            ground_truth = arg
        elif opt in ("-c", "--corrFile"):
            corr_calc = arg
        elif opt in ("-b", "--columnCalc"):
            column_to_calculate = arg
        elif opt in ("-m", "--method"):
            corr_method = arg
   
    ground_truth_df = pd.read_csv(ground_truth, header=[0], index_col=0)
    corr_var_df = pd.read_csv(corr_calc, header=[0], index_col=0)
    print('\nCorrelation Dataframe: ', corr_var_df)
    print('\nCorrelation Method: ', corr_method)
    
    COLUMN_TO_GET = column_to_calculate

    print('\nGround Truth Dataframe: ', ground_truth_df)
    columns_to_correlate = ground_truth_df.join(corr_var_df if COLUMN_TO_GET == '' else corr_var_df[COLUMN_TO_GET])

    print('\nColumns to correlate: ', columns_to_correlate)
    # ground_truth_df_norm.to_csv('ground_truth_df_norm{}.csv'.format(int(time())))
    correllation_result = columns_to_correlate.corr(method=corr_method)

    #    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print('\nCorrelation Result: ', correllation_result)

if __name__ == "__main__":
   main(sys.argv[1:])