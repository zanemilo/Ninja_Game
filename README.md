# READ ME: DFP_pyGame_Tut_2023

## Author: Zane Deso

## Last Updated: 8/5/2024

## Video Stop: 4:41:02
## Link: https://youtu.be/2gABYM5M0ww?list=PLX5fBCkxJmm1fPSqgn9gyR3qih8yYLvMj&t=16862

### Purpose
The purpose of this document is to serve in the tracking the progress of myself, Zane Deso, in completing daFluffyPotato pyGame Tutorial (2023) in 2024. I have hopes to learn much from this process and perhaps forming multifaceted toolset by the time I am an effective pyGame Dev. The general format will evolve with time and at this time due to constraints in time I will keep updates in Git. Please see past commits to development progress.

### Bugs

Refer to 3:50:37. 
    - Issue where wall_slide down rock tiles flickers between animations. [Fixed]
    - Problem with velocity NOT increasing to the left when wall jumping frmo the right. [Fixed]
Refer to 4:41:02.
    - Traceback (most recent call last):
        File "c:\Users\zanem\OneDrive\Desktop\SandboxEnviro\python_work\pyGames\DFP_pyGame_Tut_2023\main.py", line 142, in <module>
            Game().run()
        File "c:\Users\zanem\OneDrive\Desktop\SandboxEnviro\python_work\pyGames\DFP_pyGame_Tut_2023\main.py", line 91, in run
            enemy.update(self.tilemap, (0, 0))
        File "c:\Users\zanem\OneDrive\Desktop\SandboxEnviro\python_work\pyGames\DFP_pyGame_Tut_2023\scripts\entities.py", line 102, in update
            self.game.projectiles.append([[self.rect().centerx - 7, self.rect().centery]], -1.5, 0)
      TypeError: list.append() takes exactly one argument (3 given)
