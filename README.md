# AniTrack 
Ever tired of tracking when each of your favorite shows air? AniTrack does it for you! AniTrack automatically knows what shows you are currently watching through MyAnimeList (MAL) and tells you exactly when each one airs.

P.S Make sure your MAL is updated for this program to work properly!

## Built With
**Libraries:**
- `requests`
- `BeautifulSoup`

**APIs & Tech:**
- AniList API
- GraphQL 

## How does it work?
1. **Fetch:** Scrapes the user's "Currently Watching" list directly from MyAnimeList.
2. **Process:** Parses the scraped data and matches the shows to the AniList GraphQL API.
3. **Display:** Retrieves the exact release schedules and countdowns for upcoming episodes.

## Purpose
While watching anime, I always wanted to stay up to date with the most recent episodes (mostly to avoid spoilers!), but I have a very short-term memory when it comes to airing dates TwT. 

I designed this app to help myself and others with a similar problem. A nice program for a constant inconvenience! :)

Along with solving this problem, building AniTrack helped me level up my backend coding skills. Some notable takeaways:
- **Web Scraping:** Extracting live data from web pages.
- **Data Parsing:** Navigating long tables and deeply nested JSON dictionaries.
- **API Optimization:** Implementing GraphQL batching to eliminate network overhead and drastically speed up execution time.
- **Defensive Programming:** Writing safe fallbacks for missing data or request failures.
- **AI-Assisted Workflow:** Leveraged AI tools to rapidly navigate and debug complex GraphQL structures.
