import pygame

pygame.init()

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.x_mov, self.y_mov = 0, 0
        self.color = (255, 255, 255)  # Default color
        self.parent = None

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

    def render(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 3)
        pygame.draw.line(screen, (0, 255, 0), (self.x, self.y), (self.x + self.x_mov*3, self.y + self.y_mov*3), 1)

    def change_color_if_inside(self, triangles):
        for triangle in triangles:
            if triangle.is_point_inside(self.x, self.y) and self.parent != triangle:
                self.color = (255, 0, 0)
                return
        self.color = (255, 255, 255)  # Reset to default color if not inside any triangle

class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        p1.parent = self
        self.p2 = p2
        p2.parent = self
        self.p3 = p3
        p3.parent = self
        self.points = [p1, p2, p3]

        self.color = (255, 0, 0)  # Default color

    def is_point_inside(self, px, py):
        def sign(x1, y1, x2, y2, x3, y3):
            return (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)

        d1 = sign(px, py, self.p1.x, self.p1.y, self.p2.x, self.p2.y)
        d2 = sign(px, py, self.p2.x, self.p2.y, self.p3.x, self.p3.y)
        d3 = sign(px, py, self.p3.x, self.p3.y, self.p1.x, self.p1.y)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    def render(self, screen):
        pygame.draw.polygon(screen, self.color, [(self.p1.x, self.p1.y), (self.p2.x, self.p2.y), (self.p3.x, self.p3.y)], 1)

def distance(p1, p2):
    return ((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2) ** 0.5

def create_triangle(x1, y1, x2, y2, x3, y3, triangles, points, conections):
    p1 = Point(x1, y1)
    p2 = Point(x2, y2)
    p3 = Point(x3, y3)
    new_points = [p1, p2, p3]
    new_triangle = Triangle(p1, p2, p3)

    # Create connections automatically
    new_conections = [[new_points[0], new_points[1], distance(new_points[0], new_points[1])],
                  [new_points[1], new_points[2], distance(new_points[1], new_points[2])],
                  [new_points[2], new_points[0], distance(new_points[2], new_points[0])]]

    triangles.append(new_triangle)
    points += new_points
    conections += new_conections


triangles = []
points = []
conections = []

create_triangle(400, 300, 500, 300, 450, 400, triangles, points, conections)
create_triangle(200, 400, 300, 500, 250, 600, triangles, points, conections)
create_triangle(200, 200, 300, 300, 250, 400, triangles, points, conections)


new_point = None

s_quality = 4
connection_density = 3

def update_objects():
    for point in points:
        point.update()

    for point in points:
        point.x_mov -= point.x
        point.y_mov -= point.y

    for i in range(s_quality):
        for p1, p2, connection_d in conections:
            d = distance(p1, p2)
            if d != 0:
                if d > connection_d:
                    dl = connection_d - d
                    p1.x -= ((p2.x - p1.x) / d * dl / 2) * connection_density / s_quality
                    p2.x += ((p2.x - p1.x) / d * dl / 2) * connection_density / s_quality

                    p1.y -= ((p2.y - p1.y) / d * dl / 2) * connection_density / s_quality
                    p2.y += ((p2.y - p1.y) / d * dl / 2) * connection_density / s_quality

                if d < connection_d:
                    o = connection_d - d
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

    for triangle in triangles:
        triangle.render(screen)


    for point in points:
        point.change_color_if_inside(triangles)  # Check if point is inside any triangle
        point.render(screen)

# Main loop
while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for triangle in triangles:
                if not new_point and triangle.is_point_inside(mx, my):
                    new_point = Point(mx, my)
                    points.append(new_point)

                    new_point.parent = triangle
                    conections.extend([[new_point, point, distance(new_point, point)] for point in triangle.points])


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
