import bs4
import requests
import csv
import pandas as pd
import geocoder
import json

# CALLS DATAFRAME AND PRINTS OUT INFORMATION OF ITS CONTENTS
def dataframe_info(dataframe):
    print('***NUMBER OF ROWS x COLUMNS***\n',dataframe.shape,'\n')
    print('***NUMBER OF EMPTY DATA***\n',dataframe.isnull().sum(),'\n')
    print('***DATA TYPE***\n',dataframe.dtypes)
    print(dataframe.columns)

while True:
    command = input('Enter \"scrape" to begin data retreival or enter \"merge" to combine dataframes and export geojson.\n')
    if command == 'scrape':
        # GRABS WEBPAGE INFORMATION
        url = 'https://www.megalithicbuilders.com'
        html = requests.get(url).text
        soup = bs4.BeautifulSoup(html, 'html5lib')

        # PARSES NAMES OF MEGALITH SITES
        print('Parsing for site names...')
        site_names = []
        for i in soup.find_all('span', {'class' : 'g-menu-item-title'}):
            contents = i.text
            
            if '-' in contents:   
                    contents = contents.split(' - ')[1:]
                    mliths = ''.join(contents)
                    site_names.append(mliths)

        df_msites = pd.DataFrame({'Sites':site_names})
        print('Retreived ', len(site_names)-site_names.count(None), ' site names.\n')

        # CREATES A LATITUDE LONGITUDE, and COUNTRY CODE COLUMN
        print('Retreiving coordinates...')

        df_msites['Latitude'] = None
        df_msites['Longitude'] = None

        # LOOPS THROUGH CSV FILE AND FINDS LATITUDE AND LONGITUDE
        for i in range(0, len(df_msites), 1):
            geocode_result = geocoder.osm(df_msites.iloc[i,0])
            try:
                lat = geocode_result.latlng[0]
                lng = geocode_result.latlng[1]
                df_msites.iloc[i, df_msites.columns.get_loc('Latitude')] = lat
                df_msites.iloc[i, df_msites.columns.get_loc('Longitude')] = lng
            except:
                lat = None
                lng = None
                # print(df_msites.iloc[i,0], lat, lng)
        print('Retreived ', len(df_msites.dropna()),'/',len(site_names), ' sets of coordinates.\n')

        # PARSES LINK TO WEBSITE/COUNTRY
        print('Parsing country and urls...')
        site_country = []
        site_links = []
        for i in soup.find_all('a', {'class' : 'g-menu-item-container'}):
            contents = i.get('href')
            
            # disregards '#' and the blog/news link from results
            if contents != '#' and len(contents) > 5:
                link = url + contents
                site_links.append(link)     
                country = contents.split('/')
                country = country[2].title().replace('-', ' ')
                site_country.append(country)
                # print(link)
                # print(country)
        df_msites['Country'] = site_country
        df_msites['Site Links'] = site_links
        print('Retreived ', len(site_country)-site_country.count(None),'/',len(site_names), ' countries.')
        print('Retreived ', len(site_links)-site_links.count(None),'/',len(site_names), ' site links.\n')

        # PARSES ALL IMAGE SOURCES ON THE WEBSITE
        print('Parsing for image sources...')
        site_img = []
        for i in site_links:
            r = requests.get(i).text
            soup = bs4.BeautifulSoup(r, 'html5lib')
            try:
                img_page = soup.find('div', {'itemprop' : 'blogPost'}).find_all('img')
                img_src = img_page[0].get('src', '')        # ('src', '') returns an empty string if no 'src' exists
                img_gallery = soup.find('a', {'class':'sigProLink fancybox-gallery', 'href':True})
                if img_page:
                    if '.jpg' in img_src:
                        img_link = url + img_src
                        site_img.append(img_link)
                        # print(img_link)
                    elif img_gallery:
                        href = img_gallery.get('href', '')                
                        if '.jpg' in href:
                            img_link = url + href
                            site_img.append(img_link)
                            # print(img_link)
            except IndexError:
                    elem = None
                    site_img.append(elem)
                    # print('No images found')
        df_msites['Image Source'] = site_img
        print('Retreived ', len(site_img)-site_img.count(None),'/',len(site_names), ' image sources.\n')

        # PARSES SECOND PARAGRAPH OF EACH PAGE
        print('Parsing for site paragraphs...')
        site_para = []
        for i in site_links:
            r = requests.get(i).text
            soup = bs4.BeautifulSoup(r, 'html5lib')
            para = soup.find('div', {'class' : 'leading-0', 'itemprop' : 'blogPost'}).find_all('p')[1].text
            site_para.append(para)
            # print(para)
        df_msites['Paragraph'] = site_para
        print('Retreived ', len(site_para)-site_para.count(None),'/',len(site_names), ' paragraphs.\n')

        # CREATES TWO DATA FRAMES - ONE WITH NULL DATA AND ONE WITH COMPLETE DATA
        null_data = df_msites[df_msites.isnull().any(axis=1)]
        completed_data = df_msites.dropna()

        # EXPORTS DATA FRAMES TO CSV
        null_data.to_csv('Megalith Sites Null Data.csv', index=False, header=True)
        completed_data.to_csv('Megalith Sites Completed.csv', index=False, header=True)
        print('Data exported to .csv')
        
        if command == 'scrape':
            break

    elif command == 'merge':
        # MERGES MANUALLY FOUND DATA WITH COMPLETED DATA INTO ONE DATAFRAME & EXPORTS TO .CSV
        null_complete = pd.read_csv('Megalith Sites Null Data Completed.csv')            
        completed_data = pd.read_csv('Megalith Sites Completed.csv')

        frames = [null_complete, completed_data]
        df_msites = pd.concat(frames, sort=False)

        df_msites.to_csv('Megalithic Sites.csv', index=False, header=True)
        print('Data frames merged and exported to .csv')

        # CREATES A GEOJSON FILE
        def df_to_geojson(df, properties, lat='Latitude', lon='Longitude'):
            geojson = {'type':'FeatureCollection', 'features':[]}               # create a new python dict to contain our geojson data, using geojson format
            for _, row in df.iterrows():                                        # loop through each row in the dataframe and convert each row to geojson format
                feature = {'type':'Feature',
                        'properties': {},
                        'geometry':{'type':'Point',
                                    'coordinates':[]}}
                feature['geometry']['coordinates'] = [row[lon], row[lat]]       # fill in the coordinates
                for prop in properties:                                         # for each column, get the value and add it as a new feature property
                    feature['properties'][prop] = row[prop]
                geojson['features'].append(feature)                             # add this feature (aka, converted dataframe row) to the list of features inside our dict
            return geojson

        cols = ['Sites', 'Country', 'Site Links', 'Image Source', 'Paragraph']  # select which columns to add to properties in geojson
        geojson = df_to_geojson(df_msites, properties=cols)

        # EXPORTS TO GEOJSON FILE
        with open('Megalith Sites.json', 'w') as outfile:
            json.dump(geojson, outfile, indent=2)

        print('Geojson file created succesfully.')
        
        if command == 'merge':
            break
    
    else:
        print('Unknown command. Please enter scrape or merge.')
    
