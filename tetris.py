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
                'orientation': [int(x) for x in str('1111')],
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
                'orientation': [int(x) for x in str('010')][::-1],
                'width': 3,
                'height': 2
            },
            {
                'orientation': [int(x) for x in str('10')][::-1],
                'width': 2,
                'height': 3
            },
            {
                'orientation': [int(x) for x in str('111')][::-1],
                'width': 3,
                'height': 2
            },
            {
                'orientation': [int(x) for x in str('01')][::-1],
                'width': 2,
                'height': 3
            }
        ])
        self.PIECES.append([
            {
                'orientation': [int(x) for x in str('11')],
                'width': 2,
                'height': 2
            }
        ])
        self.PIECES.append([
            {
                'orientation': [int(x) for x in str('100')][::-1],
                'width': 3,
                'height': 2
            },
            {
                'orientation': [int(x) for x in str('11')][::-1],
                'width': 2,
                'height': 3
            },
            {
                'orientation': [int(x) for x in str('111')][::-1],
                'width': 3,
                'height': 2
            },
            {
                'orientation': [int(x) for x in str('01')][::-1],
                'width': 2,
                'height': 3
            }
        ])
        self.PIECES.append([
            {
                'orientation': [int(x) for x in str('001')][::-1],
                'width': 3,
                'height': 2
            },
            {
                'orientation': [int(x) for x in str('10')][::-1],
                'width': 2,
                'height': 3
            },
            {
                'orientation': [int(x) for x in str('111')][::-1],
                'width': 3,
                'height': 2
            },
            {
                'orientation': [int(x) for x in str('11')][::-1],
                'width': 2,
                'height': 3
            }
        ])
        self.PIECES.append([
            {
                'orientation': [int(x) for x in str('011')][::-1],
                'width': 3,
                'height': 2
            },
            {
                'orientation': [int(x) for x in str('10')][::-1],
                'width': 2,
                'height': 3
            }
        ])
        self.PIECES.append([
            {
                'orientation': [int(x) for x in str('110')][::-1],
                'width': 3,
                'height': 2
            },
            {
                'orientation': [int(x) for x in str('01')][::-1],
                'width': 2,
                'height': 3
            }
        ])





    def GetLandingHeight(self, last_move):
        return last_move["landing_height"] + ((len(last_move["piece"]) -1) / 2)
    
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
    
    def get_number_of_holes(self, board, num_columns):
        holes = 0
        row_holes = 0x0000
        previous_row = board[-1]

        for i in range(len(board) - 2, -1, -1):
            row_holes = ~board[i] & (previous_row | row_holes)

            for j in range(num_columns):
                holes += (row_holes >> j) & 1

            previous_row = board[i]

        return holes
    

    def GetWellSums(self, board, num_columns):
        well_sums = 0
        # Check for well cells in the "inner columns" of the board.
        # "Inner columns" are the columns that aren't touching the edge of the board.
        for i in range(1, num_columns - 1):
            for j in range(len(board) - 1, -1, -1):
                if (
                    (board[j] >> i) & 1 == 0 and
                    (board[j] >> (i - 1)) & 1 == 1 and
                    (board[j] >> (i + 1)) & 1 == 1
                ):
                    # Found well cell, count it + the number of empty cells below it.
                    well_sums += 1
                    for k in range(j - 1, -1, -1):
                        if (board[k] >> i) & 1 == 0:
                            well_sums += 1
                        else:
                            break
        # Check for well cells in the leftmost column of the board.
        for j in range(len(board) - 1, -1, -1):
            if (board[j] >> 0) & 1 == 0 and (board[j] >> (0 + 1)) & 1 == 1:
                # Found well cell, count it + the number of empty cells below it.
                well_sums += 1
                for k in range(j - 1, -1, -1):
                    if (board[k] >> 0) & 1 == 0:
                        well_sums += 1
                    else:
                        break
        # Check for well cells in the rightmost column of the board.
        for j in range(len(board) - 1, -1, -1):
            if (
                (board[j] >> (num_columns - 1)) & 1 == 0 and
                (board[j] >> (num_columns - 2)) & 1 == 1
            ):
                # Found well cell, count it + the number of empty cells below it.
                well_sums += 1
                for k in range(j - 1, -1, -1):
                    if (board[k] >> (num_columns - 1)) & 1 == 0:
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
        print("esto es de pick Move y es lo que no sirve")
        print("piece")
        print(piece)
        print("piece index")
        print(pieceIndex)
        best_evaluation = -100000
        best_orientation = None
        best_column = 0
        evaluation = None

        # Evaluate all possible orientations within the piece
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

        if placement_row + len(piece) > len(board):
            # Game over.
            return {'game_over': True}

        # Add piece to board.
        for i in range(len(piece)):
            board[placement_row + i] |= piece[i]

        # Remove any full rows
        i = 0
        while i < len(piece):
            if board[placement_row + i] == self.FULLROW:
                del board[placement_row + i]
                # Add an empty row on top.
                board.append(0)
                # Since we have decreased the number of rows by one, we need to adjust
                # the index accordingly.
                i -= 1
                rows_removed += 1
            i += 1

        return {
            'landing_height': placement_row,
            'piece': piece,
            'rows_removed': rows_removed,
            'game_over': False
        }
    

    def get_placement_row(self, board, piece):
        # Descend from top to find the highest row that will collide
        # with the our piece.
        for row in range(len(board) - len(piece), -1, -1):
            # Check if piece collides with the cells of the current row.
            for i in range(len(piece)):
                if (board[row + i] & piece[i]) != 0:
                    # Found collision - place piece on row above.
                    return row + 1

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



    


















