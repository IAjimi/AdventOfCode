import numpy as np
from math import cos, sin, radians

def move_ship(_input):
    compass = {0: "N", 90: "E", 180: "S", 270: "W"}
    north, east, angle = 0, 0, 90

    for inst in _input:
        letter, num = inst[0], int(inst[1:])

        if letter == "F":
            direction = compass[angle]
            letter = direction
        if letter == 'R':
            angle = (angle + num) % 360
        if letter == 'L': 
            angle = (angle - num) % 360
        if letter == 'N':
            north += num
        if letter == 'S':
            north += -num
        if letter == 'W':
            east += - num
        if letter == 'E':
            east += num

    return abs(north) + abs(east)

def rotate_point(point, rotation):
    '''Rotates any point around the origin. Rotation is the angle of the rotation in degrees.'''
    rotation = radians(rotation)
    point = np.array(point)
    rotation_matrix = np.array([[cos(rotation), -sin(rotation)], [sin(rotation), cos(rotation)]])
    rotated_point = rotation_matrix.dot(point)
    return [rotated_point[0], rotated_point[1]]

def move_ship_w_waypoint(_input):
    '''Ship and waypoint positions are stored in (North, East) tuples.
    https://math.stackexchange.com/questions/1058010/how-can-i-rotate-a-point-45-degrees-counterclockwise-around-any-point 
    https://math.stackexchange.com/questions/346672/2d-rotation-of-point-about-origin'''
    ship, waypoint, angle = [0, 0], [1, 10], 90

    for inst in _input:
        letter, num = inst[0], int(inst[1:])

        if letter == "F":
            ship[0] += waypoint[0] * num
            ship[1] += waypoint[1] * num
        if letter == 'R':
            waypoint = rotate_point(waypoint, num)
        if letter == 'L': 
            waypoint = rotate_point(waypoint, -num)
        if letter == 'N':
            waypoint[0] += num
        if letter == 'S':
            waypoint[0] += -num
        if letter == 'W':
            waypoint[1] += -num
        if letter == 'E':
            waypoint[1] += num

    return abs(ship[0]) + abs(ship[1])

if __name__ == "__main__":
    _input = open("aoc_12.txt").read().splitlines()
    
    print("PART 1")
    move_ship(_input)
    print("")
    print("PART 2")
    round(move_ship_w_waypoint(_input))



