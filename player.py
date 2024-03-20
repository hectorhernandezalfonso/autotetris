from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image

import time

import tetris

class bot:

    def __init__(self):
        self.orientation_columns = {
            "I": [4,6],
            "T": [4, 5, 4, 4],
            "O": [5],
            "L": [4, 5, 4, 4],
            "S": [4, 5],
            "J": [4, 5,4,4],
            "Z": [4,5],
        }

        self.pieces_indexes = {
            "I": 0,
            "T": 1,
            "O": 2,
            "L": 4,
            "S": 5,
            "J": 3,
            "Z": 6,
        }


        self.current_pieces = None
        self.current_pieces = []
        self.currentColumn = 4
        self.ai = tetris.AI(10, 20)
        self.moves = 0
        self.driver = webdriver.Firefox()
        self.driver.get("https://tetr.io/")
    

    def start_game(self):
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
        self.current_pieces = self.update_piece()
        self.get_next_piece()
        time.sleep(4)


    def get_color(self, image):
        # Get the dimensions of the image
        reference_colors = {
            'L': (192, 111, 62),  # Light orange
            'O': (213, 186, 82),  # Light yellow
            'J': (86, 69, 164),   # Dark blue
            'T': (163, 68, 153),  # Purple
            'S': (127, 172, 54),  # Light green
            'Z': (195, 62, 69),
        }
        width, height = image.size

        # Find the coordinates of the center pixel
        center_x = width // 2
        center_y = height // 2

        # Get the color of the center pixel
        center_pixel = image.getpixel((center_x, center_y))

        negro = center_pixel[0] + center_pixel[1] + center_pixel[2]

        if negro < 40:
            center_pixel = image.getpixel((center_x, center_y+10))

        
        # Define color thresholds with some tolerance for variations
        color_tolerances = {
            'L': (20, 20, 20),  # Tolerance for light orange
            'O': (20, 20, 20),  # Tolerance for light yellow
            'J': (20, 20, 20),  # Tolerance for dark blue
            'T': (20, 20, 20),  # Tolerance for purple
            'Z': (20, 20, 20),  # Tolerance for light green
            'S': (20,20,20)
        }

        # Classify color based on minimum distance to reference colors with tolerance
        min_distance = float(50)
        classified_color = None
        for reference_color, tolerance in color_tolerances.items():
            ref_red, ref_green, ref_blue = reference_colors[reference_color]
            distance = (
                abs(center_pixel[0] - ref_red) + abs(center_pixel[1] - ref_green) + abs(center_pixel[2] - ref_blue)
            )
            if distance < min_distance:
                min_distance = distance
                classified_color = reference_color

        # Handle cases where no color matches within tolerance (consider 'I' or other)
        
        #if negro < 40:
        #    return 'N'
        
        if min_distance > sum(tolerance):  # Directly sum the elements in the tuple
            classified_color = 'I'

        return classified_color

    def update_piece(self):
        self.driver.save_screenshot("tetris.png")
        screenshot = Image.open("tetris.png")
        resized_width = 800  # Adjust width as needed
        resized_height = 600  # Adjust height as needed

        resized_image = screenshot.resize((resized_width, resized_height))
        # Desired crop width and height
        
        left = 270
        up = 84
        right = 540
        low = 480
        tetris_completo = resized_image.crop((left, up, right, low))

        #tetris_completo.show()
        width, height = tetris_completo.size
        left = 0
        right=width
        up = 0
        low = height
        # CROP(LEFT, UPPER, RIGHT, LOWER)
        self.next_piece = tetris_completo.crop((right-68,up+15,right,low-85))

        aux_pieces = self.next_piece
        width, height = self.next_piece.size
        left = 0
        right=width
        up = 0
        low = height
        
        add = low/5
        #aux_pieces.show()


        pieces = []

        for i in range(5):
            piece = self.next_piece.crop((left, up+(i*add), right, up+((i+1)*add)))
            color = self.get_color(piece)
            if color == None:
                color = "I"
            pieces.append(color)
        return pieces
    

    def izquierda(self):
        time.sleep(1)
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ARROW_LEFT).perform()
        print("Movido a la izquierda")

    def derecha(self):
        time.sleep(1)
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ARROW_RIGHT).perform()
        print("Movido a la derecha")

    def enviar(self):
        time.sleep(1)
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.SPACE).perform()
        print("enviado")

    def guardar(self):
        actions = ActionChains(self.driver)
        actions.send_keys("c").perform()
        print("Guardado")

    
    def rotar(self, orientacion):
        time.sleep(1)
        actions = ActionChains(self.driver)
        for i in range(orientacion):
            actions.send_keys(Keys.UP).perform()
        
        print("rotar" + str(orientacion))
        print("BUG")
        print("orientation columns")
        print(self.orientation_columns)
        print("orientacion")
        print(orientacion)
        print("current_piece")
        print(self.current_piece)
        self.currentColumn = self.orientation_columns[self.current_piece][orientacion]


    def moveColumn(self, column):
        deltaColumns = column - self.currentColumn

        if (deltaColumns<0):
            for i in range(abs(deltaColumns)):
                self.izquierda()
        elif deltaColumns>0:
            for i in range(abs(deltaColumns)):
                self.derecha()

    
    def get_next_piece(self):
        """Gets the next tetromino piece and refills the list if empty.

        Args:
            self: An instance of the Tetris game class (or similar).

        Returns:
            The next tetromino piece (string).
        """

        # Get the next piece from the list
        self.current_piece = self.current_pieces.pop(0)

        # Refill the list if empty (assuming getNextPieces exists)
        if not self.current_pieces:
            self.current_pieces = self.update_piece()
            self.get_next_piece()  # Get the next piece from the refilled list

        # Set starting column based on piece type (O piece centered)
        self.current_column = 5 if self.current_piece == 'O' else 4
        return self.current_piece
    
    def play_move(self):
        """Executes the current Tetris move and updates the game state.

        Args:
            self: An instance of the Tetris game class (or similar).
        """

        # Pick the move for the current piece

        aux_dict = self.ai.pickMove(
            self.pieces_indexes[self.current_piece])
        
        orientationIndex = aux_dict["orientationIndex"]
        orientation = aux_dict["orientation"]
        column = aux_dict["column"]
        # Play the move on the board
        self.ai.play_move(self.ai.board, orientation, column)

        # Log the move (optional for debugging)
        print(f"Move #{self.moves} played: {self.current_piece} at column {column}")

        # Update board visualization
        self.ai.draw_board()

        # Update game state
        self.rotar(int(orientationIndex))
        self.moveColumn(column)
        self.get_next_piece()
        self.enviar()

        # Take screenshot (optional)
        # if ... (implement screenshot logic using an external library)
        #   ...

        self.moves += 1


    def arranque(self):

        self.start_game()
        
        while True:
            self.play_move()








    
    

