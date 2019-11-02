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
        
        cnns = []
        for i in image_urls:
            url = i
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img = img.resize((299, 299), Image.NEAREST)
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            predictions = model.predict(x)
            cnns.append(decode_predictions(predictions, top=1)[0][0])
#             cnns.append(decode_predictions(predictions, top=3)[0])
        image_df["CNN"] = cnns
        
        from IPython.display import Image
        from IPython.core.display import HTML
        
        def path_to_image_html(path):
            return '<img src="'+ path + '" width="300" >'
        
        print("Server received request for 'About' page...")
        return (image_df.to_html(escape=False ,formatters=dict(image=path_to_image_html)))

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
        
        cnns = []
        for i in image_urls:
            url = i
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img = img.resize((224, 224), Image.NEAREST)
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            predictions = model.predict(x)
            cnns.append(decode_predictions(predictions, top=1)[0][0])
#             cnns.append(decode_predictions(predictions, top=3)[0])
        image_df["CNN"] = cnns
        
        from IPython.display import Image
        from IPython.core.display import HTML
        
        def path_to_image_html(path):
            return '<img src="'+ path + '" width="300" >'
        
        print("Server received request for 'About' page...")
        return (image_df.to_html(escape=False ,formatters=dict(image=path_to_image_html)))

    return render_template("vgg19.html")


if __name__ == "__main__":
    app.run(debug=True)
