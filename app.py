from flask import Flask, render_template, jsonify, request, redirect
import json

from flask.helpers import url_for
from uni_bi_trigrams import *
import uni_bi_trigrams
import scrapper_playstore
import sentiment_analysis
import time

app = Flask(__name__)
#http://localhost:5000/

@app.route('/')
def hello():
    return render_template("dashboard.html")

@app.route('/form_app_id', methods=['POST'])
def form_app_id():
  app_id=request.form['appID']
  app_details=scrapper_playstore.review_app(app_id)

  #corpus = nlp('reviews.txt')
  #print(corpus)
  #redirect(url_for('unidata'))
  #time.sleep(5)
  unidata()
  bidata()
  tridata()
  data = app_details
  scores=sentiment_analysis.analysis()
  data +=scores
  
  '''
  data[comment 0,1,2,3,4,5,6,7,8,9,10, title, number_of_installs, rating, summary, positive_sentiment, negative_sentiment]
  '''
  
  return render_template("dashboard.html",data=data)




@app.route('/unidata', methods=['GET']) 
def unidata():
  corpus = nlp('reviews.txt')
  top_words = get_top_n_words(corpus, n=6)
  top_df = pandas.DataFrame(top_words)
  top_df.columns=["Word", "Freq"]
  uni_labels=list(top_df['Word'])
  uni_data = list(top_df['Freq'])
  data = uni_data
  labels = uni_labels
  return jsonify({'payload':json.dumps({'data':data, 'labels':labels})})
  
@app.route('/bidata', methods=['GET']) 
def bidata():
  corpus = nlp('reviews.txt')
  print(corpus)
  top_words = get_top_n2_words(corpus, n=6)
  top_df = pandas.DataFrame(top_words)
  top_df.columns=["Word", "Freq"]
  bi_labels=list(top_df['Word'])
  bi_data = list(top_df['Freq'])
  data = bi_data
  labels = bi_labels
  return jsonify({'payload':json.dumps({'data':data, 'labels':labels})})

@app.route('/tridata', methods=['GET']) 
def tridata():
  corpus = nlp('reviews.txt')
  top_words = get_top_n3_words(corpus, n=6)
  top_df = pandas.DataFrame(top_words)
  top_df.columns=["Word", "Freq"]
  tri_labels=list(top_df['Word'])
  tri_data = list(top_df['Freq'])
  data = tri_data
  labels = tri_labels
  return jsonify({'payload':json.dumps({'data':data, 'labels':labels})})

if __name__ == '__main__':
    app.run(debug=True)
    
     