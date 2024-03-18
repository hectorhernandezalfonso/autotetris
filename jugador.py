from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

class Jugador:
    def __init__(self):
        self.driver = 0  # Store the WebDriver instance

    def derecha(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ARROW_RIGHT).perform()
        print("Movido a la derecha")

    def izquierda(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ARROW_LEFT).perform()
        print("Movido a la izquierda")

    def rotar(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.UP).perform()
        print("rotar")

    def guardar(self):
        actions = ActionChains(self.driver)
        actions.send_keys("c").perform()
        print("Guardado")

    def enviar(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.SPACE).perform()
        print("enviado")

    def start_game(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://tetr.io/")
        join_button = WebDriverWait(self.driver, 100).until(
            EC.element_to_be_clickable((By.ID, "entry_button"))
        )
        join_button.click()

        solo_button = WebDriverWait(self.driver, 100).until(
            EC.element_to_be_clickable((By.ID, "play_solo"))
        )
        solo_button.click()

        lines_button = WebDriverWait(self.driver, 100).until(
            EC.element_to_be_clickable((By.ID, "game_40l"))
        )
        lines_button.click()

        start_button = WebDriverWait(self.driver, 100).until(
            EC.element_to_be_clickable((By.ID, "start_40l"))
        )
        start_button.click()
        time.sleep(6)
        self.driver.save_screenshot("tetris.png")
        time.sleep(4)

    def analizar(self, piezas, tablero, pieza_actual):
        
        print(tablero)
        print(piezas)
        print(pieza_actual)
        self.izquierda()
        self.izquierda()
        self.enviar()
        time.sleep(0.5)
        self.driver.save_screenshot("tetris.png")
        


