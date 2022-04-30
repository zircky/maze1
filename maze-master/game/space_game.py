import pygame, controls
from gun import Gun
from pygame.sprite import  Group

def run():
    dis = pygame.display
    pygame.init()
    screen = dis.set_mode((700, 800))
    dis.set_caption("Космические защитники")
    bg_color = (0, 0, 0)
    gun = Gun(screen)
    bullets = Group()
    inos = Group()
    controls.create_army(screen, inos)

    while True:
        controls.events(screen, gun, bullets)
        gun.update_gun()
        controls.update(bg_color, screen, gun, inos, bullets)
        controls.update_bullets(bullets)
        controls.update_inos(inos)

run()