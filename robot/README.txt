AUTONOMOUS ROBOT NAVIGATION - STARTER CODE
==========================================

This starter project contains three Python files and three map files.

1. map_reader.py
----------------

Students complete TWO tasks:

Task 1:
    read_txt_map(filename)

Read a txt file and return a nested list of symbols.

Task 2:
    convert_to_cost_map(raw_map)

Convert the symbol map into a nested list of costs.

Cost rules:

    . = 1
    S = 1
    G = 1
    B = 1
    # = None

For Challenge 4:

    g = 2
    M = 5
    W = 10

Teacher functions will check whether your output follows these rules.

2. robot.py
-----------

Complete:

    move()
    search1()
    search2()
    search3()
    record()

IMPORTANT:

search1(), search2(), and search3() mean DIFFERENT SEARCH METHODS.

They do NOT mean Challenge 1, Challenge 2, and Challenge 3.

For example, one group may choose:

    search1() = BFS
    search2() = DFS
    search3() = Dijkstra

Another group may choose different algorithms.

3. main.py
----------

The starter code only reads the three provided maps and stores:

    challenge1_map
    challenge1_start
    challenge1_goal
    challenge1_bonuses

    challenge2_map
    challenge2_start
    challenge2_goal
    challenge2_bonuses

    challenge3_map
    challenge3_start
    challenge3_goal
    challenge3_bonuses

Students should write the rest of main.py themselves:

    - create Robot objects
    - call search methods
    - compare algorithms
    - print results
    - visualize results

MAP FILES
---------

maps/challenge1.txt
maps/challenge2.txt
maps/challenge3.txt

Symbols:

    .  normal cell
    S  start
    G  goal
    B  bonus
    #  obstacle

For Challenge 4:

    g  grass
    M  mud
    W  water
