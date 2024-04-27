import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.x_mov, self.y_mov = 0, 0

    def update(self):
        self.x_mov *= 0.99
        self.y_mov *= 0.99

        self.y_mov += 0.3

        self.x += self.x_mov
        self.y += self.y_mov


        if self.y > 800:
            self.y_mov = 800-self.y
            self.x_mov *= 0.9

            self.y = 800

        if self.y < 0:
            self.y_mov = 0-self.y
            self.x_mov *= 0.9

            self.y = 0

        if self.x > 800:
            self.y_mov *= 0.9
            self.x_mov = 800-self.x

            self.x = 800

        if self.x < 0:
            self.y_mov *= 0.9
            self.x_mov = 0-self.x

            self.x = 0

    def render(self):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 3)


def distance(p1, p2):
    return ((p2.x-p1.x)**2 + (p2.y-p1.y)**2)**0.5


s_quality = 10
connection_density = 5
def update_objects():
    for point in points:
        point.update()

    for point in points:
        point.x_mov -= point.x
        point.y_mov -= point.y

    for i in range(s_quality):
        for p1, p2, conection_d in conections:
            d = distance(p1, p2)
            if d != 0:
                if d > conection_d:
                    dl = conection_d - d
                    p1.x -= ((p2.x - p1.x)/d * dl/2) *connection_density /s_quality
                    p2.x += ((p2.x - p1.x)/d * dl/2) *connection_density /s_quality

                    p1.y -= ((p2.y - p1.y)/d * dl/2) *connection_density /s_quality
                    p2.y += ((p2.y - p1.y)/d * dl/2) *connection_density /s_quality

                if d < conection_d:
                    o = conection_d - d
                    p1.x -= ((p2.x - p1.x)/d * o/2) *connection_density /s_quality
                    p2.x += ((p2.x - p1.x)/d * o/2) *connection_density /s_quality

                    p1.y -= ((p2.y - p1.y)/d * o/2) *connection_density /s_quality
                    p2.y += ((p2.y - p1.y)/d * o/2) *connection_density /s_quality


    for point in points:
        point.x_mov += point.x
        point.y_mov += point.y


def render_objects():
    for p1, p2, a in conections:
        pygame.draw.line(screen, (255, 0, 0), [p1.x, p1.y], [p2.x, p2.y], 1)

    for point in points:
        point.render()

points = []
points.append(Point(50, 50))
points.append(Point(100, 50))
points.append(Point(100, 100))
points.append(Point(50, 100))

points.append(Point(150, 50))
points.append(Point(200, 50))

conections = [[points[0], points[1], distance(points[0], points[1])],
              [points[1], points[2], distance(points[1], points[2])],
              [points[2], points[3], distance(points[2], points[3])],
              [points[3], points[0], distance(points[3], points[0])],

              [points[0], points[2], distance(points[0], points[2])],
              [points[1], points[3], distance(points[1], points[3])],

              [points[1], points[4], distance(points[1], points[4])],
              [points[4], points[5], distance(points[4], points[5])]]


target_point = None
while 1:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            target_point = sorted(points, key=lambda x: distance(x, Point(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])))[0]

            if distance(target_point, Point(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])) > 60:
                target_point = None

    if pygame.mouse.get_pressed()[0] and target_point!= None:
        target_point.x_mov = pygame.mouse.get_pos()[0] - target_point.x
        target_point.y_mov = pygame.mouse.get_pos()[1] - target_point.y

    update_objects()
    render_objects()

    pygame.display.update()
    clock.tick(60)