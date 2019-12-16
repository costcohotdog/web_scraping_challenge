# Dependiencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests

def init_browser():
    # Prepare chromedriver
    # MUST USE CHROME 79
    executable_path = {'executable_path': 'C:/Users/Smili_000/Desktop/Bootcamp/web_scraping_challenge/chromedriver.exe'}
    return Browser('chrome', {'executable_path': 'C:/Users/Smili_000/Desktop/Bootcamp/web_scraping_challenge/chromedriver.exe'}, headless=False)


def scrape():
    browser = init_browser

    # Dictionary for holding scraped info
    mars_scraped_info = {}

    #####################################################
    # Mars News Title and Text
    #####################################################

    # Retrieve page
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    # Create soup object and parse first news article title/text
    news_soup = bs(browser.html, 'html.parser')
    mars_scraped_info['news_title'] = news_soup.find("div",class_="content_title").text.strip()
    mars_scraped_info['news_text'] = news_soup.find("div",class_="rollover_description").text.strip()


    #####################################################
    # Mars Image
    #####################################################

    # Retrieve page
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)

    # Create soup object
    img_soup = bs(browser.html, 'html.parser')

    # Get popup link
    img_page = 'https://www.jpl.nasa.gov' + str(img_soup.find('li', class_='slide').find('a')['data-link'])

    # Create soup object of popup page
    browser.visit(img_page)
    img_large_soup = bs(browser.html, 'html.parser')

    # Get large image link
    mars_scraped_info['img_large'] = 'https://www.jpl.nasa.gov' + str(img_large_soup.find('figure').find('a')['href'])

    # Close browser
    browser.quit()


    #####################################################
    # Mars Weather
    #####################################################

    # Retrieve page
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(weather_url)

    # Crete soup object and parse weather paragraph
    soup = bs(response.text, 'html.parser')
    mars_scraped_info['weather'] = soup.find('div', class_="js-tweet-text-container").find('p').text.split('hPapic')[0].rstrip()


    #####################################################
    # Mars Facts
    #####################################################

    # Mars facts table is static and implmented into the html


    #####################################################
    # Mars Hemispheres
    #####################################################

    # Retrieve mars hemispheres page and create soup object
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(hemispheres_url)
    soup = bs(response.text, 'html.parser')

    # Get url for each hemisphere page
    hemispheres_url_list = []

    for x in range(len(soup.find_all('div', class_='item'))):
        hemispheres_url_list.append('https://astrogeology.usgs.gov' + soup.find_all('div', class_='item')[x].find('a')['href'])

    # Create a list of dictionaries containing the title and img url for each hemisphere
    hemisphere_image_list = []

    for url in range(len(hemispheres_url_list)):
        
        hemisphere_image_dict = {}
        
        response = requests.get(hemispheres_url_list[url])
        soup = bs(response.text, 'html.parser')
        
        title = soup.find('title').text.split('Enhanced')[0].rstrip()
        img_url = soup.find('div', class_='downloads').find('a')['href']
        
        hemisphere_image_dict['title'] = title
        hemisphere_image_dict ['img_url'] = img_url
        
        hemisphere_image_list.append(hemisphere_image_dict)

    # Add hemisphere image list to scraped info dictionary
    mars_scraped_info['hemisphere_image_list'] = hemisphere_image_list


    return mars_scraped_info