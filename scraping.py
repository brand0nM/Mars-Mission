# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=True)

def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='headerimage fade-in').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url


def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


def hemisphere():
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    Mars_soup = soup(html, 'html.parser')
    img_url_rel = Mars_soup.find_all('a', class_='itemLink product-item')
    
    hemisphere_image_urls = {'title':[], 'low_res': [], 'high_res': []} # Create a list to hold the images and titles.
    for i in range(len(img_url_rel)):
        browser.visit(url)
        try:
            hemisphere_image_urls['title'].append(img_url_rel[i].find('img').get('alt').replace(' Enhanced thumbnail',''))
            hemisphere_image_urls['low_res'].append(url + img_url_rel[i].find('img').get('src'))
            browser.visit(url + img_url_rel[i]['href'])
            pic_soup = soup(browser.html, 'html.parser')
            pic_link = pic_soup.find('img', class_='wide-image').get('src')
            hemisphere_image_urls['high_res'].append(url + pic_link)
        except:
            x = "not a link"
        
    hemisphere = pd.DataFrame(hemisphere_image_urls)
    
    return hemisphere


def scrape_all():
    news_title, news_paragraph = mars_news(browser)
    hemisphere_df = hemisphere()
    tit = hemisphere_df["title"].to_list()
    pic = hemisphere_df["high_res"].to_list()

    tit_pic = []
    for i in range(len(tit)):
        tit_pic.append({"title": tit[i], "url": pic[i]})

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere": tit_pic}

    # Stop webdriver and return data
    browser.quit()
    return data


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

