import pygame

class Button:
    def __init__(self, x, y, width, height, text, callback, color=(100, 100, 100), hover_color=(150, 150, 150), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def draw(self, screen, font):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2, border_radius=5)
        
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.callback()
                return True
        return False


class ConfirmDialog:
    def __init__(self, title, message, on_confirm, on_cancel):
        self.title = title
        self.message = message
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        self.width = 400
        self.height = 200
        self.x = (1000 - self.width) // 2
        self.y = (600 - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.confirm_btn = Button(
            self.x + 80, self.y + 140, 100, 40, "确认", 
            lambda: self.on_confirm(),
            (0, 150, 0), (0, 200, 0)
        )
        self.cancel_btn = Button(
            self.x + 220, self.y + 140, 100, 40, "取消", 
            lambda: self.on_cancel(),
            (150, 0, 0), (200, 0, 0)
        )

    def draw(self, screen, font, small_font):
        pygame.draw.rect(screen, (50, 50, 50), self.rect, border_radius=10)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 3, border_radius=10)
        
        title_surface = font.render(self.title, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.x + self.width // 2, self.y + 40))
        screen.blit(title_surface, title_rect)
        
        message_surface = small_font.render(self.message, True, (200, 200, 200))
        message_rect = message_surface.get_rect(center=(self.x + self.width // 2, self.y + 90))
        screen.blit(message_surface, message_rect)
        
        self.confirm_btn.draw(screen, small_font)
        self.cancel_btn.draw(screen, small_font)

    def handle_event(self, event):
        if self.confirm_btn.handle_event(event):
            return True
        if self.cancel_btn.handle_event(event):
            return True
        return False
