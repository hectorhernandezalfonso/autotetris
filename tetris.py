import numpy as np
import random


class AI():
    def __init__(self, number_of_columns, number_of_rows):
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.rows_completed = 0

        self.board = np.zeros(number_of_rows, dtype=int)

        self.FULLROW = np.power(2, number_of_columns) -1



        self.PIECES = []

        self.PIECES = []
        self.PIECES.append([
            {
                'orientation': [self.parse('1111')],
                'width': 4,
                'height': 1
            },
            {
                'orientation': [1, 1, 1, 1],
                'width': 1,
                'height': 4
            }
        ])
        self.PIECES.append([
            {
                'orientation': list(reversed([self.parse('010'), self.parse('111')])),  # Fixed
                'width': 3,
                'height': 2
            },
            {
                'orientation': list(reversed([self.parse('10'), self.parse('11'), self.parse('10')])),  # Fixed
                'width': 2,
                'height': 3
            },
            {
                'orientation': list(reversed([self.parse('111'), self.parse('010')])),  # Fixed
                'width': 3,
                'height': 2
            },
            {
                'orientation': list(reversed([self.parse('01'), self.parse('11'), self.parse('01')])),  # Fixed
                'width': 2,
                'height': 3
            }
        ])

        self.PIECES.append([
            {
                'orientation': [self.parse('11'), self.parse('11')],
                'width': 2,
                'height': 2
            }
        ])


        self.PIECES.append([
            {
                'orientation': list(reversed([self.parse('100'), self.parse('111')])),  # Fixed
                'width': 3,
                'height': 2
            },
            {
                'orientation': list(reversed([self.parse('11'), self.parse('10'), self.parse('10')])),  # Fixed
                'width': 2,
                'height': 3
            },
            {
                'orientation': list(reversed([self.parse('111'), self.parse('001')])),  # Fixed
                'width': 3,
                'height': 2
            },
            {
                'orientation': list(reversed([self.parse('01'), self.parse('01'), self.parse('11')])),  # Fixed
                'width': 2,
                'height': 3
            }
        ])


        self.PIECES.append([
            {
                'orientation': list(reversed([self.parse('001'), self.parse('111')])),  # Fixed
                'width': 3,
                'height': 2
            },
            {
                'orientation': list(reversed([self.parse('10'), self.parse('10'), self.parse('11')])),  # Fixed
                'width': 2,
                'height': 3
            },
            {
                'orientation': list(reversed([self.parse('111'), self.parse('100')])),  # Fixed
                'width': 3,
                'height': 2
            },
            {
                'orientation': list(reversed([self.parse('11'), self.parse('01'), self.parse('01')])),  # Fixed
                'width': 2,
                'height': 3
            }
        ])
        self.PIECES.append([
            {
                'orientation': list(reversed([self.parse('011'), self.parse('110')])),  # Already fixed
                'width': 3,
                'height': 2
            },
            {
                'orientation': list(reversed([self.parse('10'), self.parse('11'), self.parse('01')])),  # Already fixed
                'width': 2,
                'height': 3
            }
        ])

        self.PIECES.append([
            {
                'orientation': list(reversed([self.parse('110'), self.parse('011')])),  # Fixed
                'width': 3,
                'height': 2
            },
            {
                'orientation': list(reversed([self.parse('01'), self.parse('11'),self.parse('10')])), 
                'width': 2,
                'height': 3
            }
        ])

    def parse(self, x):
        return int(x[::-1], 2)





    def GetLandingHeight(self, last_move):
        return last_move["landing_height"] + (len(last_move["piece"]) -1) / 2
    
    def GetRowTransitions(self, board, num_columns):
        transitions = 0
        last_bit = 1

        for i in range(len(board)):
            row = board[i]
            for j in range(num_columns):
                bit = (row >> j) & 1

                if bit != last_bit:
                    transitions+=1
                
                last_bit = bit
            
            if bit == 0:
                transitions+=1
            
            last_bit = 1
        
        return transitions
    

    def get_column_transitions(self, board, num_columns):
        transitions = 0
        last_bit = 1

        for i in range(num_columns):
            for j in range(len(board)):
                row = board[j]
                bit = (row >> i) & 1

                if bit != last_bit:
                    transitions += 1

                last_bit = bit

            last_bit = 1

        return transitions
    
    #ESTA SE CAMBIO SEGÚN GEMINI
    def get_number_of_holes(self, board, num_columns):
        holes = 0
        row_holes = 0x0000
        previous_row = board[-1]

        for i in range(len(board) - 1, -1, -1): #ESTE FUE EL CAMBIO
            row_holes = ~board[i] & (row_holes | 0)

            for j in range(num_columns):
                holes += (row_holes >> j) & 1

            row_holes  |= board[i]

        return holes
    

    def GetWellSums(self, board, num_columns):
        well_sums = 0

        # Check for well cells in inner columns
        for i in range(1, num_columns - 1):
            for j in range(len(board) - 1, -1, -1):
                if (board[j] >> i) & 1 == 0 and (board[j] >> (i - 1)) & 1 == 1 and (board[j] >> (i + 1)) & 1 == 1:
                    well_sums += 1
                    for k in range(j - 1, -1, -1):
                        if (board[k] >> i) & 1 == 0:
                            well_sums += 1
                        else:
                            break

        # Check for wells in the leftmost column
        for j in range(len(board) - 1, -1, -1):
            if (board[j] >> 0) & 1 == 0 and (board[j] >> 1) & 1 == 1:
                well_sums += 1
                for k in range(j - 1, -1, -1):
                    if (board[k] >> 0) & 1 == 0:
                        well_sums += 1
                    else:
                        break

        # Check for wells in the rightmost column
        for j in range(len(board) - 1, -1, -1):
            if (board[j] >> (num_columns - 1)) & 1 == 0 and (board[j] >> (num_columns - 2)) & 1 == 1:
                well_sums += 1
                for k in range(j - 1, -1, -1):
                    if (board[k] & 1 << (num_columns - 1)) == 0:  # Equivalent to (board[k] >> (num_columns - 1)) & 1
                        well_sums += 1
                    else:
                        break

        return well_sums
    

    def parse(self, x):
        return int(x[::-1], 2)
    

    def play(self):
        piece = self.getRandomPiece()
        move = self.pickMove(piece)
        last_move = self.playMove(self.board, move["orientation"], move["column"])

        if not last_move["game_over"]:
            self.rows_completed += last_move["rows_removed"]

        return last_move
    
    def pickMove(self, pieceIndex):
        piece = self.PIECES[pieceIndex]  # ESTO ES LO QUE NO SIRVE
        best_evaluation = -100000
        best_orientation = None
        best_column = 0
        evaluation = None

        # Evaluate all possible orientations within the piece
        aux_orientador = 0
        for element in piece:
            orientation = element['orientation']
            for j in range(self.number_of_columns - element['width']+1):
                board = self.board.copy()
                last_move = self.play_move(board, orientation, j)
                if not last_move["game_over"]:
                    evaluation = self.evaluateBoard(last_move, board)
                    if evaluation > best_evaluation:
                        best_evaluation = evaluation
                        best_orientation = aux_orientador  # Use the actual orientation list
                        best_column = j
                        orientation_win = orientation
            
            aux_orientador = aux_orientador + 1

        self.board = board = np.append(self.board, 0)

        



        return {
            'orientation' : orientation_win,
            'column' : best_column,
            'orientationIndex': best_orientation
        }
                           

        for i, orientation_dict in enumerate(piece):  # Iterate through orientations within the piece list
            orientation = orientation_dict['orientation']
            for j in range(self.number_of_columns - orientation_dict['width'] + 1):
                # Copy current board
                board = self.board.copy()  # Create a deep copy
                last_move = self.play_move(board, orientation, j)
                if not last_move["game_over"]:
                    evaluation = self.evaluateBoard(last_move, board)
                    if evaluation > best_evaluation:
                        best_evaluation = evaluation
                        best_orientation = orientation  # Use the actual orientation list
                        best_column = j

        return {
            'orientation': best_orientation,  # Return the best orientation dictionary
            'column': best_column,
            'orientationIndex': i  # Use the index of the orientation in the loop
        }


    

    def evaluateBoard(self, last_move, board):
        return (
            self.GetLandingHeight(last_move) * -4.500158825082766 +
            last_move["rows_removed"] * 3.4181268101392694 +
            self.GetRowTransitions(board, self.number_of_columns) * -3.2178882868487753 +
            self.get_column_transitions(board, self.number_of_columns) * -9.348695305445199 +
            self.get_number_of_holes(board, self.number_of_columns) * -7.899265427351652 +
            self.GetWellSums(board, self.number_of_columns) * -3.3855972247263626
        )


    def play_move(self, board, piece, column):
        piece = self.move_piece(piece, column)
        placement_row = self.get_placement_row(board, piece)
        rows_removed = 0

        if placement_row + len(piece) > self.number_of_rows:
            # Game over.
            return {'game_over': True}

        # Add piece to board.
        for i in range(len(piece)):
            board[placement_row + i] |= piece[i]

        # Remove any full rows
            
        #ESTA ES LA GRAN PUTA MIERDA QUE NO FUNCIONA O FUNCIONA MAL AHÍ ESTÁ EL CODIGO ORIGINAL 
        #QUE TIENE QUE PASARSE PARA QUE SIRVA
        
        """
        for (i = 0; i < piece.length; i++) {
            if (board[placementRow + i] == this.FULLROW) {
                board.splice(placementRow + i, 1);
                // Add an empty row on top.
                board.push(0);
                // Since we have decreased the number of rows by one, we need to adjust
                // the index accordingly.
                i--;
                rowsRemoved++;
            }
        }
        """

        i = 0
        rowsRemoved = 0
        while i < len(piece):
            if board[placement_row + i] == self.FULLROW:  
                board = np.delete(board, [placement_row + i, placement_row + i+1], axis=0)
                # Add an empty row on top
                board = np.append(board, 0)
                # Since we have decreased the number of rows by one, we need to adjust
                # the index accordingly.
                i -= 1
                rowsRemoved += 1
            i += 1
            
        return {
            'landing_height': placement_row,
            'piece': piece,
            'rows_removed': rows_removed,
            'game_over': False,
        }
    
    

    def get_placement_row(self, board, piece):
        # Descend from top to find the highest row that will collide
        # with the our piece.
        row = self.number_of_rows-len(piece)
        while row >= 0:
            for i in range(len(piece)):
                if (board[row + i] & piece[i]) != 0:
                    # Found collision - place piece on row above.
                    return (row + 1)
            row = row-1

        return 0  # No collision found, piece should be placed on first row.
    
    def move_piece(self, piece, column):
        # Make a new copy of the piece
        
        new_piece = [0] * len(piece)
        for i in range(len(piece)):
            try:
                new_piece[i] = piece[i] << column
            except:
                pass

        return new_piece
    


    def get_random_piece_index(self):
        return random.randint(0, len(self.PIECES) - 1)  # Assuming PIECES is defined elsewhere
    

    def get_random_piece(self):
        return self.PIECES[self.get_random_piece_index()]  # Assuming PIECES is defined elsewhere
    

    def draw_row(self, row_number, row_value):
        for i in range(10):
            if row_value != 0:
                if row_value & 1:
                    print('x', end='')
                else:
                    print('-', end='')
                row_value >>= 1
            else:
                print('-', end='')  # Assuming the behavior is to print '-' for remaining positions when row_value becomes 0
        print()  # Print newline after each row is drawn

    def draw_board(self):
        """
        Prints a representation of the board to the console.

        Args:
            board: A list of lists representing the board state.
        """

        # Iterate through rows in reverse order (top to bottom)
        for row in range(len(self.board) - 1, -1, -1):
            self.draw_row(row, self.board[row])  # Call draw_row function
            print()  # Print a newline after each row



    


















