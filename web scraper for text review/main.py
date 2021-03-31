# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import logging
import string
import re
from flask import render_template, Flask
import requests
from bs4 import BeautifulSoup
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

app = Flask(__name__)  # initialising the flask app with the name 'app'

# base url + /
#http://localhost:8000 + /
@app.route('/', methods=['GET']) # route with allowed methods as POST and GET
def index():
    page = requests.get("https://editorial.rottentomatoes.com/guide/the-best-movies-of-2020/")
    soup = BeautifulSoup(page.content, 'html.parser')
    commentboxes = soup.find_all('div', {'class': "row countdown-item"})
    logging.basicConfig(filename="logfilename.log", level=logging.INFO)
    try:
        reviews = []
        for commentbox in commentboxes:
                textReview = commentbox.text
                iteratedata = list(filter(bool, textReview.splitlines()))

                str1 = iteratedata[1]
                str2 = iteratedata[0].replace("#","")
                str3 = "None"
                str4 = "None"
                str5 = "None"
                str6 = "None"

                if "Critics" in iteratedata[4]:
                    str3 = iteratedata[4]
                else:
                    iteratedata.insert(4, "None")

                if "Synopsis" in iteratedata[5]:
                    str4 = iteratedata[5]
                else:
                    iteratedata.insert(5, "None")

                if "Starring" in iteratedata[6]:
                    str5 = iteratedata[6]
                else:
                    iteratedata.insert(6, "None")

                if len(iteratedata) == 8 and "Directed" in iteratedata[7]:
                    str6 = iteratedata[7]
                else:
                    iteratedata.insert(7, "None")

                mydict = {"movie": str1, "score": str2, "critics": str3,
                          "synopsis": str4, "starring": str5, "directedBy": str6}  # saving that detail to a dictionary
                logging.info(mydict)
                reviews.append(mydict)  # appending the comments to the review list

        return render_template('results.html', reviews=reviews)

    except:
        return 'something is wrong'


if __name__ == "__main__":
    app.run(port=8000,debug=True) # running the app on the local machine on port 8000