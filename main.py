from environments.freestyle import Board
import pygame
from utils.utils import *
from utils.exceptions import *

from gui_elements import Button, Element

class Gui:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.field_rect = pygame.Rect(0,0,0,0)
        self.field_rect.size = (FIELD_SIZE, FIELD_SIZE)
        self.field_rect.topright = SCREEN_WIDTH, 0
        self.running = True

        self.board = Board(board_shape=(15, 15)); self.board_shape = self.board.board_shape
        self.hor_coor, self.vert_coor = self.calculate_lattice_coordinates()
        self.current_turn = 1
    
    def run(self):
        while self.running:
            self.screen.fill(THEME['bg'])
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    m_down = pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEBUTTONUP:
                    m_up = pygame.mouse.get_pos()
                    if not self.field_rect.collidepoint(m_up):
                        continue
                    row, col = self.locate_mouse_wrt_lattice_points(m_up)
                    try:
                        self.board.place((row, col), self.current_turn)
                    except OccupiedCell as e:
                        print(e)
                        continue
                    self.current_turn *= -1
                    winner = self.board.is_over()
                    if winner:
                        print('BLACK!' if winner == 1 else 'WHITE!')
                        self.running = False
                elif event.type == pygame.QUIT:
                    self.running = False

            self.draw_field_lines()
            self.draw_stones()
            self.draw_closest_lattice_point(pygame.mouse.get_pos())
            self.draw_last_stone_highlight()
            pygame.draw.rect(self.screen, THEME['field_outline'], self.field_rect, 4)
            pygame.display.update()
    
    def locate_mouse_wrt_lattice_points(self, mouse_pos) -> Pos:
        h, v = mouse_pos
        min_h, min_v = 10000, 10000
        # res_h, res_v = -1, -1
        for i, hc in enumerate(self.hor_coor):
            if abs(hc[0] - h) < min_h:
                min_h = abs(hc[0] - h)
                res_h = i
        for i, vc in enumerate(self.vert_coor):
            if abs(vc[1] - v) < min_v:
                min_v = abs(vc[1] - v)
                res_v = i
        return res_v, res_h

    def calculate_lattice_coordinates(self) -> tuple[list[float], list[float]]:
        wshift, hshift = self.field_rect.topleft
        margin_hor, margin_vert = self.field_rect.width/(self.board_shape[0]+1), self.field_rect.height/(self.board_shape[1]+1)
        hor_coor = [(margin_hor*(i+1) + wshift, hshift) for i in range(self.board_shape[0])]
        vert_coor = [(wshift, margin_vert*(i+1) + hshift) for i in range(self.board_shape[1])]
        return hor_coor, vert_coor

    def draw_stones(self):
        for row_n, row in enumerate(self.board.b):
            for col_n, el in enumerate(row):
                if el == 1:
                    pygame.draw.circle(self.screen, THEME['black_stone'], (self.hor_coor[col_n][0], self.vert_coor[row_n][1]), STONE_RADIUS)
                elif el == -1:
                    pygame.draw.circle(self.screen, THEME['white_stone'], (self.hor_coor[col_n][0], self.vert_coor[row_n][1]), STONE_RADIUS)
    
    def draw_field_lines(self) -> None:
        for hc in self.hor_coor:
            pygame.draw.line(self.screen, THEME['grid_lines'], hc, (hc[0], hc[1] + self.field_rect.width))
        for vc in self.vert_coor:
            pygame.draw.line(self.screen, THEME['grid_lines'], vc, (vc[0] + self.field_rect.height, vc[1]))

    def draw_closest_lattice_point(self, mouse_pos):
        row, col = self.locate_mouse_wrt_lattice_points(mouse_pos)
        pygame.draw.circle(self.screen, (0, 0, 255), (self.hor_coor[col][0], self.vert_coor[row][1]), STONE_RADIUS/2, 1)
    
    def draw_last_stone_highlight(self):
        if self.board.last_placed is not None:
            row, col = self.board.last_placed
            pygame.draw.circle(self.screen, (200, 0, 0), (self.hor_coor[col][0], self.vert_coor[row][1]), STONE_RADIUS/3)

def game_window():
    game = Gui()
    game.run()

def main():
    # game_window()
    menu_window()

def menu_window():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    start_btn_rect = pygame.Rect((0,0), (650, 140))
    start_btn_rect.center = screen.get_rect().center
    start_btn = Button(start_btn_rect, screen, 'START GAME', 'ok')
    
    running = True
    while running:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                m_down = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                m_up = pygame.mouse.get_pos()
                if start_btn.click(m_up):
                    game_window()
            elif event.type == pygame.QUIT:
                running = False

        mouse_pos = pygame.mouse.get_pos()
        start_btn.render(mouse_pos)
        pygame.display.update()

if __name__ == '__main__':
    main()