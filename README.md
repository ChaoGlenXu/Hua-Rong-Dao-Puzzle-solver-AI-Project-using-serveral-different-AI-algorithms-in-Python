# Hua-Rong-Dao-Puzzle-solver-AI-Project-using-serveral-different-AI-algorithms-in-Python
Hua Rong Dao Puzzle solver project using serveral different AI algorithm including: DFS algorithm, A star algorithm and   Manhattan Distance heuristic Algorithm

This is an AI project that I implemented in Python.
I used 3 different AI alogrithm to solve this puzzle game called Hua Rong Dao.
The Three algorithm are : Depth First Search Algorithm, A Star Alorithm, and Manhattan Distance heuristic Algorithm
This project will output and output files that contains a optimal path to the solution

I completed this project in Feburary 2023

The puzzle looks like the following:
![The Hua Rong Dao puzzle](https://github.com/ChaoGlenXu/Hua-Rong-Dao-Puzzle-solver-AI-Project-using-serveral-different-AI-algorithms-in-Python/assets/59375616/1658be0e-5eae-4eaf-b14a-a3cddb540d7a)

![Screen Shot 2023-09-16 at 2 42 08 AM](https://github.com/ChaoGlenXu/Hua-Rong-Dao-Puzzle-solver-AI-Project-using-serveral-different-AI-algorithms-in-Python/assets/59375616/738e33ba-fcd2-4e62-af5c-f41e03296173)

Here is an example of a initial state:
```
 ^11^
 v11v
 ^<>^
 v22v
 2..2
```



We can test my program by using several initial configurations of various difficulties. For each initial configuration, we can run the following two commands:
```
python3 hrd.py --algo astar --inputfile <input file> --outputfile <output file> 

python3 hrd.py --algo dfs --inputfile <input file> --outputfile <output file>
```



For example, if we run the following commands for an input file hrd5.txt:
```
python3 hrd.py --algo astar --inputfile hrd5.txt --outputfile hrd5sol_astar.txt

python3 hrd.py --algo dfs --inputfile hrd5.txt --outputfile hrd5sol_dfs.txt
```



This project is completed by Chao(Glen) Xu 
