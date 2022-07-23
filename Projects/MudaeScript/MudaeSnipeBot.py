import os,threading
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.keys import Keys
from time import sleep
from dotenv import load_dotenv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

##################################################################################

#scroll to the end
def scrollDown():
    threading.Timer(5.0, scrollDown)
    a = driver.find_elements_by_xpath("//li")[-1]
    driver.execute_script("return arguments[0].scrollIntoView();",a)

# checks if chars in list are worht reacting
def checkItem(currList,charsKakera):
    for elem in currList:
        if (elem in charsSet) or (int(charsKakera) >= 900):
            u = elem.find_element_by_xpath(".//ancestor::li")
            driver.execute_script("return arguments[0].scrollIntoView();",u)
            sleep(0.5)
            u.click()
            sleep(0.5)
            v = u.find_element_by_xpath("./div/div[3]//div[@class='button-3bklZh']")
            sleep(0.5)
            v.click()
            sleep(0.5)
            r = driver.find_element_by_class_name("input-2FSSDe").send_keys("moon")
            g = driver.find_element_by_class_name("input-2FSSDe").send_keys(Keys.ENTER)

#every hour: roll cards , if good/rare go to checkItem()
def rollingCards():
    threading.Timer(3600.0,rollingCards).start()
    cardList = []
    currentLenghtOfCards = driver.find_elements_by_xpath("//div[@class='grid-1aWVsE']/div/span")
    for i in range(10):
        try:
            rollCommand = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/form/div/div/div/div[1]/div/div[3]/div[2]/div")
            sleep(2)
            rollCommand.send_keys("$ma")
            rollCommand.send_keys(Keys.ENTER)
            card = driver.find_elements_by_xpath("//div[@class='grid-1aWVsE']/div/span")[-1]
            sleep(1)
            newLength = driver.find_elements_by_xpath("//div[@class='grid-1aWVsE']/div/span")
            if len(currentLenghtOfCards) == len(newLength):
                break
            driver.execute_script("return arguments[0].scrollIntoView();",card)
            # last Li elem
            lastLi = card.find_element_by_xpath(".//ancestor::li")
            # Character's strongness
            kakera = lastLi.find_element_by_tag_name("strong")
            kakeraOfChar = kakera.text
            cardName = card.text
            cardList.append(cardName)
            checkItem(cardList,kakeraOfChar)
            cardList = []
        except Exception:
            break

# snipes other people cards if they are currently rolling     
def checkItemForSniping(currList):
    for character in currList:
        # moving to element before even reaching the god damn element
        if character.text in charsSetCopy and character.text != '':
            u = character.find_element_by_xpath(".//ancestor::li")
            sleep(1)
            ActionChains(driver).move_to_element(u).perform()
            character.click()
            v = u.find_element_by_xpath("./div/div[3]/div[@class='buttons-3dF5Kd container-2gUZhU isHeader-2bbX-L']")
            sleep(1)
            p = v.find_element_by_xpath("./div/div[@class='button-3bklZh']")
            p.click()
            sleep(1)
            t = driver.find_element_by_class_name("input-2FSSDe")
            g = driver.find_element_by_class_name("input-2FSSDe").send_keys(Keys.ENTER)
            charsSetCopy.remove(character.text)

#dynamic list that changes every few seconds, to collect last 5 rolled to snipe check
def snipeCards():
    threading.Timer(5.0,snipeCards).start()
    while True:
        charName = []
        currentElement = driver.find_elements_by_xpath("//div[@class='grid-1aWVsE']/div/span")
        slicedList = currentElement[-5:]
        checkItemForSniping(slicedList)
        break

##################################################################################
chars = open("MudaeTop400.txt").readlines()
character = []

for i in chars:
    b = i.split("\n")
    character.append(b[0])

# for fast checking
charsSet = set(character)
charsSetCopy = charsSet.copy()

PATH = "C:\Program Files (x86)\chromedriver.exe" 
load_dotenv("Data.env")
email = os.getenv("NAME")
pw = os.getenv("PW")
driver = webdriver.Chrome(PATH)
driver.get("https://www.discord.com")
sleep(2)

##################################################################################

try:
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//div/a[contains(text(), 'Login')]")))
    element.click()
except NoSuchElementException:
    print("Not Found")

driver.maximize_window()

sleep(1)
#Login into Discord (Webbrowser)
driver.find_element_by_xpath("//input[contains(@name, 'email')]").send_keys(email)
driver.find_element_by_xpath("//input[contains(@name, 'password')]").send_keys(pw)
driver.find_element_by_xpath("//div[contains(text(), 'Login')]").click()
sleep(2)

#click Mudae Server and go to channel (not dynamic, only for my settings/servers)
try:
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,"//div[@data-dnd-name ='Konohagakure']")))
    element.click()
except NoSuchElementException:
    print("Not Found")

sleep(1)

try:
    driver.find_element_by_xpath("//div[contains(text(),'Got it')]").click()
except Exception:
    pass

sleep(2)
driver.find_element_by_xpath("//div[@data-dnd-name ='mudae-games']").click()
sleep(2)

scrollDown()
sleep(1)
rollingCards()
snipeCards()


# sleep(2)
# driver.quit()