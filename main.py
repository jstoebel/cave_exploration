######################################################################
##Caves and Back Tracking
##   Jacob Stoebel (stoebelj)
## main.py
## Purpose: Runs user through a cave exploration simulation
## Aknowledgements:
##Help with the Tkinter library: 
##	http://effbot.org/tkinterbook/
##	https://stackoverflow.com/questions/15781802/python-tkinter-clearing-a-frame

import Tkinter as tk
import tkFont
from tkFileDialog import askopenfilename
from collections import deque
import numpy as np

class Cave(object):

    DIRECTIONS = {
    'n': np.array([0, -1]),
    'e': np.array([1, 0]),
    's': np.array([0, 1]),
    'w': np.array([-1, 0])
    }

    def __init__(self):
        """

        creates a cave which includes a map, a hunter, a hunter map, a search history and a display of what the hunter
        knows about the cave.
        pre: a location of a text file representing a cave.
        post: Cave object is created.
        """


        self.root = tk.Tk()     #the root display window
        self.root.withdraw()    #hide this window since its not ready.
        map_loc = pick_cave()

        raw_map = parse_map(map_loc)
        self.complete_map, self.hunter_map = build_maps(raw_map)
        self.location = self.get_hunter_loc()       #get hunters initial location
        self.history = deque()
        self.treasure_loc = []      #save locations of all treasure

        self.curr_terrain = self.get_terrain(self.location)        #initialize the current terrain

        self.seeking = True     #if the hunter is seeking treasure (False means hunter is stuck and needs to back)

        #set up display

        self.root.title("Cave Exploration")
        self.step_btn = tk.Button(self.root, text ="Step", command = self.step)
        self.step_btn.pack()

        font = tkFont.Font(family="courier", size=12)       #changing font to courier for monospacing.
        self.map = tk.Label(self.root, text="hello", font="courier")
        self.map.pack()     #loads the element into the window

        self.status = tk.Label(self.root, text="Click step to begin.", font="courier")
        self.status.pack()

        self.update()       #fetch the initial hunter_map
        self.root.deiconify()
    def update(self):
        """
        pre: none
        post: display is updated based on new hunter map

        """
        new_map = ""

        for row in self.hunter_map:
            new_map += '  '.join(row) + '\n'

        self.map.configure(text=new_map)    #configure the map element
        self.root.update_idletasks()        #refresh the window!

    def step(self):
        """
        process one step in the simulation
        pre: none
        post: hunter is moved one step in the simulation
        """
        #if we are standing on top of treasure and its new to us output the path.
        if self.curr_terrain == 'T' and self.location not in self.treasure_loc:
            self.report_path()
            self.treasure_loc.append(self.location)     #add treasure location so we don't report it twice

        if self.seeking:
            self.forward()  #try to move forward
        else:
            self.back_track()   #backtrack one step

    def move(self, to):
        """
        move hunter to coordinates and update map
        pre:
            to: to location of where the hunter is going
        post:
            hunter map is updated to reflect new position,
            self.location is updated.
        """

        old_x, old_y = self.location
        self.hunter_map[old_y][old_x] = self.complete_map[old_y][old_x]     #change previous location to terrain type

        new_x, new_y = to
        self.hunter_map[new_y][new_x] = 'M'     #hunter's new location is set.

        self.location = to      #sets new location
        self.curr_terrain = self.get_terrain(self.location)     #update current terrain
        self.update()   #update the hunter's map

    def forward(self):
        """
        hunter seeks treasure:

        the hunter's objective is to explore new terrain following this order of priority: north, east, south, west
        in other words, the hunter first attempts to explore north (if that space is not already explored) then east
        then south then west
        pre: none
        post:
            hunter's location is updated
            hunter_map is updated
            display is updated based on new hunter_map
        """

        #update status to 'Yarrr! Seeking Treasure!'
        self.status.configure(text='Yarrr! Seeking Treasure!')

        for direction in 'nesw':
            coord_mod = self.DIRECTIONS[direction]      #how should we modify our cooridnates to look in the given direction
            look_here = coord_mod + self.location

            #consult the map, have we been here before?
            x, y = look_here
            known_terrain = self.hunter_map[y][x]
            if known_terrain == '?':
                #uncharted terrain, let's see what's there.
                actual_terrain = self.inspect(direction)
                self.hunter_map[y][x] = actual_terrain  #update the hunter map based on what we found
                self.update()       #update from what we learned about new terrain
                if actual_terrain != 'W':
                    #its not a wall, let's head in that direction!
                    self.history.append(self.location)  #update history to remember where we can from
                    self.move(tuple(look_here))
                    return

        #if we get here, there was no new terrain to explore in any direction. Back track!
        self.seeking = False        #hunter needs to backtrack

    def back_track(self):
        """
        Hunter backtracks one space, based on history
        pre: none
        post: hunter back tracks to location on top of history stack
        """

        #update status
        self.status.configure(text='Yarrr! Backtracking!')
        self.update()
        try:
            back_to = self.history.pop()
        except IndexError:
            #nothing was left in stack, we must be done
            self.wrap_up()
            return

        self.move(back_to)

        self.seeking = True     #try to seek treasure again

    def report_path(self):
        """
        Report the hunter's path based on it history stack
        pre: none
        post: hunter's path is printed to the screen
        """

        print "Treasure found. Path:"

        for i in reversed(self.history):
            print tuple(i)

    def inspect(self, direction):
        """
        pre:
            :param direction: direction to inspect, in 'nsew'
        post:
            :return: returns the terrain in that direction of the hunter.
        """

        #use array addition to compute new location to inspect
        new_location = self.location + self.DIRECTIONS[direction]
        return self.get_terrain(new_location)  #inspect new_location

    def get_terrain(self, point):
        """
        gets terrain for coordinates.
        pre:
            point: a tuple of valid x, y coordinates
        post:
            :return: returns the terrain type of location at point
        """

        x, y = point        #unpack to coordinates
        assert (x >= 0 and y >= 0)      #both must be >= 0 or else we'll get strange results
        return self.complete_map[y][x]  #will return an IndexError if either coordinate is too large.

    def get_hunter_loc(self):
        """
        returns the location of the hunter
        pre: none
        post: the location of the hunter as a tuple (column, row)
        """

        for ri in xrange(len(self.hunter_map)):     #performs a linear search for the hunter
            for ci in xrange(ri):
                if self.hunter_map[ri][ci] == 'M':
                    # return (ci, ri)
                    return np.array([ci, ri])

    def wrap_up(self):
        """
        Wraps up the simulation by changing the status text box and changing the step button to a button that quits the
        program
        """

        self.step_btn.config(text='Quit', command = self.root.destroy)
        self.status.configure(text='Done exploring the cave. Yarr!')

