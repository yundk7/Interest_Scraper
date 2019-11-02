# 1. import Flask
from flask import Flask, request, render_template, session, redirect, jsonify
import pandas as pd
from splinter import Browser
import requests
from bs4 import BeautifulSoup
import re
import operator as op
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
# from IPython.display import Image
# from IPython.core.display import HTML
from time import sleep

# import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.xception import (
    Xception, preprocess_input, decode_predictions)
from PIL import Image
import requests
from io import BytesIO

from tensorflow import keras
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg19 import (
    VGG19, 
    preprocess_input, 
    decode_predictions
)

pd.set_option('display.max_colwidth', -1)
url = 'https://youtube.com'

# #using beautifulsoup only, splinter not working for for loop
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')
# news = soup.find_all("h3",class_="title")
# #extracting href and combining with url to get news url and append in list
# news_urls = []
# for n in range(0,3):
#     news_urls.append(url + news[n].a['href'])
# news_df = pd.DataFrame()
# for u in news_urls:
#     response = requests.get(u)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     title = str(soup.find_all("h1",class_="article_title")).splitlines()[1]
#     rel_date = soup.find_all("span",class_="release_date")
#     rel_date = str(rel_date).splitlines()[1][2:]
#     para = soup.find_all("p")
#     para = str(para[1]).replace("<p>","").replace("</p>","").replace("—","")
#     df = pd.DataFrame({"date":[rel_date],"title":[title],"content":[para]})
#     news_df = news_df.append(df)
# news_df.to_html("news.html")



# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return ("interest scraper")


# 4. Define what to do when a user hits the /about route

@app.route("/xception", methods=["GET", "POST"])
def xception():
    if request.method == "POST":
        instaid = request.form["instaid"]
    
        #scraping images with beautifulsoup
        url = "https://www.instagram.com/" + instaid
        browser = Browser('chrome')
        browser.visit(url)
        sleep(1)
        bs = BeautifulSoup(browser.html, 'html.parser')

        #finds all the images in website and puts url in df
        images = bs.find_all('img', {'src':re.compile('.jpg')})
        image_urls = []
        for image in images: 
            image_urls.append(str(image['src']))
        image_df = pd.DataFrame({"image":image_urls})
        
        import numpy as np
        import tensorflow as tf

        from tensorflow.keras.preprocessing import image
        from tensorflow.keras.applications.xception import (
            Xception, preprocess_input, decode_predictions)

        from PIL import Image
        import requests
        from io import BytesIO


        model = Xception(
            include_top=True,
            weights='imagenet')
        
        prds = []
        pcts = []
        for i in image_urls:
            url = i
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img = img.resize((299, 299), Image.NEAREST)
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            predictions = model.predict(x)
            prds.append(decode_predictions(predictions, top=1)[0][0][1])
            pcts.append(decode_predictions(predictions, top=1)[0][0][2])
#             cnns.append(decode_predictions(predictions, top=3)[0])
        image_df["predictions"] = prds
        image_df["%"] = pcts
        image_df.sort_values("%",ascending = False,inplace = True)
        
#         from IPython.display import Image
#         from IPython.core.display import HTML
        
#         def path_to_image_html(path):
#             return '<img src="'+ path + '" width="300" >'
        
#         print("Server received request for 'About' page...")
#         return (image_df.to_html(escape=False ,formatters=dict(image=path_to_image_html)))
    
    
        depart =  request.form["depart"]
        pois = image_df.head(3)["predictions"]
        target_radius = 1000
        
        records = pd.DataFrame()
        target_list = str(pois).split(",")
        targets = str(depart).split(",")
        for target in targets:
                # Build the endpoint URL
            target_url = (f'https://maps.googleapis.com/maps/api/geocode/json?address={target}&key={gkey}')
            geo_data = requests.get(target_url).json()


            target_adr = geo_data["results"][0]["formatted_address"]
            lat = geo_data["results"][0]["geometry"]["location"]["lat"]
            lng = geo_data["results"][0]["geometry"]["location"]["lng"]

            target_coordinates = str(lat) + "," + str(lng)
            
            
#             target_radius = 800
            target_type = ""

            # set up a parameters dictionary

            for target_search in target_list:
                params = {
                    "location": target_coordinates,
                    "keyword": target_search,
                    "radius": target_radius,
                    "type": target_type,
                    "key": gkey
                }

                # base url
                base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

                # run a request using our params dictionary
                response = requests.get(base_url, params=params)
                places_data = response.json()

                n=0
                # while int(n) > len(places_data):
                while int(n) < len(places_data["results"]):
                    try:
                        price=places_data["results"][int(n)]["price_level"]
                    except KeyError:
                        price = "NA"
                    try:
                        link=places_data["results"][int(n)]["place_id"]
                    except KeyError:
                        link = "NA"
                    try:
                        score = places_data["results"][int(n)]["rating"]
                    except KeyError:
                        score = "NA"
                    try:
                        reviews = places_data["results"][int(n)]["user_ratings_total"]
                    except KeyError:
                        reviews = "NA"
