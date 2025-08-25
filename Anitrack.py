from bs4 import BeautifulSoup
import requests
import json

url = "https://myanimelist.net/animelist/Hapadisa?status=7"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', 'list-table')
    #print(table)
    if table: # Always check if the element was found
        info = table['data-items']
        #print(type(info))
    else: 
        print("Where table")
    
    infodict = json.loads(info)
    #print(infodict[19])
    
    for i in infodict:
        try:
            if (i['anime_title_eng'] == ''):
                print(i['anime_title'])
            else:
                print(i['anime_title_eng'])
        except:
            print("fucking theta")

else:
    print(f"GG ip ban. {response.status_code}")