def build_maps(map):
    """
    builds a complete_map and hunter_map based on a parsed map from file
    pre: map parsed from file
    post:
        complete_map: a map of the entire cave, with M replaced with a '.'
        hunter_map: all characters that are not "M" are replaced with "?"
    """

    hunter_map = []
    complete_map = []
    for row in map:
        h_row = ['?' if i != 'M' else 'M' for i in row]     #replace non 'M' characters with '?'
        hunter_map.append(h_row)

        c_row = [j if j != 'M' else '.' for j in row]       #replace 'M' with '.'
        complete_map.append(c_row)

    return complete_map, hunter_map

def pick_cave():
    """
    prompts user to pick a cave file
    pre: none
    post: location of  a cave file
    """

    return askopenfilename(title='Please select a cave file.')


def parse_map(cave_loc):
    """
    Prompt user to locate a cave file
    Returns map of cave and map of hunters knowledge of the cave
    pre: location of a map .txt file
    post: returns a map as a list of lists.
    """

    with open(cave_loc, 'r') as cave_file:
        coords = cave_file.readline().split()       #read the coordinates from the first line
        cols = int(coords[1])

        #next create the map
        map = []
        while True:
            line = cave_file.readline()     #readlines until we reach the end of the file
            if line:
                map.append(line.split())
            else:
                break

    return map      #builds and returns a compelte_map and hunter_map

def main():
    # cave_loc = r'caves/cave2.txt'
    # cave_loc = pick_cave()
    cave = Cave()
    while cave.seeking or cave.history:     #continue as long as we are seeking, or have somewhere to backtrack to.
        cave.root.mainloop()
    quit()

if __name__ == '__main__':
    main()
