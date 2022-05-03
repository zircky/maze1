import pygame, controls
from gun import Gun
from pygame.sprite import  Group
from stats import Stats

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
    stats = Stats()

    while True:
        controls.events(screen, gun, bullets)
        gun.update_gun()
        controls.update(bg_color, screen, gun, inos, bullets)
        controls.update_bullets(inos, bullets)
        controls.update_inos(stats, screen, gun, inos, bullets)

run()