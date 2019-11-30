# Game-Of-Life
A Python implementation of Conway's Game of Life

GameOfLife() spawns a grid populated with Cells() that live/die according to the
following rules:

    When a live cell:
        - has fewer than two neighbours, this cell dies
        - has more than three neighbours, this cell dies
        - has two or three neighbours, this cell stays alive

    When an empty position:
        - has exactly three neighbouring cells, a cell is created in its position
            - otherwise, it remains empty
