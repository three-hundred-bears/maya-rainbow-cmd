# maya-rainbow-cmd
My first attempt at a python plug-in for Maya. 

Meant more as learning exercise to familiarize myself with the overall plug-in structure, working with Maya's undo queue, and efficiently querying the scene graph.

## Overview
py1Rainbow is a basic python command plug-in for Maya that randomizes the wireframe colors of all selected objects if such a selection exists, or all objects in the scene if not.
The optional `-b` flag forces randomized grayscale values instead.
Example:

`py1Rainbow`

![Rainbow](https://i.imgur.com/ADPONuO.png)


`py1Rainbow -b`

![Boring](https://i.imgur.com/PxJqkNt.png)
## Installation
1. Copy py1Rainbow.py into a directory within MAYA_PLUG_IN_PATH.
2. Launch a new session of Maya, and load py1Rainbowl.py within the Plug-in Manager