#                     try:
#                         poi_coord = str(places_data["results"][int(n)]["geometry"]["location"]["lat"]) + "," + str(places_data["results"][int(n)]["geometry"]["location"]["lng"])
# #                         dist = pd.read_html(f"http://boulter.com/gps/distance/?from={target_coordinates}&to={poi_coord}&units=k")
# #                         distance = float(str(dist[1][1][1]).split(" ")[0])
# #                     except IndexError or TimeoutError:
# #                         distance = "NA"
#                         drive_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={target_coordinates}&destinations={poi_coord}&key=AIzaSyA-Rjp6nOeJp6815Xt1Kkuxc5XKMiKl_yA"
#                         drive_res = requests.get(drive_url).json()
#                         distance = drive_res["rows"][0]["elements"][0]["distance"]["value"]/1000
#                         duration= int(drive_res["rows"][0]["elements"][0]["duration"]["value"]/60)
#                     except KeyError:
#                         distance = "NA"
#                         drive_dur = "NA"
                    
#                     try:
#                         walk_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={target_coordinates}&destinations={poi_coord}&mode=walking&key=AIzaSyA-Rjp6nOeJp6815Xt1Kkuxc5XKMiKl_yA"
#                         walk_res = requests.get(walk_url).json()
#                         distance = walk_res["rows"][0]["elements"][0]["distance"]["value"]/1000
#                         walk_dur = int(walk_res["rows"][0]["elements"][0]["duration"]["value"]/60)
#                     except KeyError:
#                         walk_dur = "NA"
                    
#                     try:
#                         transit_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={target_coordinates}&destinations={poi_coord}&mode=transit&key=AIzaSyA-Rjp6nOeJp6815Xt1Kkuxc5XKMiKl_yA"
#                         transit_res = requests.get(transit_url).json()
#                         transit_dur = int(transit_res["rows"][0]["elements"][0]["duration"]["value"]/60)
#                     except KeyError:
#                         transit_dur = "NA"
                    
                    content = pd.DataFrame ({"depart":target_adr,"poi":target_search,
                                            "name":[places_data["results"][int(n)]["name"]],
                                            "score":score,
                                             "reviews":reviews,
                                             "price":price,
                                             "link":link,
                                            "address":[places_data["results"][int(n)]["vicinity"]]})
#                                            "distance":distance,
#                                             "drive":duration,
#                                             "public":transit_dur,
#                                             "walk":walk_dur})
                    records = records.append(content)
                    n+=1
        records.reset_index(drop = True,inplace = True)
        records["link"]=records["link"].apply(lambda x: '<a href="https://www.google.com/maps/place/?q=place_id:{0}">link</a>'.format(x))
        return (records.to_html(escape=False))

    return render_template("xception.html")

@app.route("/vgg19", methods=["GET", "POST"])
def vgg19():
    if request.method == "POST":
        instaid = request.form["instaid"]
    
        #scraping images with beautifulsoup
        url = "https://www.instagram.com/" + instaid
        browser = Browser('chrome')
        browser.visit(url)
        sleep(1)
        bs = BeautifulSoup(browser.html, 'html.parser')

        #finds all the images in website and puts url in df
        images = bs.find_all('img', {'src':re.compile('.jpg')})
        image_urls = []
        for image in images: 
            image_urls.append(str(image['src']))
        image_df = pd.DataFrame({"image":image_urls})
        
        import numpy as np
        import tensorflow as tf

        from tensorflow import keras
        from tensorflow.keras.preprocessing import image
        from tensorflow.keras.applications.vgg19 import (
            VGG19, 
            preprocess_input, 
            decode_predictions
        )

        from PIL import Image
        import requests
        from io import BytesIO


        model = VGG19(include_top=True, weights='imagenet')
        
        prds = []
        pcts = []
        for i in image_urls:
            url = i
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img = img.resize((224, 224), Image.NEAREST)
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            predictions = model.predict(x)
            prds.append(decode_predictions(predictions, top=1)[0][0][1])
            pcts.append(decode_predictions(predictions, top=1)[0][0][2])
#             cnns.append(decode_predictions(predictions, top=3)[0])
        image_df["prediction"] = prds
        image_df["%"] = pcts
        image_df.sort_values("%",ascending = False, inplace = True)
        
        from IPython.display import Image
        from IPython.core.display import HTML
        
        def path_to_image_html(path):
            return '<img src="'+ path + '" width="300" >'
        
        print("Server received request for 'About' page...")
        return (image_df.to_html(escape=False ,formatters=dict(image=path_to_image_html)))

    return render_template("vgg19.html")


if __name__ == "__main__":
    app.run(debug=True)
