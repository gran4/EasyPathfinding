"""IN ORDER TO RUN, YOU MUST DO `pip3 install arcade`

This example can be run from the command line with:
python -m EasyPathfinding.Search_Around_example
"""

import arcade
import random

from pathfinding import SearchTilesAround
from customMaps import LivingMap


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

MOVEMENT_SPEED = 5
VIEWPORT_MARGIN = 100


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)


        # Set the window background color
        self.background_color = arcade.color.AMAZON

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.Map = LivingMap(20, 20, 400, tilesize=64)

        # Set up the player
        resource = ":resources:images/animated_characters/" \
                   "female_person/femalePerson_idle.png"
        self.player = arcade.Sprite(resource, scale=.5)
        self.player.center_x = 320
        self.player.center_y = 320

        #set up walls
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        for column in range(15):
            for row in range(10):
                sprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", scale = .5)
                x = (column + 1) * sprite.width
                y = (row + 1) * sprite.height

                sprite.center_x = x
                sprite.center_y = y
                if random.random() < .3: #30% chance of wall
                    self.wall_list.append(sprite)
                    self.Map[sprite.center_x/64][sprite.center_y/64] = 1
        for column in range(15):
            sprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", scale = .5, center_x=column * sprite.width)
            self.wall_list.append(sprite)

            sprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", scale = .5, center_x=column * sprite.width, center_y = 9*sprite.height)
            self.wall_list.append(sprite)
            self.Map[sprite.center_x/64][sprite.center_y/64] = 1
        for row in range(1, 10):
            sprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", scale = .5, center_y = row * sprite.height)
            self.wall_list.append(sprite)
            self.Map[sprite.center_x/64][sprite.center_y/64] = 1

            sprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", scale = .5, center_x = 12*64, center_y=row * sprite.width)
            self.wall_list.append(sprite)
            self.Map[sprite.center_x/64][sprite.center_y/64] = 1
        

        #Uncover player
        self.Map[4][4] = 0
        removing = arcade.check_for_collision_with_list(self.player, self.wall_list)
        if removing: self.wall_list.remove(removing[0])


        num = SearchTilesAround(self.Map, self.player.position, allow_diagonal_movement=False, movelist=[0])
        print(num)


    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.wall_list.draw()
        self.player.draw()


def main():
    """ Main function """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, "A* Pathfinding Example")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

