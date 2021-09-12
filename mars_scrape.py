import traceback
import sys
from bs4 import BeautifulSoup as bs4
import pandas as pd 
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import urls


class ChromeBrowser(object):

    def __init__(self, url):
        self.url = url

    def __enter__(self):
        executable_path = {'executable_path': ChromeDriverManager().install()}
        self.browser = Browser('chrome', **executable_path, headless=False)
        self.browser.visit(self.url)
        return self.browser

    def __exit__(self, ex_type, val, tb):
        if (ex_type is not None):
            traceback.print_exception(ex_type, val, tb)
        if (self.browser is not None):
            self.browser.quit()
        return True

# Function that returns the title and summary text from nasa website
def get_news(url):

    news_title = ""
    news_p = ""

    with ChromeBrowser(url) as browser: 
        html = browser.html
        soup = bs4(html, "html.parser")
        news_title = soup.find('div', class_='content_title').text
        news_p = soup.find('div', class_='article_teaser_body').text

    return [news_title, news_p]

# Test for function
# news = get_news(urls.nasa_news)
# for n in news:
    # print(n)
    # print("----------------------")

def get_image(url):

    image_url = ""

    with ChromeBrowser(url) as browser:
        html = browser.html
        soup = bs4(html, "html.parser")
        browser.links.find_by_partial_text("FULL IMAGE").click()
        html = browser.html
        soup = bs4(html, "html.parser")
        image_url = url.replace("index.html", soup.find(class_="fancybox-image")["src"])
    
    return image_url

# Test for function
# image_url = get_image(urls.mars_images)
# print(image_url)
# print("----------------------")

# Returns an Earth vs. Mars general comparison 
def get_comparison(url):
    with ChromeBrowser(url) as browser:
        mars_facts_frame = pd.read_html(browser.html, match="Mars")[0]
        mars_facts_frame = mars_facts_frame.set_index("Mars - Earth Comparison", drop=True)
        mars_facts_frame.columns = [col.replace(":","") for col in mars_facts_frame.columns]
        return mars_facts_frame

# Test for function
# df = get_comparison(urls.mars_facts)
# print(df)
# print("----------------------")

# Returns only Mars facts
def get_mars_facts(url):
    with ChromeBrowser(url) as browser:
        mars_facts_frame = pd.read_html(browser.html, match="Mars")[0]
        mars_facts_frame = mars_facts_frame.set_index("Mars - Earth Comparison", drop=True)
        mars_facts_frame.columns = [col.replace(":","") for col in mars_facts_frame.columns]
        mars_facts_frame.drop('Earth', axis=1, inplace=True)
        return mars_facts_frame

# Test for function
# df = get_mars_facts(urls.mars_facts)
# print(df)
# print("----------------------")

def get_hemisphere_images(url):

    image_urls = []

    with ChromeBrowser(url) as browser:
        html = browser.html
        soup = bs4(html, "html.parser")
        res = soup.find(class_="result-list").find_all(class_="item")
        for r in res: 
            hemi = {}
            hemi["title"] = r.find("h3").text
            browser.links.find_by_partial_text(hemi["title"]).click()
            html = browser.html
            soup = bs4(html, "html.parser")
            hemi["img_url"] = urls.astro_url + soup.find(class_="wide-image")["src"]
            image_urls.append(hemi)
            browser.back()

    return image_urls

image_urls = get_hemisphere_images(urls.mars_hemispheres)
for url in image_urls:
    print(url)
print("----------------------")