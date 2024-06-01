<div align="center">

# `py1Rainbow`

A quick, simple command allowing a user to create an easy visual distinction between different objects in the viewport without polluting the dependency graph.

</div>

## Overview
`py1Rainbow` is a basic python command plug-in for Maya that randomizes the wireframe colors of all selected objects if such a selection exists, or all objects in the scene if not. The optional `-b` flag forces randomized grayscale values instead.

This is meant to be a simple quality-of-life addition allowing artists to easily tell at a glance which geometry is its own, distinct object without polluting the dependency graph with temporary shaders.

This command is undo-able.

## Quickstart

Select which objects you'd like to apply the operation to, or leave the selection empty to apply it to every object in the scene. Then simply invoke `py1Rainbow` from the MEL command line.

![Rainbow](https://i.imgur.com/ADPONuO.png)
___

To restrict the random colors to grayscale values, add the `-b` flag to the command, like so: `py1Rainbow -b`

![Boring](https://i.imgur.com/PxJqkNt.png)

> [!NOTE]
> This option is largely redundant, and was added so that I could learn the syntax for optional flags in API 1.0 command plugins. 

## Installation
1. Copy `py1Rainbow.py` into a directory within `MAYA_PLUG_IN_PATH`
2. Launch a new session of Maya
3. Open the Plug-in Manager and load `py1Rainbowl.py`
