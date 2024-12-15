from dataclasses import dataclass
from itertools import product, chain
import re
import os
import time
import array

ROOM_SIZE=(101, 103)


def frame_writer(room, n):
    width = ROOM_SIZE[0]
    height = ROOM_SIZE[1]

    img = []

    for x in range(width):
        row = ()
        
        for y in range(height):
            if room[(x, y)] == '#':
                row += (255, 255, 255)
            else:
                row += (0, 0, 0)

        img.append(row)

    img = flatten(img)

    with open(f'frames/frame_{n}.ppm', 'wb') as f:
        header = f'P6\n{width} {height}\n255\n'
        f.write(bytearray(header, 'ascii'))
        f.write(array.array('B', img))
    

@dataclass
class Robot:
    coords: tuple
    speed: tuple

    regex = re.compile(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)')

    def move(self, seconds):
        self.coords = (
            (self.coords[0] + self.speed[0] * seconds) % ROOM_SIZE[0],
            (self.coords[1] + self.speed[1] * seconds) % ROOM_SIZE[1]
        )

    def quadrant(self):
        middle_line = ROOM_SIZE[0] // 2
        middle_column = ROOM_SIZE[1] // 2

        if self.coords[0] == middle_line or self.coords[1] == middle_column:
            return None

        if self.coords[0] < middle_line and self.coords[1] < middle_column:
            return '1'

        if self.coords[0] < middle_line and self.coords[1] > middle_column:
            return '2'

        if self.coords[0] > middle_line and self.coords[1] < middle_column:
            return '3'

        return '4'


    @staticmethod
    def build(line):
        [pos_x, pos_y, spd_x, spd_y] = [int(i) for i in Robot.regex.findall(line)[0]]
        
        coords = (pos_x, pos_y)
        speed = (spd_x, spd_y)

        return Robot(coords=coords, speed=speed)


def print_room(room):
    for x in range(ROOM_SIZE[0]):
        for y in range(ROOM_SIZE[1]):
            print(room[(x, y)], end='')

        print()


def flatten(list_of_lists):
    "Flatten one level of nesting."
    return chain.from_iterable(list_of_lists)

    
def clear(room):
    for k in room:
        room[k] = '.'


with open('input.txt') as f:
    robots = [Robot.build(line) for line in f.readlines()]

room = {(x, y): '.' for x, y in product(range(ROOM_SIZE[0]), range(ROOM_SIZE[1]))}

for robot in robots:
    room[robot.coords] = '#'

for second in range(10_000):
    frame_writer(room, second)
    clear(room)

    for robot in robots:
        robot.move(1)
        room[robot.coords] = '#'

    print(f'{(second/10_000)*100:.3f} => {second}/10_000', end='\r')

print()
