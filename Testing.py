import requests
import json
import pprint
import datetime

# Here we define our query as a multi-line string
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
  'idMal': 53065,
  "notYetAired": True,
  "perPage": 2,
  "type": "ANIME",
}
#53065 bisque doll
#55690 dangers in <3

url = 'https://graphql.anilist.co'

# Make the HTTP Api request
response = requests.post(url, json={'query': query, 'variables': variables})

# Check if the request was successful 
    # Check if bricked
if response.status_code == 200:
    # Print the JSON response in a readable format
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