from selenium import webdriver
import jugador as jugador_clase
import procesamiento
def main():
    jugador = jugador_clase.Jugador()
    jugador.start_game()
    tablero = procesamiento.Tablero()
    piezas = tablero.get_piece()
    grid = tablero.update_grid()
    #holding = tablero.get_hold()
    jugador.analizar(piezas, tablero, "x")
    tablero.update_grid()



if __name__ == "__main__":
    main()
