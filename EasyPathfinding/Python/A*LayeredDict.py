"""IN ORDER TO RUN, YOU MUST DO `pip3 install arcade`

This example can be run from the command line with:
python -m EasyPathfinding.A*_example
"""

import arcade
import random

from pathfinding import AStarWLayeredDict
from customMaps import LayeredBarrierDict


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
        #For movement
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False


        # --- Path related
        # This variable holds the travel-path. We keep it as an attribute so
        # we can calculate it in on_update, and draw it in on_draw.
        self.path = None

        # Note: If the enemy sprites are the same size, we only need to calculate
        # one of these. We do NOT need a different one for each enemy. The sprite
        # is just used for a size calculation.
        self.Map = LayeredBarrierDict([], 64, 0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, base = "dirt")

        # Set up the player
        resource = ":resources:images/animated_characters/" \
                   "female_person/femalePerson_idle.png"
        self.player = arcade.Sprite(resource, scale=.5)
        self.player.center_x = 128
        self.player.center_y = 128

        # Set enemies
        resource = ":resources:images/animated_characters/zombie/zombie_idle.png"
        self.enemy = arcade.Sprite(resource, scale = .5)
        self.enemy.center_x = 640
        self.enemy.center_y = 320


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
        #player
        self.Map[2][2] = 0

        #enemy
        self.Map[10][5] = 0

    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.player.draw()
        self.wall_list.draw()
        self.enemy.draw()

        if self.path:
            arcade.draw_line_strip(self.path, arcade.color.BLUE, 2)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Calculate speed based on the keys pressed
        change_x = 0
        change_y = 0
        player = self.player

        if self.up_pressed:
            change_y += MOVEMENT_SPEED
        if self.down_pressed:
            change_y -= MOVEMENT_SPEED
        if self.left_pressed:
            change_x -= MOVEMENT_SPEED
        if self.right_pressed:
            change_x += MOVEMENT_SPEED
        
        x = player.center_x+change_x
        y = player.center_y+change_y

        if not 0<x<SCREEN_WIDTH:
            change_x = 0
        if not 0<y<SCREEN_HEIGHT:
            change_y = 0

        player.center_x += change_x
        if arcade.check_for_collision_with_list(player, self.wall_list):
            #revert move
            player.center_x -= change_x
        player.center_y += change_y
        if arcade.check_for_collision_with_list(player, self.wall_list):
            #revert move
            player.center_y -= change_y

        # NOTE: diagonal movement might cause the enemy to clip corners.
        self.path = AStarWLayeredDict(self.Map, self.player.position, self.enemy.position, allow_diagonal_movement=False, movelist=[0])

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False


def main():
    """ Main function """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, "A* Pathfinding Example")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

