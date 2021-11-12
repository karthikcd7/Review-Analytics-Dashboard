from google_play_scraper import Sort, reviews, app


def review_app(id):
    result, continuation_token = reviews(
        id,
        #lang='en', # defaults to 'en'
        #country='us', # defaults to 'us'
        sort=Sort.NEWEST, # defaults to Sort.MOST_RELEVANT
        count=1000, # defaults to 100
        #filter_score_with=5 # defaults to None(means all score)
    )

    # If you pass `continuation_token` as an argument to the reviews function at this point,
    # it will crawl the items after 3 review items.

    result, _ = reviews(
        id,
        continuation_token=continuation_token # defaults to None(load from the beginning)
    )

    details = app(
    id,
    #lang='en', # defaults to 'en'
    #country='us' # defaults to 'us'
    )
    #print(result)
    number_of_reviews_found = len(result)
    print("Number of reviews found:",number_of_reviews_found)
    #print(result[0]['content'])
    number_of_reviews_infile = 1000
    print("Number of reviews put in file:",number_of_reviews_infile)
    with open('./reviews.txt' , 'w', encoding="utf-8") as file:
        for i in range(number_of_reviews_infile):
            # Adding a random uncomman string at the end of each review
            # Which will make it easier to detect the starting and ending of each review while reading
            file.write(result[i]['content'] + '\n^^^\n') 
    
    data = [result[0]["content"], result[1]["content"], result[2]["content"], result[3]["content"], result[4]["content"], result[5]["content"],\
            result[6]["content"], result[7]["content"], result[8]["content"], result[9]["content"], result[10]["content"], details["title"], \
            details["installs"], "{:.1f}".format(details["score"]), details["description"]]
    return data
    

if __name__ == "__main__":
    id = 'com.google.android.apps.meetings'
    review_app(id)