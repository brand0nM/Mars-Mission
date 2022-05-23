# Mars-Mission
## Overview
Create a web application that store's scraped Nasa data and has a button to update.

### Purpose
First, create scraping.py which uses BeautifulSoup and Splitter to automate the scraping process, storing its results in a python dictionary; to find the required components use chrome's developer tools and identify HTML elements. Then create the mars_app database in mongo to store the dictionary. Finally, query the NoSQL database to retrieve Nasa's data and store it in the flask application app.py, with templates/index.html (flask requires the folder templates) to store our website's structure.

## Website
<img width="1438" alt="Screen Shot 2022-05-23 at 11 08 05 AM" src="https://user-images.githubusercontent.com/79609464/169873100-e179e480-372d-4e11-811c-bf2de0f69815.png">
<img width="1440" alt="Screen Shot 2022-05-23 at 11 08 29 AM" src="https://user-images.githubusercontent.com/79609464/169872174-a339f12f-3583-4511-8dc8-c1653e44244a.png">
<img width="1426" alt="Screen Shot 2022-05-23 at 11 08 41 AM" src="https://user-images.githubusercontent.com/79609464/169872196-e977d06f-bcad-4432-8c8f-41c96d6a67bc.png">

### Challenges and Difficulties
For the sake of index.html's list comprehension (lines 65-75), inserting data to mongo required a specific order- different than our python dataframe; to rectify this, lines 111-116 were added to scraping.py to convert the dictionaries structure- a simpler method could exist.

## Summary
We've used html to store scrapped data and flask to activate the website (scraping new data at the press of a button).
