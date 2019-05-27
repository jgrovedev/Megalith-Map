## Megalith-Map
Marked locations of megalithic sites around the world with informational popups. 

## Motivation
This was an exercise in scraping data from a website and compiling into a map.
 
## Screenshots
![screenshot](https://github.com/jgrovedev/Megalith-Map/blob/master/capture1.PNG)
![screenshot](https://github.com/jgrovedev/Megalith-Map/blob/master/capture2.PNG)

## Tech/framework used
<b>Built with</b>
- [Python](https://www.python.org/) 
- [Pandas](https://pandas.pydata.org/)
- [Folium](https://python-visualization.github.io/folium/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Geocoder](https://geocoder.readthedocs.io/)
- [JSON](https://docs.python.org/3/library/json.html)
- [CSV](https://docs.python.org/3/library/csv.html)
- [Requests](https://pypi.org/project/requests/2.7.0/)

## Features
Users can navigate the map and click markers that will display a popup with information.

## How to use?
Run "data_scrape.py" and enter the "scrape" command. This will begin the process of scraping the data from the website and finding the coordinates. Two files will be created. One file will be named 'Megalith Sites Completed.csv' which has no missing data and another file will be created called "Megalith Sites Null Data.csv" which has missing data that needs to be found via some other source. Once the data is found and added to the "Megalith Sites Null Data.csv" rename the file to "Megalith Sites Null Data Completed.csv" and "data_scrape.py" once more but enter the "merge" command. This will merge both "Megalith Sites Completed.csv" and "Megalith Sites Null Data Completed.csv" into one file called "Megalith Sites.csv" which will now be a complete dataset. 

Next, run "megalith_map.py" to create the interactive map.

Note: All information scraped is from https://www.megalithicbuilders.com
