import pygame
import sys
import random
import time
from pygame import mixer

# Инициализация Pygame
pygame.init()
mixer.init()

# Константы
WIDTH, HEIGHT = 600, 700
BOARD_SIZE = 3
CELL_SIZE = 150
MARGIN = 50
BOARD_PADDING = 100

# Цвета
BG_COLOR = (28, 35, 51)
GRID_COLOR = (79, 91, 122)
X_COLOR = (240, 84, 84)
O_COLOR = (76, 175, 80)
HOVER_COLOR = (61, 90, 128)
WIN_COLOR = (255, 215, 0)
TEXT_COLOR = (240, 240, 240)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎮 Крестики-Нолики с ИИ")

# Шрифты
font_large = pygame.font.Font(None, 60)
font_medium = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 30)

# Звуки
try:
    click_sound = mixer.Sound("click.wav")
    win_sound = mixer.Sound("win.wav")
    lose_sound = mixer.Sound("lose.wav")
except:
    print("Звуковые файлы не найдены. Игра будет без звука.")
    click_sound = win_sound = lose_sound = None

class TicTacToe:
    def __init__(self):
        self.board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.winning_cells = []
        self.player_score = 0
        self.bot_score = 0
        self.animations = []

    def reset(self):
        self.board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.winning_cells = []
        self.animations = []

    def make_move(self, row, col):
        if self.board[row][col] == '' and not self.game_over:
            self.board[row][col] = self.current_player
            
            # Анимация появления символа
            self.animations.append({
                'type': 'appear',
                'row': row,
                'col': col,
                'symbol': self.current_player,
                'progress': 0
            })
            
            if click_sound:
                click_sound.play()
            
            # Проверка победы
            if self.check_win(self.current_player):
                self.game_over = True
                self.winner = self.current_player
                if self.current_player == 'X':
                    self.player_score += 1
                    if win_sound:
                        win_sound.play()
                else:
                    self.bot_score += 1
                    if lose_sound:
                        lose_sound.play()
            elif self.is_board_full():
                self.game_over = True
                self.winner = 'Draw'
            
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def bot_move(self):
        if self.game_over or self.current_player != 'O':
            return

        # ИИ: сначала проверяем выигрышный ход
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == '':
                    self.board[i][j] = 'O'
                    if self.check_win('O'):
                        self.board[i][j] = ''
                        self.make_move(i, j)
                        return
                    self.board[i][j] = ''

        # Блокировка выигрышного хода игрока
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == '':
                    self.board[i][j] = 'X'
                    if self.check_win('X'):
                        self.board[i][j] = ''
                        self.make_move(i, j)
                        return
                    self.board[i][j] = ''

        # Центр
        if self.board[1][1] == '':
            self.make_move(1, 1)
            return

        # Углы
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        random.shuffle(corners)
        for i, j in corners:
            if self.board[i][j] == '':
                self.make_move(i, j)
                return

        # Любая свободная клетка
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == '':
                    self.make_move(i, j)
                    return

    def check_win(self, player):
        # Проверка строк и столбцов
        for i in range(BOARD_SIZE):
            if all(self.board[i][j] == player for j in range(BOARD_SIZE)):
                self.winning_cells = [(i, j) for j in range(BOARD_SIZE)]
                return True
            if all(self.board[j][i] == player for j in range(BOARD_SIZE)):
                self.winning_cells = [(j, i) for j in range(BOARD_SIZE)]
                return True

        # Проверка диагоналей
        if all(self.board[i][i] == player for i in range(BOARD_SIZE)):
            self.winning_cells = [(i, i) for i in range(BOARD_SIZE)]
            return True
        if all(self.board[i][2-i] == player for i in range(BOARD_SIZE)):
            self.winning_cells = [(i, 2-i) for i in range(BOARD_SIZE)]
            return True

        return False

    def is_board_full(self):
        return all(self.board[i][j] != '' for i in range(BOARD_SIZE) for j in range(BOARD_SIZE))

    def draw(self, screen):
        # Фон
        screen.fill(BG_COLOR)
        
        # Сетка
        for i in range(1, BOARD_SIZE):
            # Вертикальные линии
            pygame.draw.line(screen, GRID_COLOR, 
                           (MARGIN + i * CELL_SIZE, MARGIN),
                           (MARGIN + i * CELL_SIZE, MARGIN + BOARD_SIZE * CELL_SIZE), 5)
            # Горизонтальные линии
            pygame.draw.line(screen, GRID_COLOR,
                           (MARGIN, MARGIN + i * CELL_SIZE),
                           (MARGIN + BOARD_SIZE * CELL_SIZE, MARGIN + i * CELL_SIZE), 5)

        # Символы
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                cell_x = MARGIN + j * CELL_SIZE + CELL_SIZE // 2
                cell_y = MARGIN + i * CELL_SIZE + CELL_SIZE // 2
                
                # Подсветка выигрышной комбинации
                if (i, j) in self.winning_cells:
                    pygame.draw.rect(screen, WIN_COLOR, 
                                  (MARGIN + j * CELL_SIZE + 5, MARGIN + i * CELL_SIZE + 5,
                                   CELL_SIZE - 10, CELL_SIZE - 10), 3)

                if self.board[i][j] == 'X':
                    size = int(CELL_SIZE * 0.6)
                    pygame.draw.line(screen, X_COLOR, 
                                   (cell_x - size//2, cell_y - size//2),
                                   (cell_x + size//2, cell_y + size//2), 8)
                    pygame.draw.line(screen, X_COLOR,
                                   (cell_x + size//2, cell_y - size//2),
                                   (cell_x - size//2, cell_y + size//2), 8)
                
                elif self.board[i][j] == 'O':
                    radius = int(CELL_SIZE * 0.3)
                    pygame.draw.circle(screen, O_COLOR, (cell_x, cell_y), radius, 8)

        # Обновление анимаций
        for anim in self.animations[:]:
            if anim['type'] == 'appear':
                anim['progress'] += 0.1
                if anim['progress'] >= 1:
                    self.animations.remove(anim)
                else:
                    i, j = anim['row'], anim['col']
                    cell_x = MARGIN + j * CELL_SIZE + CELL_SIZE // 2
                    cell_y = MARGIN + i * CELL_SIZE + CELL_SIZE // 2
                    
                    if anim['symbol'] == 'X':
                        size = int(CELL_SIZE * 0.6 * anim['progress'])
                        pygame.draw.line(screen, X_COLOR, 
                                       (cell_x - size//2, cell_y - size//2),
                                       (cell_x + size//2, cell_y + size//2), 8)
                        pygame.draw.line(screen, X_COLOR,
                                       (cell_x + size//2, cell_y - size//2),
                                       (cell_x - size//2, cell_y + size//2), 8)
                    else:
                        radius = int(CELL_SIZE * 0.3 * anim['progress'])
                        pygame.draw.circle(screen, O_COLOR, (cell_x, cell_y), radius, 8)

        # Статус игры
        status_text = ""
        if self.game_over:
            if self.winner == 'X':
                status_text = "🎉 Вы выиграли!"
            elif self.winner == 'O':
                status_text = "🤖 Бот выиграл!"
            else:
                status_text = "🤝 Ничья!"
        else:
            status_text = f"Ход: {'Игрок (X)' if self.current_player == 'X' else 'Бот (O)'}"

        text = font_medium.render(status_text, True, TEXT_COLOR)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 20))

        # Счет
        score_text = font_small.render(f"Счет: {self.player_score} - {self.bot_score}", True, TEXT_COLOR)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT - 80))

        # Кнопка перезапуска
        if self.game_over:
            pygame.draw.rect(screen, (61, 90, 128), (WIDTH // 2 - 100, HEIGHT - 120, 200, 50), border_radius=10)
            restart_text = font_small.render("Новая игра", True, TEXT_COLOR)
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT - 110))

def main():
    game = TicTacToe()
    clock = pygame.time.Clock()
    last_bot_move_time = 0
    
    print("🎮 Добро пожаловать в Крестики-Нолики!")
    print("🔹 Вы играете за X")
    print("🔹 Бот играет за O")
    print("🔹 Нажмите на клетку, чтобы сделать ход")
    print("🔹 Для новой игры нажмите кнопку внизу")

    while True:
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                
                # Проверка клика по доске
                if (MARGIN <= x <= MARGIN + BOARD_SIZE * CELL_SIZE and
                    MARGIN <= y <= MARGIN + BOARD_SIZE * CELL_SIZE and not game.game_over):
                    col = (x - MARGIN) // CELL_SIZE
                    row = (y - MARGIN) // CELL_SIZE
                    if game.board[row][col] == '' and game.current_player == 'X':
                        game.make_move(row, col)
                        last_bot_move_time = current_time
                
                # Проверка клика по кнопке перезапуска
                if (game.game_over and 
                    WIDTH // 2 - 100 <= x <= WIDTH // 2 + 100 and
                    HEIGHT - 120 <= y <= HEIGHT - 70):
                    game.reset()

        # Ход бота с задержкой
        if (not game.game_over and game.current_player == 'O' and 
            current_time - last_bot_move_time > 0.5):
            game.bot_move()
            last_bot_move_time = current_time

        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()