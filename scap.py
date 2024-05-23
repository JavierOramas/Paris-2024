from bs4 import BeautifulSoup
import requests

# URL of the page to scrape
url = 'https://www.besoccer.com/competition/teams/summer_olympics'

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Find all li items within elements with class 'panel-body table-list'
li_items = soup.select('.panel-body.table-list div')

teams = {}
# Print the href attribute of each a tag within the li items
for li in li_items:
    a_tag = li.find('a')
    if a_tag and 'href' in a_tag.attrs:
        team_name = a_tag['href'].split("/")[-1]
        teams[team_name] = { "url": a_tag['href']}

# for country, team in teams.items():
    


