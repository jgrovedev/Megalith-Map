import folium
import pandas as pd
import json

# READS DATA FROM CSV
df_msites = pd.read_csv('Megalithic Sites.csv')

# CREATES A FOLIUM MAP
m = folium.Map(location=[20, 0], tiles="stamenwatercolor", zoom_start=2)

# PLOTS EACH ROW IN THE .csv
for i in range(0,len(df_msites)):
    html = ('<font face=\"Arial"><center><h1>' + df_msites.iloc[i]['Sites'] + '</h1></center><br>'
            '<center><b>Country: </b>' + df_msites.iloc[i]['Country'] + '&nbsp&nbsp&nbsp&nbsp' +
            '<b>Latitude: </b>' + str(df_msites.iloc[i]['Latitude'].round(decimals=4)) + '&nbsp&nbsp&nbsp&nbsp' +
            '<b>Longitude: </b>' +  str(df_msites.iloc[i]['Longitude'].round(decimals=4)) + '&nbsp&nbsp&nbsp&nbsp' + '</center></br>'
            '<p>' + df_msites.iloc[i]['Paragraph'] + '</p></br></font>'
            '<img src=' + df_msites.iloc[i]['Image Source'] + '>')


    iframe = folium.IFrame(html=html, width=500, height=300)
    popup = folium.Popup(iframe, max_width=2650)
    folium.Marker([df_msites.iloc[i]['Latitude'], df_msites.iloc[i]['Longitude']], 
                   popup=popup, tooltip=(df_msites.iloc[i]['Sites'] + ' - ' + df_msites.iloc[i]['Country']),
                   icon=folium.Icon(color='black', icon='flag')).add_to(m)

m.save('Megalith Map.html')
print('Map created')