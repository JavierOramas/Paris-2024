from bs4 import BeautifulSoup
import requests
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Firefox()
driver.get("https://www.besoccer.com/competition/teams/summer_olympics")
 
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/button[2]/span")))

 
cookies_botom = driver.find_element(By.XPATH , '/html/body/div[1]/div/div/div/div[2]/div/button[2]')
cookies_botom.click()
 
print("Cookies aceptadas")

driver.implicitly_wait(5)
teams = driver.find_elements(By.CLASS_NAME , "item-box")
team = [x for x in teams]

print(team)

for k in range(len(team)):
    
    driver.implicitly_wait(5)
    teams = driver.find_elements(By.CLASS_NAME , "item-box")
    team = [x for x in teams]

    team_link = team[k].find_element(By.TAG_NAME , "a").get_attribute('href')
    driver.get(team_link)

    driver.implicitly_wait(5)
    menu = driver.find_elements(By.CLASS_NAME , "menu-item")
    for item in menu:
        print(item.text)
        if item.text == 'SQUAD':
            squad_link = item.get_attribute('href')

    print(squad_link)

    driver.get(squad_link)

    
    from selenium.webdriver.support.ui import Select

    
    driver.implicitly_wait(5)
    competicions = driver.find_element(By.ID , 'competition')
    competicions = Select(competicions)
    competicions = competicions.options
    competicion = [x for x in competicions]

    print(competicion)
    
    player_names=[]
    season_2024 = False
    for i in range(len(competicion)):
        driver.implicitly_wait(5)
        competicions = driver.find_element(By.ID , 'competition')
        competicions = Select(competicions)
        competicions = competicions.options
        competicion = [x for x in competicions]
        print(competicion[i].text)
        competicion[i].click()

        time.sleep(10)

        seasons = driver.find_element(By.ID , 'season')
        seasons = Select(seasons)
        seasons = seasons.options
        season = [x for x in seasons]
        for j in range(len(season)):
            seasons = driver.find_element(By.ID , 'season')
            seasons = Select(seasons)
            seasons = seasons.options
            season = [x for x in seasons]
            print(season[j].text)
            if season[j].text == '2024':
                season_2024 = True
                player_names = [td.text for td in driver.find_elements(By.CLASS_NAME,'name')]
                break
        if season_2024:
            break
        time.sleep(5)

    
    with open('lineups.tex' , 'a') as f:
        f.write(f'{squad_link} \n')
        f.write("------------------------------------------------------------- \n")
        for player in player_names:
            f.write(player)
            f.write("\n")
    time.sleep(3)
    driver.get("https://www.besoccer.com/competition/teams/summer_olympics")    
    driver.implicitly_wait(5)
    teams = driver.find_elements(By.CLASS_NAME , "item-box")
    team = [x for x in teams]

