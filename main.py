from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
from selenium import webdriver
from bs4 import BeautifulSoup
from os import path
import warnings
import time
import csv
import re
import os


# parameter
SLEEP_TIME = 2

# hide deprecated warnings
warnings.filterwarnings("ignore")

# ask user to give input
keywords = input("Enter keyword seperate by white-space: \n")
pages = input("\nHow many pages you want to search [~999]: \n")
print(f"\n[keywords]: {keywords} \n[search range]: 1-{pages} pages\n")


# output file setting
filename = datetime.now().strftime("%Y_%m_%d_%H_%M") + keywords + ".csv"
if path.exists(filename):
    os.remove(filename)

with open(filename, "a", newline="", encoding="utf-8-sig'") as f:
    writer = csv.writer(f)
    writer.writerow(
        ["post_id", "topic", "author", "content", "timestamp", "comment_number"]
    )

# set up connection to reddit website
options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
chrome = webdriver.Chrome("./chromedriver", chrome_options=options)
chrome.get("https://www.reddit.com/search/?q=" + keywords)

# scroll down page to access the website
for x in range(1, int(pages)):
    chrome.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(SLEEP_TIME)


# parse the whole file and check if the contents matches input
post_id = 0
soup = BeautifulSoup(chrome.page_source, "html.parser")
posts = soup.find_all("div", attrs={"data-testid": "post-container"})
for post in posts:

    # topic
    topic = post.find("h3").text

    # content
    content = ""
    if post.find("p"):
        content = "[text: ]" + post.find("p").text
    elif post.find("a", attrs={"data-testid": "outbound-link"}):
        content = (
            "[link]: "
            + post.find("a", attrs={"data-testid": "outbound-link"}).attrs["href"]
        )
    elif post.find("img"):
        content = "[img]: " + post.find("img").attrs["src"]
    else:
        content = "not provide"

    # check topic or content match user input
    no_match = True
    for i in range(len(keywords.split())):
        keyward = keywords.split()[i].lower()
        keyward_re1 = " " + keyward + " "
        keyward_re2 = "^" + keyward + " "
        keyward_re3 = " " + keyward + "$"
        if (
            re.search(keyward_re1, content.lower())
            or re.search(keyward_re2, content.lower())
            or re.search(keyward_re3, content.lower())
        ):
            no_match = False
            break
        if (
            re.search(keyward_re1, topic.lower())
            or re.search(keyward_re2, topic.lower())
            or re.search(keyward_re3, topic.lower())
        ):
            no_match = False
            break
        no_match = True

    if no_match:
        continue

    # author
    try:
        author = post.find("a", attrs={"data-testid": "post_author_link"}).text
        author = re.search("[^u/].*", author).group()
    except:
        continue

    # timestamp
    timestamp = ""
    try:
        timestamp_text = post.find("a", attrs={"data-testid": "post_timestamp"}).text
        timestamp_text = re.search("[0-9]*", timestamp_text).group()
        timestamp = datetime.now() - timedelta(hours=int(timestamp_text))
        timestamp = timestamp.strftime("%Y/%m/%d %H:00")
    except:
        continue

    # comment number
    try:
        comment_number = post.find("div", attrs={"data-click-id": "body"}).text
        comment_number = re.search("votes.*comments", comment_number).group()
        comment_number = comment_number[5:-8]

        if "k" in comment_number:
            comment_number = re.search("[0-9.]*", comment_number)
            comment_number = int(float(comment_number.group()) * 1000)
        else:
            comment_number = int(comment_number)
    except:
        continue

    # write to csv file
    post_id += 1
    post_line = [post_id, topic, author, content, timestamp, comment_number]
    with open(filename, "a", newline="", encoding="utf-8-sig'") as f:
        writer = csv.writer(f)
        writer.writerow(post_line)


print(f"\nsearch for {len(posts)} posts and found {post_id} matches")
