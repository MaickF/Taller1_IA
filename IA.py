import pygame
import sys
import random
import math
import copy

board = [["","",""],["","",""],["","",""]]
profundidad=3

#Función de la IA para determinar la victoria, no es relevante para el algoritmo.
def victoria(pos, figura, copia):
    row, col = pos
    n = len(copia)  # Asumimos que el tablero es cuadrado
    
    # Verifica si toda la fila está llena de la misma figura
    if all(copia[row][i] == figura for i in range(n)):
        return True

    # Verifica si toda la columna está llena de la misma figura
    if all(copia[i][col] == figura for i in range(n)):
        return True

    # Verifica la diagonal principal (si la jugada está en ella)
    if row == col and all(copia[i][i] == figura for i in range(n)):
        return True

    # Verifica la diagonal secundaria (si la jugada está en ella)
    if row + col == n - 1 and all(copia[i][n - 1 - i] == figura for i in range(n)):
        return True

    return False

#Función para obtener el indice del numero mayor de una lista.
def posicion_maximo(lista):
    if not lista:
        return None
    
    max_valor = max(lista)
    return lista.index(max_valor)

#Funcion para realizar una jugada en una matriz determinada
def jugada(matriz, accion, figura):
    row, col = accion
    matriz[row][col] = figura
    return matriz

#Funcion que retorna las acciones posibles dado un estado de la  matriz       
def action(matriz):
    posiciones = []
    for i in range(3):
        for j in range(3):
          if (matriz[i][j] == ""):
              posiciones += [[i,j]]
    return posiciones


#Funcion inicial para el algoritmo minimax, la diferencia con la auxiliar es que esta si hac e uso de la accion y no solo la evalua
def maxN(figura):
    acciones = action(board)
    ramas = []
    if len(acciones)==0:
        return 0
    else:
        for accion in acciones:
            x = copy.deepcopy(board)
            simulacion = jugada(x, accion, figura)
            if victoria(accion, figura, simulacion):
                jugada(board, accion, figura)
                return accion
            else:
                minimo = 0
                if figura == "X":
                    minimo = min_aux(1, simulacion, "O")
                else:
                    minimo = min_aux(1, simulacion, "X")
                ramas.append(minimo)
        pos = posicion_maximo(ramas)
        accionOptima = acciones[pos]
        jugada(board, accionOptima, figura)
        return accionOptima
        

#Funcion auxiliar del algoritmo minimax, evalua la puntuacion de una accion de forma recursiva
def max_aux(profActual, matriz, figura):
    acciones = action(matriz)
    ramas = []
    if len(acciones)==0:
        return 0
    else:
        for accion in acciones:
            x = copy.deepcopy(matriz)
            simulacion = jugada(x, accion, figura)
            if victoria(accion, figura, simulacion):
                return 1
            elif profActual==profundidad:
                return 0
            else:
                minimo = 0
                if figura == "X":
                    minimo = min_aux(profActual+1, simulacion, "O")
                else:
                    minimo = min_aux(profActual+1, simulacion, "X")
                ramas.append(minimo)
        return max(ramas)

#Funcion auxiliar del algoritmo minimax, evalua la puntuacion de una accion de forma recursiva
def min_aux(profActual, matriz, figura):
    acciones = action(matriz)
    ramas = []
    if len(acciones)==0:
        return 0
    else:
        for accion in acciones:
            x = copy.deepcopy(matriz)
            simulacion = jugada(x, accion, figura)
            if victoria(accion, figura, simulacion):
                return -1
            elif profActual==profundidad:
                return 0
            else:
                minimo = 0
                if figura == "X":
                    maximo = max_aux(profActual+1, simulacion, "O")
                else:
                    maximo = max_aux(profActual+1, simulacion, "X")
                ramas.append(maximo)
        return min(ramas)
            


#Todo lo de abajo es interfaz hecha por IA.

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 300, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - Juego")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configuración del tablero (3x3)
ROWS, COLS = 3, 3
CELL_SIZE = WIDTH // COLS

# Inicializamos el tablero global como matriz 3x3 con celdas vacías
board = [["" for _ in range(COLS)] for _ in range(ROWS)]


def draw_board():
    """Dibuja la cuadrícula y las marcas sobre la pantalla."""
    screen.fill(WHITE)
    # Líneas de la cuadrícula:
    for i in range(1, COLS):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 3)
    for i in range(1, ROWS):
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 3)
    # Dibuja cada marca (X u O) centrada en su celda
    font = pygame.font.Font(None, 80)
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] != "":
                text = font.render(board[row][col], True, BLACK)
                text_rect = text.get_rect(
                    center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
                )
                screen.blit(text, text_rect)


def get_cell_from_pos(pos):
    """Dada una posición (x, y), retorna la tupla (fila, columna) de la celda."""
    x, y = pos
    col = x // CELL_SIZE
    row = y // CELL_SIZE
    return row, col


