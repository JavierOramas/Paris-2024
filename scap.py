from bs4 import BeautifulSoup
import requests

def save_lineup():
    with open('lineups.tex' , 'a') as f:
        f.write(f'{link} \n')
        f.write("-------------------------------------------------------------")
        for player in player_names:
            f.write(player)

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
# Get all href
team_link = [team['url'] for team in teams.values()]
link = team_link[0]
response = requests.get(link)
soup = BeautifulSoup(response.content , 'html.parser')
menu_links = soup.find_all('a', class_="menu-item")
for option in menu_links:
    if "Squad" in option:
        squad_link = option['href']
response = requests.get(squad_link)
soup = BeautifulSoup(response.content , 'html.parser')
competicion = soup.find('select' , id = "competition")
competicion_value = [option['value'] for option in competicion.find_all('option')]
url = competicion_value[0]
response = requests.get(url)
soup = BeautifulSoup(response.content , 'html.parser')
print(soup)

player_names = [td.get_text() for td in soup.find_all('td', class_='name')]

# Hace falta scrapear por las competiciones y quedarse con el squad mas reciente guardado
