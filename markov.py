import pandas as pd
import numpy as np

def numberToQuantile( percent ):
        if percent < -0.01:
            return 0
        elif percent < 0:
            return 1
        elif percent < 0.01:
            return 2
        else:
            return 3

def addToMarkovDict (markovdict, dictstring):
    if dictstring in markovdict:
        markovdict[dictstring] += 1    
    else:
        markovdict[dictstring] = 1
    return markovdict

def stock_df_to_percents( df ):
    return (df['Close'] - df['Open']) / df['Open']

def calculateMarkov( quantiles ):
    markovQ1 = {}
    markovQ2 = {}
    markovQ3 = {}
    markovQ4 = {}
    
    for x in range(0, int(len(quantiles) - (len(quantiles) * 0.1))):
        dictstring = str(quantiles[x]) + str(quantiles[x+1]) + str(quantiles[x+2])
        quantile = quantiles[x+3]
        if quantile == 0:
            addToMarkovDict(markovQ1, dictstring)
        elif quantile == 1:
            addToMarkovDict(markovQ2, dictstring)
        elif quantile == 2:
            addToMarkovDict(markovQ3, dictstring)
        else:
            addToMarkovDict(markovQ4, dictstring)
    return [markovQ1, markovQ2, markovQ3, markovQ4]

def number_in_last_10_percent (arr):
    return int((len(arr)-3) -  (len(arr) - (len(arr) * 0.1)))

def get_number_from_dict(dict, str):
    try:
        return dict[str]
    except:
        return 0


def exerciseMarkov (quantiles, markovQ1, markovQ2, markovQ3, markovQ4):
    totalcorrect = 0
    unpredicted = 0
    highrangetotal = 0
    highrangecorrect = 0
    highconftotal = 0
    highconfcorrect = 0
    highconfpercent = 0.4
    for x in range (int(len(quantiles) - (len(quantiles) * 0.1)), int(len(quantiles) - 3)):
        dictstring = str(quantiles[x]) + str(quantiles[x+1]) + str(quantiles[x+2])
        quantile = quantiles[x+3]
        q1total = get_number_from_dict(markovQ1, dictstring)
        q2total = get_number_from_dict(markovQ2, dictstring)
        q3total = get_number_from_dict(markovQ3, dictstring)
        q4total = get_number_from_dict(markovQ4, dictstring)
        total = int(q1total) + int(q2total) + int(q3total) + int(q4total)
        highconf = False
        predict = -1
        if q1total > max(q2total, q3total, q4total):
            print('we predict a big loss with a ' + str(int(q1total) / total) + ' percent likelihood')
            predict = 0
            if (q1total / total) > highconfpercent:
                highconf = True
        elif q2total > max(q1total, q3total, q4total):
            print('we predict a small loss with a ' + str(int(q2total) / total) + ' percent likelihood')
            predict = 1
            if (q2total / total) > highconfpercent:
                highconf = True
        elif q3total > max(q1total, q2total, q4total):
            print('we predict a small gain with a ' + str(int(q3total) / total) + ' percent likelihood')
            predict = 2
            if (q3total / total) > highconfpercent:
                highconf = True
        elif q4total > max(q1total, q2total, q3total):
            print('we predict a big gain with a ' + str(int(q4total) / total) + ' percent likelihood')
            predict = 3
            highrangetotal += 1
            if (q4total / total) > highconfpercent:
                highconf = True
        else:
            print('we have no prediction. the totals were: ' + str(q1total) + ', ' + str(q2total) + ', ' + str(q3total) + ', ' + str(q4total))
            unpredicted += 1
        print('the actual result was: ' + str(quantile))
        if highconf:
            highconftotal += 1
        if int(quantile) == predict:
            totalcorrect += 1
            if predict == 3:
                highrangecorrect += 1
            if highconf:
                highconfcorrect += 1
        

    print('total correct is: ' + str(totalcorrect) + ' out of: ' + str(number_in_last_10_percent(quantiles)))
    print('thats ' + str(totalcorrect / number_in_last_10_percent(quantiles))  + ' percent!')
    print('not accounting for unpredicted, thats: ' + str(totalcorrect) + ' out of: ' + str(number_in_last_10_percent(quantiles) - unpredicted))
    print('thats ' + str(totalcorrect / (number_in_last_10_percent(quantiles) - unpredicted) ) + ' percent!')
    print('highrange correct was: ' + str(highrangecorrect) + ' out of ' + str(highrangetotal))
    print('thats ' + str(highrangecorrect / highrangetotal) + ' percent!')
    print('high confidence correct was :' + str(highconfcorrect) + ' out of: ' + str(highconftotal))
    print('thats ' + str(highconfcorrect / highconftotal) + ' percent!')

appledf = pd.read_csv('data/AAPL.csv', sep=',')
amazondf = pd.read_csv('data/AMZN.csv', sep=',')
googledf = pd.read_csv('data/GOOGL.csv', sep=',')

applepercents = stock_df_to_percents(appledf)
amazonpercents = stock_df_to_percents(amazondf)
googlepercents = stock_df_to_percents(googledf)


applequantiles = [numberToQuantile(item) for item in applepercents]
amazonquantiles = [numberToQuantile(item) for item in amazonpercents]
googlequantiles = [numberToQuantile(item) for item in googlepercents]

[applemarkovQ1, applemarkovQ2, applemarkovQ3, applemarkovQ4]  = calculateMarkov(applequantiles)

exerciseMarkov(applequantiles, applemarkovQ1, applemarkovQ2, applemarkovQ3, applemarkovQ4)

print('total length: ' + str(len(applequantiles)))

