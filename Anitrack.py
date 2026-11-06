from bs4 import BeautifulSoup
import requests
import json
import datetime
import time

user = input("Enter MAL username (default: Satellamoon): ") or "Satellamoon"
#user = "Satellamoon"
url = f"https://myanimelist.net/animelist/{user}?status=1"

start_time = time.time()
response = requests.get(url)
end_time = time.time()

if response.status_code == 200:
  elapsed_time = round(end_time - start_time, 2)
  print(f" MAL Request successful! Time taken: {elapsed_time} seconds. \n")
  
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

  # print(infodict[1])
  # for i in infodict:
  #     try:
  #         if (i['anime_title_eng'] == ''): 
  #             print(f"{i['anime_title']}: {i['anime_id']}")
  #         else:
  #             print(f"{i['anime_title_eng']}: {i['anime_id']}")
  #     except:
  #         print("fucking theta")
  
elif response.status_code == 404:
  print(f"Wrong username? Try again.")
else:
  print(f"GG ip ban. {response.status_code}")


# ---------- API ----------
start_time = time.time()

# myanimelist id -> anilist request
url = 'https://graphql.anilist.co'

query = ''' 
query Query($idMalIn: [Int], $type: MediaType) {
  Page {
    media(idMal_in: $idMalIn, type: $type) {
      idMal
      title {
        english
        romaji
      }
      airingSchedule(notYetAired: true, perPage: 1) {
        nodes {
          airingAt
          episode
          timeUntilAiring
        }
      }
    }
  }
}
'''

all_mal_ids = [i["anime_id"] for i in infodict]

hasAiringShows = False
chunk_size = 50

for i in range(0, len(all_mal_ids), chunk_size):
  chunk = all_mal_ids[i:i + chunk_size]

  variables = {
      "idMalIn": chunk,
      "type": "ANIME"
  }

  response = requests.post(url, json={'query': query, 'variables': variables})
    #53065 bisque doll
    #55690 dangers in <3

  if response.status_code == 200:
    # json output -> python dict
    data = response.json()

    # Check if GraphQL returned an error for this specific anime
    if 'errors' in data:
      print(f"GraphQL Error on chunk: {data['errors'][0]['message']}")
      continue
    
    media_list = data['data']['Page']['media']

    for media in media_list:
      if media['airingSchedule'] and media['airingSchedule']['nodes']:    # Takes timeUntilAiring(in seconds) and prints in readable format
        hasAiringShows = True
        
        #time
        duration = datetime.timedelta(seconds=media['airingSchedule']['nodes'][0]['timeUntilAiring'])
        days = duration.days
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        #weekday
        date = datetime.datetime.fromtimestamp(media['airingSchedule']['nodes'][0]['airingAt'])

        title = media['title'].get('english') or media['title']['romaji']
        print(f"{title} | ep {media['airingSchedule']['nodes'][0]['episode']}")
        print(f"Time until airing: {days} days, {hours} hours, and {minutes} minutes.")
        print(f"{date.strftime('%A')} {date.strftime('%I:%M %p')}\n")
  else:
    print(f"Shit code, try again: {response.status_code}")

  # Pause betwen chunks to stay under 90 requests/minute
  time.sleep(1.5)

if not hasAiringShows:
  print("No currently airing shows found in your list.")

end_time = time.time()
elapsed_time = round(end_time - start_time, 2)
print(f" API Request successful! Time taken: {elapsed_time} seconds. \n")