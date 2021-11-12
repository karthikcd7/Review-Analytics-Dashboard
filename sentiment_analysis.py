from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
#nltk.download('vader_lexicon')
def analysis():
    with open('reviews.txt','r', encoding="utf-8") as file:
        data = file.read()

    sentences = data.split('\n^^^\n')
    #print(sentences)
    negative = 0
    positive = 0
    neutral = 0

    sid = SentimentIntensityAnalyzer()
    for sentence in sentences:
        #print(sentence)
        #ss is of type dict
        ss = sid.polarity_scores(sentence)
        #for k in sorted(ss):
            #print('{0}: {1}, '.format(k, ss[k]), end='\n')
        
        negative += ss['neg']
        positive += ss['pos']
        neutral += ss['neu']

    number_of_sentences = len(sentences)-1
    perc_negative = negative*100/number_of_sentences
    perc_positive = positive*100/number_of_sentences
    perc_neutral = neutral*100/number_of_sentences

    print("Based on " + str(number_of_sentences) + " Reviews!")
    print("Negative % = ",perc_negative)
    print("Positive % = ",perc_positive)
    print("Neutral % = ",perc_neutral)
    return ["{:.2f}".format(perc_positive), "{:.2f}".format(perc_negative)]
    

if __name__ == "__main__":
    analysis()