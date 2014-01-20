beast-arena
===========

beast-arena is a distributed simulation in which artifical creatures ("beasts") act in a two-dimensional world. The beasts act in a world of a specified size of N*N fields however for them it seems to be infinitely due to wrap-around.

Installation
============
1. Install Python -> "apt-get install python"
2. Install PIP -> "apt-get install python-pip"
3. Install python virual environment tool -> "pip install virtualenv"
4. Create a new virtual environment for the project to run -> "virtualenv BeastArena"
5. Activate the virtual environment to work on -> "source BeastArena/bin/activate"
6. Switch to the created directory -> "cd BeastArena"
7. Clone github project "BeastArena" -> "git clone https://github.com/eyeswideopen/beastArena.git"
8. Switch to the directory created by git commamnd -> "cd beastArena"
9. Install required python packages [numpy / urwid / scoop / deap] -> "pip install -r requirements"
10. [OPTIONAL] change configuration settings [e.g. urwid visualisation, rounds to play, port etc.] -> vi beast-arena.conf
11. Start a server game to connect to -> "python BeastArena.py"
12. Open a new console and navigate to the BeastArena directory again and start the virtualenv. Start the genetic beast simulator with scoop flag -> "python -m scoop GeneticBeastSimulator.py"


Components
==========

beast-arena.py: main application which includes (optional) visualisation of the simulation and a socket server for allowing network clients to participate in games
Client.py: simple console based client which connects to a server via SSL over TCP and participates with a specified beast type
clientGui/ClientGui.py: graphical client based on Qt


Configure beast-arena
=====================

Open beast-arena.conf with your favourite editor.
The most important options are:

useNetworking: if set to True, socket server allows connections from clients to participate in games. If set to False, simulation will be done locally only
useUrwidVisualisation: if set to True, simulation will be displayed graphically on the terminal using urwid, a text user interface library (similar to ncurses, included in urwid/)


Run beast-arena
===============

$ python beast-arena.py

then, optionally:
$ python Client.py
or
$ cd clientGui/; python ClientGui.py


Bugs & Questions?
=================

contact info@beast-arena.de

