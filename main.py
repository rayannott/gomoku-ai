from environments.freestyle import Board
import pygame
from utils.utils import *

# def calculate_lattice_coordinates(field_rect: pygame.Rect, board_shape: tuple[int, int]) -> tuple[list[float], list[float]]:
#     wshift, hshift = field_rect.topleft
#     margin_hor, margin_vert = field_rect.width/(board_shape[0]+1), field_rect.height/(board_shape[1]+1)
#     hor_coor = [(margin_hor*(i+1) + wshift, hshift) for i in range(board_shape[0])]
#     vert_coor = [(wshift, margin_vert*(i+1) + hshift) for i in range(board_shape[1])]
#     return hor_coor, vert_coor

# def draw_field_lines(screen, hor_coor, vert_coor, field_rect) -> None:
#     wshift, hshift = field_rect.topleft
#     for hc in hor_coor:
#         pygame.draw.line(screen, THEME['grid_lines'], hc, (hc[0], hc[1] + field_rect.width))
#     for vc in vert_coor:
#         pygame.draw.line(screen, THEME['grid_lines'], vc, (vc[0] + field_rect.height, vc[1]))

# def locate_mouse_wrt_lattice_points(mouse_pos: tuple[int, int], hor_coor, vert_coor) -> Pos:
#     h, v = mouse_pos
#     min_h, min_v = 10000, 10000
#     # res_h, res_v = -1, -1
#     for i, hc in enumerate(hor_coor):
#         if abs(hc[0] - h) < min_h:
#             min_h = abs(hc[0] - h)
#             res_h = i
#     for i, vc in enumerate(vert_coor):
#         if abs(vc[1] - v) < min_v:
#             min_v = abs(vc[1] - v)
#             res_v = i
#     return res_v, res_h

# def draw_stones(screen, board, hor_coor, vert_coor):
#     for row_n, row in enumerate(board):
#         for col_n, el in enumerate(row):
#             if el == 1:
#                 pygame.draw.circle(screen, THEME['black_stone'], (hor_coor[col_n][0], vert_coor[row_n][1]), STONE_RADIUS)
#             elif el == -1:
#                 pygame.draw.circle(screen, THEME['white_stone'], (hor_coor[col_n][0], vert_coor[row_n][1]), STONE_RADIUS)

# def draw_closest_lattice_point(screen, mouse_pos, hor_coor, vert_coor):
#     row, col = locate_mouse_wrt_lattice_points(mouse_pos, hor_coor, vert_coor)
#     pygame.draw.circle(screen, (0, 0, 255), (hor_coor[col][0], vert_coor[row][1]), STONE_RADIUS//2, 1)

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
                    self.board.place((row, col), self.current_turn)
                    self.current_turn *= -1
                    winner = self.board.is_over()
                    # board.display()
                    # print(board.last_placed)
                    # print(winner)
                    if winner:
                        print('BLACK!' if winner == 1 else 'WHITE!')
                        self.running = False
                elif event.type == pygame.QUIT:
                    self.running = False
            self.draw_field_lines()
            self.draw_stones()
            self.draw_closest_lattice_point(pygame.mouse.get_pos())
            pygame.draw.rect(self.screen, THEME['field_outline'], self.field_rect, 4)
            pygame.display.update()
    
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

    def draw_closest_lattice_point(self, mouse_pos):
        row, col = self.locate_mouse_wrt_lattice_points(mouse_pos)
        pygame.draw.circle(self.screen, (0, 0, 255), (self.hor_coor[col][0], self.vert_coor[row][1]), STONE_RADIUS//2, 1)


def main():
    game = Gui()
    game.run()

if __name__ == '__main__':
    main()