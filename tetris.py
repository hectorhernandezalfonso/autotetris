from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


class Jugador:
    def __init__(self, driver):
        self.posicion = [0, 0]  # Inicializa la posición del jugador en (0, 0)
        self.orientacion = 0     # Inicializa la orientación del jugador
        self.driver = driver  # Store the WebDriver instance

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

    def analizar(self):
        print("analizar")
    
    def enviar(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.SPACE).perform()
        print("enviado")


def main():
    driver = webdriver.Firefox()
    driver.get("https://tetr.io/")

    try:
        # Wait for the 'JOIN' button to be clickable (ensure tetr.io is loaded)
        join_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "entry_button"))
        )
        join_button.click()

        # Wait for the 'SOLO' element to be clickable
        solo_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "play_solo"))
        )
        solo_button.click()

        lines_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "game_40l"))
        )
        lines_button.click()

        start_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "start_40l"))
        )
        start_button.click()
        print("Clicked 'SOLO' button successfully!")

        # Create an instance of Jugador with the driver object
        jugador = Jugador(driver)
        time.sleep(10)

        # Call the derecha method to press the right arrow key
        jugador.derecha()
        time.sleep(1)
        jugador.derecha()
        time.sleep(1)
        jugador.derecha()
        time.sleep(1)
        jugador.izquierda()
        time.sleep(1)
        jugador.izquierda()
        time.sleep(1)
        jugador.izquierda()
        time.sleep(1)
        jugador.rotar()
        time.sleep(1)
        jugador.guardar()
        time.sleep(1)
        jugador.enviar()
        time.sleep(4)


    finally:
        driver.quit()  # Close the browser window after execution

if __name__ == "__main__":
    main()
