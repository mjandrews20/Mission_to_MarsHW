from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import time
import datetime as dt

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    mars_dict = {}
# mars scrape
    browser=init_browser()
    mars_url = 'https://mars.nasa.gov/news'
    browser.visit(mars_url)
    html = browser.html
    time.sleep(3)
    mars_soup = bs(html, 'html.parser')

    mars_title = mars_soup.find('div', {"class": "content_title"}).text
    #mars_title.text
    mars_pg = mars_soup.find('div', {"class": "article_teaser_body"}).text
    #mars_pg.text
#add to empty dictionary
    mars_dict['News Title'] = mars_title
    mars_dict['News Para'] = mars_pg

    image_soup = bs(html, 'html.parser')
    # click on full image button to get jpg for image then concatenate 
    #relative_image = image_soup.select_one('figure.lede a img')["src"]
    #relative_image

    #featured_image_url = 'https://www.jpl.nasa.gov' + relative_image
    #featured_image_url

    full_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(full_image_url)
    full_image = browser.find_link_by_partial_text("FULL IMAGE")
    time.sleep(3)
    full_image.click()
    time.sleep(3)
    more_info = browser.find_link_by_partial_text("more info")
    more_info.click()
    time.sleep(3)

    html = browser.html
    image_soup = bs(html, 'html.parser')

    relative_image = image_soup.select_one('figure.lede a img').get("src")
    relative_image

    featured_image_url = 'https://www.jpl.nasa.gov' + relative_image
    featured_image_url

    mars_dict['Mars Featured URL'] = featured_image_url
    
# twitter (weather) scrape
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    html = browser.html
    time.sleep(3)
    twitter_soup = bs(html, 'html.parser')
    weather = twitter_soup.find('p', class_= 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    mars_dict['Mars Weather'] = weather
    

    spacefacts_url = 'https://space-facts.com/mars/'
    browser.visit(spacefacts_url)
    html = browser.html
    time.sleep(3)
    spacefacts_soup = bs(html, 'html.parser')

    tables=pd.read_html(spacefacts_url)[0]
    tables

    html_table_string = tables.to_html()
    mars_dict['Mars Info Table'] = html_table_string
    
# hemisphere scrape
    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hem_url)
    html = browser.html
    time.sleep(3)

    hem_soup = bs(html, 'html.parser')

    hemi = hem_soup.find_all('div', class_='description')
    hemi

    hem_dict = []
    base_usgs_url = 'https://astrogeology.usgs.gov'
    for hem in hemi:
        title = hem.find('h3').text
        target_url = hem.find("a",class_ = "itemLink product-item")['href']
        picture_url = base_usgs_url + target_url
        browser.visit(picture_url)
        html = browser.html
        time.sleep(1)
        picture_soup = bs(html, 'html.parser')

        img = picture_soup.find('img', class_ = 'wide-image')['src']
        img_url = 'https://astrogeology.usgs.gov' + img

        hem_dict.append({'title': title, 'img_url':img_url})
    mars_dict['Hemisphere URL'] = hem_dict

    timenow = dt.datetime.utcnow()
    mars_dict["Date Time"] = timenow

#Change variable names below to match
    final_dict = {
        'News_Headline': mars_dict['News Title'],
        'News_Paragraph': mars_dict['News Para'],
        'Feature_Image_URL': mars_dict['Mars Featured URL'],
        'Mars_Current_Weather': mars_dict['Mars Weather'],
        'Mars_Facts_Table': mars_dict['Mars Info Table'],
        'Mars_Hemispheres': mars_dict['Hemisphere URL'],
        'Date_Time': mars_dict['Date Time']
    }

    browser.quit()
    return final_dict
