import math
import numpy as np

def translate(position):
    tx, ty, tz = position
    return np.array([[1, 0, 0, 0], 
                    [0, 1, 0, 0], 
                    [0, 0, 1, 0], 
                    [tx, ty, tz, 1]])

def rotate_x(angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([[1, 0, 0, 0], 
                    [0, c, s, 0], 
                    [0, -s, c, 0], 
                    [0, 0, 0, 1]])

def rotate_y(angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([[c, 0, -s, 0], 
                    [0, 1, 0, 0], 
                    [s, 0, c, 0], 
                    [0, 0, 0, 1]])

def rotate_z(angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([[c, s, 0, 0], 
                    [-s, c, 0, 0], 
                    [0, 0, 1, 0], 
                    [0, 0, 0, 1]])

def scale(number):
    return np.array([[number, 0, 0, 0], 
                    [0, number, 0, 0], 
                    [0, 0, number, 0], 
                    [0, 0, 0, 1]])