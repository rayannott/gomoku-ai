import pygame
from utils.utils import FONT, FONT_SMALL

class Element:
    def __init__(self, pg_rect: pygame.Rect, surface: pygame.Surface, hover_tooltip='', active=True):
        self.rect = pg_rect
        self.surface = surface
        self.active = active
        self.visible = True
        self.hover = False
        self.hover_tooltip = hover_tooltip
        self.htt_text_surface = FONT_SMALL.render(self.hover_tooltip, True, (200, 200, 200))
        self.htt_text_rect = self.htt_text_surface.get_rect(bottomleft=self.rect.topleft)

    def draw(self) -> None:
        if not self.visible:
            return
        pygame.draw.rect(self.surface, (30, 30, 30), self.rect, 1)
        if self.hover_tooltip and self.hover:
            self.surface.blit(self.htt_text_surface, self.htt_text_rect)
    
    def click(self, mouse_pos) -> bool:
        return self.hovering(mouse_pos) if self.active else False
    
    def hovering(self, mouse_pos) -> bool:
        return self.rect.collidepoint(mouse_pos)
    
    def render(self, current_mouse_pos):
        if self.hovering(current_mouse_pos):
            self.hover = True
        else:
            self.hover = False
        self.draw()
    
    def hide(self) -> None:
        self.visible = False
    
    def show(self) -> None:
        self.visible = True
    
    def deactivate(self) -> None:
        self.active = False
    
    def activate(self) -> None:
        self.active = True

class Button(Element):
    def __init__(self, pg_rect, surface, text='', hover_tooltip='', active=True) -> None:
        super().__init__(pg_rect, surface, hover_tooltip, active)
        self.text = text
        self.text_surface = FONT.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self) -> None:
        self.surface.blit(self.text_surface, self.text_rect)
        color = (140, 150, 160) if self.hover else (255, 255, 255)
        pygame.draw.rect(self.surface, color, self.rect, 4)
        return super().draw()
        