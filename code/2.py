import pygame

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
            self.y_mov = 800 - self.y
            self.x_mov *= 0.9

            self.y = 800

        if self.y < 0:
            self.y_mov = 0 - self.y
            self.x_mov *= 0.9

            self.y = 0

        if self.x > 800:
            self.y_mov *= 0.9
            self.x_mov = 800 - self.x

            self.x = 800

        if self.x < 0:
            self.y_mov *= 0.9
            self.x_mov = 0 - self.x

            self.x = 0

    def render(self):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 3)
        # Отрисовка направления и скорости движения
        pygame.draw.line(screen, (0, 255, 0), (self.x, self.y), (self.x + self.x_mov*3, self.y + self.y_mov*3), 1)


def distance(p1, p2):
    return ((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2) ** 0.5

def point_in_triangle(px, py, ax, ay, bx, by, cx, cy):
    def sign(x1, y1, x2, y2, x3, y3):
        return (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)

    d1 = sign(px, py, ax, ay, bx, by)
    d2 = sign(px, py, bx, by, cx, cy)
    d3 = sign(px, py, cx, cy, ax, ay)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)

s_quality = 4
connection_density = 3

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
                    p1.x -= ((p2.x - p1.x) / d * dl / 2) * connection_density / s_quality
                    p2.x += ((p2.x - p1.x) / d * dl / 2) * connection_density / s_quality

                    p1.y -= ((p2.y - p1.y) / d * dl / 2) * connection_density / s_quality
                    p2.y += ((p2.y - p1.y) / d * dl / 2) * connection_density / s_quality

                if d < conection_d:
                    o = conection_d - d
                    p1.x -= ((p2.x - p1.x) / d * o / 2) * connection_density / s_quality
                    p2.x += ((p2.x - p1.x) / d * o / 2) * connection_density / s_quality

                    p1.y -= ((p2.y - p1.y) / d * o / 2) * connection_density / s_quality
                    p2.y += ((p2.y - p1.y) / d * o / 2) * connection_density / s_quality

    for point in points:
        point.x_mov += point.x
        point.y_mov += point.y

def render_objects():
    for p1, p2, _ in conections:
        color = (0, 255, 0) if new_point and (new_point in [p1, p2]) else (255, 0, 0)
        pygame.draw.line(screen, color, [p1.x, p1.y], [p2.x, p2.y], 1)

    for point in points:
        point.render()

points = []
points.append(Point(400, 300))
points.append(Point(500, 300))
points.append(Point(450, 400))

conections = [[points[0], points[1], distance(points[0], points[1])],
              [points[1], points[2], distance(points[1], points[2])],
              [points[2], points[0], distance(points[2], points[0])]]

new_point = None
while 1:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if not new_point and point_in_triangle(mx, my, points[0].x, points[0].y, points[1].x, points[1].y, points[2].x, points[2].y):
                new_point = Point(mx, my)
                points.append(new_point)
                for point in points[:-1]:
                    conections.append([new_point, point, distance(new_point, point)])

        if event.type == pygame.MOUSEBUTTONUP:
            if new_point:
                points.remove(new_point)
                conections = [con for con in conections if new_point not in con]
                new_point = None

    if pygame.mouse.get_pressed()[0] and new_point:
        new_point.x_mov = (pygame.mouse.get_pos()[0] - new_point.x)/2
        new_point.y_mov = (pygame.mouse.get_pos()[1] - new_point.y)/2

    update_objects()
    render_objects()

    pygame.display.update()
    clock.tick(60)
