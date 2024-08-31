# Ninja Game

<h4> Author: Zane Deso </h4>
<h4> Last Updated: 8/31/2024 </h4>


<h5> Overview </h5>
    <p>
    The purpose of this project was to complete daFluffyPotato pyGame Tutorial (2023) in 2024. Please see past commits to development history. This tutorial covered a many topics including tiles, tilemaps, physics, entities, particles, sparks, camera, parallax effect, enemies, AI, combat, level-editing, level transitions, and making executables.
    </p>

<img src="Game_Screenshot_002.jpg">
<h6> Character and world </h6>


<img src="Game_Screenshot_001.jpg">
<h6> Dash Particles and hit sparks </h6>
<br>

<h5> Code Examples </h5>
    <p>
    The camera in the game follows the player's movement in a way that ramps to the player's location. Effectively this will create a smoother camera transition that gradually slows down as the camera location more closely aligns with the player's lcoation. The code below uses a constant of 24 as a means to divide the distance of the camera's location to the player's location each frame.
    </p>
    ```
    self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) /24
    self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) /24
    render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
    ```