from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests as rq
import pandas as pd
import datetime as dt
import time
import re

browser = Browser("chrome", executable_path = "chromedriver", headless=False)

def scrape_all():
    browser = Browser('chrome', executable_path = 'chromerdriver', headless = False)
    news_title, news_p = mars_news(browser)


url='https://mars.nasa.gov/news/'
browser.visit(url)

browser.is_element_present_by_css('ul.item_list li.slide', wait_time=1)

html = browser.html
news_soup = BeautifulSoup(html,'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find('div',class_='content_title')

new_title = slide_elem.find('div', class_='content_title').get_text()

new_p = slide_elem.find('div', class_='article_teaser_body').get_text()

#JPL Space Images Returned

url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

full_img_elem = browser.find_by_id('full_image')
full_img_elem.click()

browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.find_link_by_partial_text('more info')
more_info_elem.click()

html = browser.html
img_soup = BeautifulSoup(html, 'html.parser')

img_url_rel = img_soup.select_one('figure.lede a img').get('src')
img_url_rel

img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


#Mars Weather

url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)

time.sleep(5)

html = browser.html
weather_soup = BeautifulSoup(html, 'html.parser')

mars_weather_tweet = weather_soup.find('div', attrs={'class':'tweet','data-name':'Mars Weather'})

try:
    mars_weather = mars_weather_tweet.find('p','tweet-text').get_text()
    mars_weather
    
except AttributeError:
    pattern = re.compile(r'sol')
    mars_weather = weather_soup.find('span', text=pattern).text
    mars_weather
    
#Mars Hemispheres

url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

hemisphere_image_urls = []

links = browser.find_by_css('a.product-item h3')

for i in range(len(links)):
    hemisphere = {}
    
    browser.find_by_css('a.product-item h3')[i].click()
    
    sample_elem = browser.find_link_by_text('Sample').first
    hemisphere['img_url'] = sample_elem['href']
    
    hemisphere['title'] = browser.find_by_css('h2.title').text
    
    hemisphere_image_urls.append(hemisphere)
    
    browser.back()

#Mars Facts

df = pd.read_html('https://space-facts.com/mars/')[0]

df.columns=['description','value']

df.to_html('Mars_Facts.png')

