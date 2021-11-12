import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.collocations import *
from nltk.stem.porter import PorterStemmer
from nltk.corpus import wordnet as wn
import re

from os import path
from PIL import Image
from nltk.tokenize.destructive import MacIntyreContractions
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt , mpld3 

from sklearn.feature_extraction.text import CountVectorizer

import plotly.graph_objects as go
import seaborn as sns
import pandas
#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('wordnet')


def nlp(filename):
    wn.ensure_loaded()
    wordnet_lemmatizer = WordNetLemmatizer()
    stopWords = set(stopwords.words('english'))
    new_words = ['app','and','to','they','is','have','the','even','though','make','people','use','code', 'google', 'meet']
    stop_words = stopWords.union(new_words)
    with open(filename,'r', encoding="utf-8") as file:
        data = file.read()
    sentences = data.split("\n^^^\n")
    words = nltk.tokenize.word_tokenize(data)
    words = [word for word in words if word !='^^^']
    #print(words)
    corpus = []
    for word in words:
        text = re.sub('[^a-zA-Z]', '',word)
        text = re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
        text=re.sub("(\\d|\\W)+"," ",text)
        lower = text.lower()
        lem = wordnet_lemmatizer.lemmatize(lower)
        if lem:
            corpus.append(lem)
    corpus = [word for word in corpus if word not in stop_words and len(word)>2]
    print("\n")
    return corpus
#print(corpus)

'''
# Word cloud to know words with high frequency
wordcloud = WordCloud(background_color='white',stopwords = stop_words,max_words=100,max_font_size=50, random_state=42).generate(str(corpus))

fig = plt.figure(1)
#plt.imshow(wordcloud)
plt.axis('off')
#plt.show()
fig.savefig("word1.png", dpi=900)
'''
#Most frequently occuring uni-grams
def get_top_n_words(corpus, n=None):
    vec = CountVectorizer().fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]
#Convert most freq words to dataframe for plotting bar plot


'''
#Barplot of most freq uni-grams
fig, g = plt.subplots()
sns.set(rc={'figure.figsize':(13,8)})
g = sns.barplot(x="Word", y="Freq", data=top_df)
g.set_xticklabels(g.get_xticklabels(), rotation=30)
fig.savefig("uni.png", dpi=900)
#plt.show()
fig = go.Figure(
    data=[go.Bar(y=top_df["Freq"],x=top_df["Word"])],
    layout_title_text="A Figure Displayed with fig.show()"
)
#fig.show()
'''

#Most frequently occuring Bi-grams
def get_top_n2_words(corpus, n=None):
    corpus2 = [" ".join(word for word in corpus)]
    vec1 = CountVectorizer(analyzer='word',ngram_range=(2,2),max_features=2000)
    x1 = vec1.fit_transform(corpus2)
    bag_of_words = vec1.transform(corpus2)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec1.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]

'''
#Barplot of most freq Bi-grams
fig, h = plt.subplots()
sns.set(rc={'figure.figsize':(13,8)})
h=sns.barplot(x="Bi-gram", y="Freq", data=top2_df)
h.set_xticklabels(h.get_xticklabels(), rotation=45)
fig.savefig("bi.png", dpi=900)
#plt.show()
'''

#Most frequently occuring Tri-grams
def get_top_n3_words(corpus, n=None):
    corpus2 = [" ".join(word for word in corpus)]
    vec2 = CountVectorizer(ngram_range=(3,3), max_features=2000).fit(corpus2)
    x2 = vec2.fit_transform(corpus2)
    bag_of_words = vec2.transform(corpus2)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec2.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]
'''

#Barplot of most freq Tri-grams
fig, j = plt.subplots()
sns.set(rc={'figure.figsize':(13,8)})
j=sns.barplot(x="Tri-gram", y="Freq", data=top3_df)
j.set_xticklabels(j.get_xticklabels(), rotation=45)
fig.savefig("tri.png", dpi=900)
# Outputs all the bar graphs
#plt.show()
'''

if __name__ == "__main__":
    
    corpus = nlp('reviews.txt')
    
    top_words = get_top_n_words(corpus, n=10)
    top_df = pandas.DataFrame(top_words)
    top_df.columns=["Word", "Freq"]
    print(top_df)

    top2_words = get_top_n2_words(corpus, n=10)
    top2_df = pandas.DataFrame(top2_words)
    top2_df.columns=["Bi-gram", "Freq"]
    print(top2_df)

    top3_words = get_top_n3_words(corpus, n=10)
    top3_df = pandas.DataFrame(top3_words)
    top3_df.columns=["Tri-gram", "Freq"]
    print(top3_df)