import pygame as pg
from functions import *

class Object3D:
    def __init__(self, render, vertices='', faces=''):
        self.render = render
        self.vertices = np.array(vertices)
        self.faces = faces
        self.font = pg.font.SysFont('Arial', 30, bold=True)
        self.color_faces = [(pg.Color('dodgerblue'), face) for face in self.faces]
        self.movement_flag, self.draw_vertices = True, True
        self.label = ''
        self.light = np.array([0, 0, -1])  # Light direction


    def draw(self):
        self.screen_projection()
        self.movement()

    def movement(self):
        if self.movement_flag:
            self.rotate_y(pg.time.get_ticks() % 0.005)

    def translate(self, position):
        self.vertices = self.vertices @ translate(position)
    
    def rotate_x(self, angle):
        self.vertices = self.vertices @ rotate_x(angle)

    def rotate_y(self, angle):
        self.vertices = self.vertices @ rotate_y(angle)

    def rotate_z(self, angle):
        self.vertices = self.vertices @ rotate_z(angle)

    def scale(self, number):
        self.vertices = self.vertices @ scale(number)

    def screen_projection(self):
        vertices = self.vertices @ self.render.camera.camera_matrix()
        vertices = vertices @ self.render.projection.projection_matrix
        vertices /= vertices[:, -1].reshape(-1, 1)
        vertices[(vertices > 2) | (vertices < -2)] = 0
        vertices = vertices @ self.render.projection.to_screen_matrix
        vertices = vertices[:, :2]

        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            polygon = vertices[face]
            if not np.any((polygon == self.render.H_WIDTH) | (polygon == self.render.H_HEIGHT)):
                normal = self.calculate_normal(face)
                intensity = np.dot(normal, self.light)
                shade_color = self.shade_color(color, intensity)
                pg.draw.polygon(self.render.screen, shade_color, polygon, 0)  # fill the polygon
                pg.draw.polygon(self.render.screen, pg.Color('black'), polygon, 1)  # draw outline

                if self.label:
                    text = self.font.render(self.label[index], True, pg.Color('white'))
                    self.render.screen.blit(text, polygon[-1])

        if self.draw_vertices:
            for vertex in vertices:
                if not np.any((vertex == self.render.H_WIDTH) | (vertex == self.render.H_HEIGHT)):
                    pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 2)

    # calculate the normal vector of a face
    def calculate_normal(self, face):
        v1 = self.vertices[face[1]] - self.vertices[face[0]]
        v2 = self.vertices[face[2]] - self.vertices[face[0]]
        normal = np.cross(v1[:3], v2[:3])
        normal = normal / np.linalg.norm(normal)
        return normal

    # shade the color of a face
    def shade_color(self, color, intensity):
        intensity = max(0, min(1, intensity))
        shaded_color = (
            min(255, max(0, int(color.r * intensity))),
            min(255, max(0, int(color.g * intensity))),
            min(255, max(0, int(color.b * intensity)))
        )
        return pg.Color(*shaded_color)
    
    def __str__(self):
        return f'{self.__class__.__name__}'

    
            
class Axes(Object3D):
    def __init__(self, render):
        super().__init__(render)
        self.vertices = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
        self.faces = np.array([(0, 1), (0, 2), (0, 3)])
        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertices = False
        self.label = 'XYZ'
