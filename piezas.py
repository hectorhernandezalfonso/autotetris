import numpy as np



def orientacion_pieza(color):
    piece_orientations = {
        "O": np.array([[1, 1],
                     [1, 1]]),
        "I": np.array([1, 1, 1, 1]),
        "L": np.array([[0, 0, 1],
                     [1, 1, 1]]),
        "J": np.array([[1, 0, 0],
                     [1, 1, 1]]),
        "T": np.array([[0, 1, 0],
                      [1, 1, 1]]),
        "S": np.array([[0, 1, 1],
                      [1, 1, 0]]),
        "Z": np.array([[1, 1, 0],
                      [0, 1, 1]])
                      }
    return piece_orientations.get(color)

     