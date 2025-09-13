from bs4 import BeautifulSoup
import requests
import json
import datetime

user = input("Enter MAL username: ")
print("\n")
url = f"https://myanimelist.net/animelist/{user}?status=1"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', 'list-table')
    #print(table)
    if table: # Always check if the element was found
        info = table['data-items']
        #print(type(info))
    else: 
        print("Missing table")
    
    #json string from html table -> python dict
    infodict = json.loads(info)

    #print(infodict[1])
    # for i in infodict:
        # try:
        #     if (i['anime_title_eng'] == ''): 
        #         print(f"{i['anime_title']}: {i['anime_id']}")
        #     else:
        #         print(f"{i['anime_title_eng']}: {i['anime_id']}")
        # except:
        #     print("fucking theta")
        
elif response.status_code == 404:
    print(f"Wrong username? Try again.")
else:
    print(f"GG ip ban. {response.status_code}")


# myanimelist id -> anilist request
url = 'https://graphql.anilist.co'

query = ''' 
query Query($notYetAired: Boolean, $perPage: Int, $idMal: Int, $type: MediaType) {
  Media(idMal: $idMal, type: $type) {
    airingSchedule(notYetAired: $notYetAired, perPage: $perPage) {
      nodes {
        airingAt
        episode
        timeUntilAiring
      }
    }
    title {
      english
      romaji
      userPreferred
  }
  }
}
'''
variables = {
"notYetAired": True,
"perPage": 1,
"type": "ANIME",
}

for i in infodict:
  variables["idMal"] = i["anime_id"]
  #53065 bisque doll
  #55690 dangers in <3

  response = requests.post(url, json={'query': query, 'variables': variables})

  # Check if bricked
  if response.status_code == 200:
    # json output -> python dict
    data = response.json()
    if data['data']['Media']['airingSchedule'] and data['data']['Media']['airingSchedule']['nodes']:    # Takes timeUntilAiring(in seconds) and prints in readable format
      #time
      duration = datetime.timedelta(seconds=data['data']['Media']['airingSchedule']['nodes'][0]['timeUntilAiring'])
      days = duration.days
      hours, remainder = divmod(duration.seconds, 3600)
      minutes, seconds = divmod(remainder, 60)

      #weekday
      date = datetime.datetime.fromtimestamp(data['data']['Media']['airingSchedule']['nodes'][0]['airingAt'])

      print(f"{data['data']['Media']['title']['english']} | ep {data['data']['Media']['airingSchedule']['nodes'][0]['episode']}")
      print(f"Time until airing: {days} days, {hours} hours, and {minutes} minutes.")
      print(f"{date.strftime('%A')} {date.strftime('%I:%M %p')}")
      print("\n")
  else:
    print(f"Shit code, try again: {response.status_code}")
