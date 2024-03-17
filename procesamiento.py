"""

TODO: 
1. GRID
2. AGREGARLE ORIENTACIÓN A LAS PIEZAS

Este modulo tiene que tomar la imagen del tetris y devuelve:
el tablero como matriz:
las piezas siguientes como un listado
la ultima pieza como un solo elemento
la pieza que hay guardada
"""

from PIL import Image
import numpy as np



class Tablero:
    def __init__(self):
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
        self.full_board = tetris_completo.crop((left+65, up, right-75, low))
        self.next_piece = tetris_completo.crop((right-68,up+15,right,low-85))
        self.hold_piece = tetris_completo.crop((left+5,up+18,left+64,up+75))

                
        # Create a 10x18 matrix filled with zeros
        self.board = np.zeros((18, 10))

    def update_grid(self):
        
        screenshot = Image.open("tetris.png")
        resized_width = 800  # Adjust width as needed
        resized_height = 600  # Adjust height as needed
        resized_image = screenshot.resize((resized_width, resized_height))
        left = 270
        up = 84
        right = 540
        low = 480
        tetris_completo = resized_image.crop((left, up, right, low))
        width, height = tetris_completo.size
        left = 0
        right=width
        up = 0
        low = height
        # CROP(LEFT, UPPER, RIGHT, LOWER)
        self.full_board = tetris_completo.crop((left+65, up, right-75, low))

        
        #finally updating the GRID

        width, height = self.full_board.size
        left = 0
        right = width
        up = 0
        down = height
        height_diff = down/20 
        right_diff = right/10

        for i in range(0,18):
            for j in range(10):
                cubo = self.full_board.crop((left+(j*right_diff), up+((i+1)*height_diff), left+((j+1)*right_diff), up+((i+2)*height_diff)))
                width, height = cubo.size

                # Find the coordinates of the center pixel
                center_x = width // 2
                center_y = height // 2

                # Get the color of the center pixel
                center_pixel = cubo.getpixel((center_x, center_y))
                negro = center_pixel[0] + center_pixel[1] + center_pixel[2]

                if negro < 40:
                    self.board[i,j] = 0
                else:
                    self.board[i,j] = 1

        print(self.board)







    #This is using the colors to clasify
    # TODO: FIX THIS THAT NOT ONLY RECOGNIZE THE PIECE BUT ALSO THE ORIENTATION.
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
        
        
    def get_piece(self):
        aux_pieces = self.next_piece
        width, height = self.next_piece.size
        left = 0
        right=width
        up = 0
        low = height
        
        add = low/5
        aux_pieces.show()


        pieces = []

        for i in range(5):
            piece = self.next_piece.crop((left, up+(i*add), right, up+((i+1)*add)))
            pieces.append(self.get_color(piece))


        #p1 = self.next_piece.crop((left, up, right, up+add))
        #p1.show()
        
        return pieces 
        
    def get_hold(self):
        aux_hold = self.hold_piece
        piece = self.get_color()
        if piece == 'N':
            return False
        return piece




tablero = Tablero()
print(tablero.get_piece())


