from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

 
with open ("lineups.tex" , 'r') as f:
    lines = f.readlines()
    players_names = [line for line in lines if line != '------------------------------------------------------------- \n']
    players_names = [line for line in players_names if 'htt' not in line]
    players_names = [player[0:-1] for player in players_names]
 
driver = webdriver.Firefox()
driver.get('https://www.sofascore.com/')
with open("player_stats.tex" , 'w') as f:
    for player in players_names: 
        time.sleep(2)
        search_box = driver.find_element(By.XPATH , '//*[@id="__next"]/header/div[1]/div/div/div[2]/div/form/input')
        search_box.clear()
        search_box.send_keys(player)


        
        time.sleep(5)
        player_link = driver.find_element(By.XPATH , '//*[@id="__next"]/header/div[1]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/a').get_attribute('href')
        print(player_link)

        
        driver.get(player_link)

        time.sleep(3)
        try:
            f.write(f'{player}  {driver.find_element(By.XPATH , '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]').text} \n')
            print(f'{player}  {driver.find_element(By.XPATH , '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]').text} \n')
            try:
                if (driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[5]/div[2]').text == 'G' or driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[4]/div[2]').text == "G" or driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[3]/div[2]').text == "G"):
                    position = 'G'
                    f.write(f'{position} \n')
                    print(f'{position} \n')
                elif (driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[5]/div[2]').text == 'D' or driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[4]/div[2]').text == "D" or driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[3]/div[2]').text == "D"):
                    position = 'D'
                    f.write(f'{position} \n')
                    print(f'{position} \n')
                elif (driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[5]/div[2]').text == 'M' or driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[4]/div[2]').text == "M" or driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[3]/div[2]').text == "M"):
                    position = 'M'
                    f.write(f'{position} \n')
                    print(f'{position} \n')
                elif (driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[5]/div[2]').text == 'F' or driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[4]/div[2]').text == "F" or driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[3]/div[2]').text == "F"):
                    position = 'F'
                    f.write(f'{position} \n')
                    print(f'{position} \n')
            except Exception as e:
                f.write("No position info \n")
                print("No position info")
                f.write(e)
            if position == 'G':
                sav = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/div/div[1]/div[2]/div[3]/div/div[2]/div/div[1]/div/div/div').text
                f.write(f' sav : {sav} \n')
                print(f' sav : {sav} \n')
                ant = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[3]/div/div[2]/div/div[2]/div/div/div').text
                f.write(f' ant : {ant} \n')
                print(f' ant : {ant} \n')
                tac = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[3]/div/div[2]/div/div[3]/div/div/div').text
                f.write(f' tac : {tac} \n')
                print(f' tac : {tac} \n')
                bal = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[3]/div/div[2]/div/div[4]/div/div/div').text
                f.write(f' bal : {bal} \n')
                print(f' bal : {bal} \n')
                aer = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[3]/div/div[2]/div/div[5]/div/div/div').text
                f.write(f' aer : {aer} \n')
                print(f' aer : {aer} \n')
            else:
                att = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/div/div[1]/div[2]/div[3]/div/div[2]/div/div[1]/div/div/div').text
                f.write(f' att : {att} \n')
                print(f' att : {att} \n')
                tec = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[3]/div/div[2]/div/div[2]/div/div/div').text
                f.write(f' tec : {tec} \n')
                print(f' tec : {tec} \n')
                tac = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[3]/div/div[2]/div/div[3]/div/div/div').text
                f.write(f' tac : {tac} \n')
                print(f' tac : {tac} \n')
                de = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[3]/div/div[2]/div/div[4]/div/div/div').text
                f.write(f' de : {de} \n')
                print(f' de : {de} \n')
                cre = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/div[1]/div[2]/div[3]/div/div[2]/div/div[5]/div/div/div').text
                f.write(f' cre : {cre} \n')
                print(f' cre : {cre} \n')
        except:
            f.write("No data")
            print("No data")
        
        f.write('--------------------------')
        f.write('\n')
        print('--------------------------')
        print('\n')
        driver.get('https://www.sofascore.com/')
 
#driver.quit()


