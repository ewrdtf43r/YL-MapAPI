import sys
import requests
import pygame
import os
from io import BytesIO

spn1, spn2 = map(str, input("Введите масштаб (пример - 0.01 0.01): ").split())
coords1, coords2 = map(str, input("Введите координаты (пример - 37.620070 55.753630): ").split())

def get_maps(coords1, coords2, spn1, spn2, l="map"):
    maps_server = 'http://static-maps.yandex.ru/1.x/'
    map_params = {
        'll': coords1 + ',' + coords2,
        'spn': spn1 + ',' + spn2,
        'l': l}
    response = requests.get(maps_server, params=map_params)
    image = pygame.image.load(BytesIO(response.content))
    return image

def move(direct, coords1, coords2, spn1, spn2):
    if direct == "right":
        coords1 = str(float(coords1) + float(spn2))
    elif direct == "left":
        coords1 = str(float(coords1) - float(spn2))
    elif direct == "down":
        coords2 = str(float(coords2) - float(spn1))
    else:
        coords2 = str(float(coords2) + float(spn1))
    return coords1, coords2

pygame.init()
pygame.display.set_caption('YL-MAP')
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
running = True
now = 0
FPS = 50
scale = 0
clock = pygame.time.Clock()

image = get_maps(coords1, coords2, spn1, spn2)
def terminate():
    pygame.quit()
    sys.exit()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            print(scale)
            if event.key == 1073741899 and scale <= 0.1:
                scale += 0.01
                scale = round(scale, 3)
                image = get_maps(coords1, coords2, str(float(spn1) + scale), str(float(spn2) + scale))
            elif event.key == 1073741902 and scale - 0.01 + float(spn1) >= 0 and scale - 0.01 + float(spn2) >= 0:
                scale -= 0.01
                scale = round(scale, 3)
                image = get_maps(coords1, coords2, str(float(spn1) + scale), str(float(spn2) + scale))
            elif event.key == pygame.K_UP:
                coords1, coords2 = move("up", coords1, coords2, spn1, spn2)
                image = get_maps(coords1, coords2, spn1, spn2)
            elif event.key == pygame.K_DOWN:
                coords1, coords2 = move("down", coords1, coords2, spn1, spn2)
                image = get_maps(coords1, coords2, spn1, spn2)
            elif event.key == pygame.K_LEFT:
                coords1, coords2 = move("left", coords1, coords2, spn1, spn2)
                image = get_maps(coords1, coords2, spn1, spn2)
            elif event.key == pygame.K_RIGHT:
                coords1, coords2 = move("right", coords1, coords2, spn1, spn2)
                image = get_maps(coords1, coords2, spn1, spn2)
            elif event.key == pygame.K_b:
                image = get_maps(coords1, coords2, spn1, spn2, l="map")
            elif event.key == pygame.K_n:
                image = get_maps(coords1, coords2, spn1, spn2, l="sat")
            elif event.key == pygame.K_m:
                image = get_maps(coords1, coords2, spn1, spn2, l="sat,skl")
    screen.blit(image, (0, 0))

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()