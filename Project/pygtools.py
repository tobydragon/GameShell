import pygame,enum


def drawGoodRect(display, color, rect, thickness):
    """
    Draws a pygame rectangle without little notches in the corners.
    :param display: The pygame display to draw to
    :param color: The color of the rectangle
    :param rect: The rectangle to draw
    :param thickness: The border's thickness
    :return:
    """
    rect = pygame.Rect(rect) #Convert list-style rect to pygame rect]
    halfThick=thickness/2.0
    pygame.draw.line(display, color, (rect.x,rect.y-halfThick+1), (rect.x,rect.y+rect.h+halfThick), thickness)
    pygame.draw.line(display, color, (rect.x,rect.y), (rect.x+rect.w+halfThick,rect.y), thickness)
    pygame.draw.line(display, color, (rect.x+rect.w+halfThick,rect.y+rect.h),  (rect.x,rect.y+rect.h), thickness)
    pygame.draw.line(display, color, (rect.x+rect.w,rect.y+rect.h),(rect.x+rect.w,rect.y), thickness)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DARKGREEN = (5, 102, 0)
LIGHTGREY = (212, 208, 200)
LIGHTBLUE = (153, 255, 255)
