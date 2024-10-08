import os
from math import cos,sin
import pygame
WHITE = (255,255,255)
BLACK = (0,0,0)

os.environ['SDL_VIDE_CENTERED'] = '1'
RES = WIDTH, HEIGHT = 1000,1000
FPS = 60

pixel_width = 20
pixel_height = 20

x_pixel = 0
y_pixel = 0

screen_width = WIDTH // pixel_width
screen_height = HEIGHT // pixel_height
screen_size = screen_width * screen_height

A,B = 0,0

theta_spacing = 7
phi_spacing = 2

chars = ".,-~:;=!*#$@"

R1 = 10
R2 = 0
K2 = 50
K1 = screen_height * K2 * 3 / (8 * (R1 + R2))


pygame.init()

screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial',20,bold=True)

def text_display(char,x,y):
    text = font.render(str(char),True,WHITE)
    text_rect = text.get_rect(center=(x,y))
    screen.blit(text,text_rect)
    
k=0

running =True
while running:
    clock.tick(FPS)
    pygame.display.set_caption("FPS: {:.2f}".format(clock.get_fps()))
    screen.fill(BLACK)

    output = [' '] * screen_size
    zbuffer = [0] * screen_size


    for theta in range(0,690,theta_spacing):
        for phi in range(0,690,phi_spacing):

            cosA=cos(A)
            sinA=sin(A)
            cosB=cos(B)
            sinB=sin(B)

            costheta = cos(theta)
            sintheta = sin(theta)
            cosphi= cos(phi)
            sinphi = sin(phi)

            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z = K2 + cosA * circlex * sinphi + circley * sinA
            ooz = 1 / z

            xp = int(screen_width / 2 + K1 * ooz * x)
            yp = int(screen_height / 2 - K1 * ooz * y)

            position = xp + screen_width * yp

            L = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * ( cosA * sintheta - costheta * sinA * sinphi)

            if ooz > zbuffer[position]:
                zbuffer[position] = ooz
                luminance_index = int(L*8)
                output[position] = chars[luminance_index if luminance_index > 0 else 0]
                

    for i in range(screen_height):
        y_pixel += pixel_height
        for j in range(screen_width):
            x_pixel += pixel_width
            text_display(output[k],x_pixel,y_pixel)
            k += 1
        x_pixel = 0
    y_pixel = 0
    k=0

    A+= 0.2
    B+= 0.1


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running=False
