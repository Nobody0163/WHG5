import pygame

__font_cache = {}
def render_text(dst: pygame.Surface, text: str, coords: tuple[int, int] | None, font_name: str, font_size: int, font_color: tuple[int, int, int]):
    if (font_name, font_size) in __font_cache:
        font = __font_cache[(font_name, font_size)]
    else:
        font = pygame.font.Font(font_name, font_size)
        __font_cache[(font_name, font_size)] = font
    
    rendered_text = font.render(text, True, font_color)
    
    if coords is None:
        coords = (dst.get_width() / 2 - rendered_text.get_width() / 2, dst.get_height() / 2 - rendered_text.get_height() / 2)
    else:
        dst.blit(rendered_text, coords)