def choose_mark(screen, width, height):
    """
    Muestra una pantalla para que el jugador elija su figura (X u O)
    retornando la elección.
    """
    font_title = pygame.font.Font(None, 48)
    font_option = pygame.font.Font(None, 72)

    title_text = font_title.render("Elige tu figura:", True, BLACK)
    title_rect = title_text.get_rect(center=(width // 2, height // 4))

    text_X = font_option.render("X", True, BLACK)
    text_O = font_option.render("O", True, BLACK)
    rect_X = text_X.get_rect(center=(width // 3, height // 2))
    rect_O = text_O.get_rect(center=(2 * width // 3, height // 2))

    chosen = None
    while chosen is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if rect_X.collidepoint(pos):
                    chosen = "X"
                elif rect_O.collidepoint(pos):
                    chosen = "O"
        screen.fill(WHITE)
        screen.blit(title_text, title_rect)
        pygame.draw.rect(screen, BLACK, rect_X, 2)
        pygame.draw.rect(screen, BLACK, rect_O, 2)
        screen.blit(text_X, rect_X)
        screen.blit(text_O, rect_O)
        pygame.display.flip()
    return chosen


def choose_difficulty(screen, width, height):
    """
    Muestra una pantalla para que el jugador elija la dificultad:
    "Fácil", "Medio" o "Difícil".
    Retorna la opción seleccionada.
    """
    font_title = pygame.font.Font(None, 30)
    font_option = pygame.font.Font(None, 30)

    title_text = font_title.render("Selecciona dificultad:", True, BLACK)
    title_rect = title_text.get_rect(center=(width // 2, height // 5))

    text_facil = font_option.render("Fácil", True, BLACK)
    text_medio = font_option.render("Medio", True, BLACK)
    text_dificil = font_option.render("Difícil", True, BLACK)
    rect_facil = text_facil.get_rect(center=(width // 4, height // 2))
    rect_medio = text_medio.get_rect(center=(width // 2, height // 2))
    rect_dificil = text_dificil.get_rect(center=(3 * width // 4, height // 2))

    chosen = None
    while chosen is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if rect_facil.collidepoint(pos):
                    chosen = "facil"
                elif rect_medio.collidepoint(pos):
                    chosen = "medio"
                elif rect_dificil.collidepoint(pos):
                    chosen = "dificil"
        screen.fill(WHITE)
        screen.blit(title_text, title_rect)
        pygame.draw.rect(screen, BLACK, rect_facil, 2)
        pygame.draw.rect(screen, BLACK, rect_medio, 2)
        pygame.draw.rect(screen, BLACK, rect_dificil, 2)
        screen.blit(text_facil, rect_facil)
        screen.blit(text_medio, rect_medio)
        screen.blit(text_dificil, rect_dificil)
        pygame.display.flip()
    return chosen


#Realiza un movimiento aleatorio en la partida, para la dificultad facil
def random_move(mark):
    available = [(i, j) for i in range(ROWS) for j in range(COLS) if board[i][j] == ""]
    if available:
        move = random.choice(available)
        board[move[0]][move[1]] = mark
        return move
    return None


def main():
    global board
    clock = pygame.time.Clock()

    # Elección de la figura (jugador)
    player_mark = choose_mark(screen, WIDTH, HEIGHT)
    computer_mark = "O" if player_mark == "X" else "X"

    # Elección de dificultad
    difficulty = choose_difficulty(screen, WIDTH, HEIGHT)
    if difficulty == "medio":
        profundidad = 3
    elif difficulty == "dificil":
        profundidad = 7
    else:  # "facil"
        profundidad = None  # No se utilizará para los movimientos aleatorios

    # En Tic Tac Toe, "X" siempre comienza.
    if player_mark == "X":
        current_player = player_mark  # el jugador inicia
    else:
        current_player = computer_mark  # la computadora inicia si el jugador eligió O

    game_over = False
    winner = None
    restart_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 20, 120, 50)
    while True:
        # Procesar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if restart_rect.collidepoint(pos):
                        # Reiniciar el juego: se restablece el tablero y las variables de estado
                        board = [["" for _ in range(COLS)] for _ in range(ROWS)]
                        game_over = False
                        winner = None
                        # Se conserva la figura y dificultad previa; se reestablece quién comienza
                        if player_mark == "X":
                            current_player = player_mark
                        else:
                            current_player = computer_mark
            else:
                if current_player == player_mark:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = event.pos
                        row, col = get_cell_from_pos(pos)
                        if board[row][col] == "":
                            board[row][col] = player_mark
                            if victoria((row, col), player_mark):
                                game_over = True
                                winner = player_mark
                            elif not any("" in r for r in board):
                                game_over = True
                                winner = "Empate"
                            else:
                                current_player = computer_mark

        # Turno de la computadora (se ejecuta si no terminó la partida y es su turno)
        if not game_over and current_player == computer_mark:
            pygame.time.delay(500)  # Retraso para efecto visual
            if difficulty == "facil":
                move = random_move(computer_mark)
            else:  # "medio" o "dificil"
                move = maxN(computer_mark)
            if move:
                if victoria(move, computer_mark):
                    game_over = True
                    winner = computer_mark
                elif not any("" in r for r in board):
                    game_over = True
                    winner = "Empate"
                else:
                    current_player = player_mark
            else:
                game_over = True
                winner = "Empate"

        draw_board()

        # Si el juego terminó, se dibuja una superposición con el resultado y la opción "Reiniciar"
        if game_over:
            font_winner = pygame.font.Font(None, 50)
            msg = "Empate!" if winner == "Empate" else f"Ganador: {winner}"
            text_winner = font_winner.render(msg, True, (255, 0, 0))
            text_rect = text_winner.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(WHITE)
            screen.blit(overlay, (0, 0))
            screen.blit(text_winner, text_rect)

            # Dibujar el botón "Reiniciar"
            font_restart = pygame.font.Font(None, 40)
            restart_msg = font_restart.render("Reiniciar", True, BLACK)
            pygame.draw.rect(screen, BLACK, restart_rect, 2)
            restart_text_rect = restart_msg.get_rect(center=restart_rect.center)
            screen.blit(restart_msg, restart_text_rect)

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
