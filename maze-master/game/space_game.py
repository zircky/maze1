import pygame, controls
from gun import Gun


def run():
    dis = pygame.display
    pygame.init()
    screen = dis.set_mode((700, 800))
    dis.set_caption("Космические защитники")
    bg_color = (0, 0, 0)
    gun = Gun(screen)

    while True:
        controls.events(gun)
        gun.update_gun()
        screen.fill(bg_color)
        gun.output()
        dis.flip()


run()