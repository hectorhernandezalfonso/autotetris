from selenium import webdriver
import jugador as jugador_clase
import procesamiento
def main():
    jugador = jugador_clase.Jugador()
    jugador.start_game()
    tablero = procesamiento.Tablero()
    piezas = tablero.update_piece()
    pieza_actual = piezas[0]
    grid = tablero.update_grid()
    #holding = tablero.get_hold()
    jugador.analizar(piezas, grid, pieza_actual)

    #Así se ve un ciclo de jugar una ficha
    pieza_actual = piezas[1]
    piezas = tablero.update_piece()
    grid = tablero.update_grid()
    jugador.analizar(piezas, grid, pieza_actual)
    


if __name__ == "__main__":
    main()
