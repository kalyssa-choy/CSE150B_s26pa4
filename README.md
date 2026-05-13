# Assignment 4: Gomoku with Monte Carlo Tree Search

Implement MCTS to play Gomoku. The base game engine is from [here](https://github.com/HackerSir/PygameTutorials/tree/master/Lesson04/Gomoku). 

## The Game

Gomoku is a popular game played on the Go board, following much simpler rules. 

- There are two players, one placing black pieces and the other white pieces, at the grid intersections of the board. 
- The two players take turns to place one piece each time. Pieces are never moved or removed from the board. 
- The players' goal is to have five pieces of their own color to form an unbroken line horizontally (`examples/ex1.png`), vertically (`examples/ex2.png`), or diagonally (`examples/ex3.png`). Of course, these are unlikely realistic games between reasonable players. A real game is more like `examples/ex4.png` (black is still very lame at the end).  
- The game engine starts with human against a random-play agent. Click any grid intersections and see what the computer does. Press enter to see a random game between two random-play agents (also press enter to pause autoplay and switch back to human vs random). Press 'm' to switch to manually playing both sides.  

If you're interested, here's a video of a competitive Gomoku game: https://www.youtube.com/watch?v=siYgHaEwmZU&ab_channel=SandraJones

## Tasks

Implement MCTS in `ai.py`.

Note that the starter code makes it clear that your MCTS should return more than just one action in the end, but also the table of winning rates for all actions for the root node (number of wins divided by total number of samples, i.e., the X-bar term in the best child formula). The tests compare these values that you compute with the correct ones for a few predefined states. 

In MCTS, the search exits when the "computation budget" is reached. The current default value is 1000, which will be used for testing. You can increase or decrease it to see the different behaviors of AI. For instance, with a budget over 6000, a correctly implemented MCTS AI should be able to play a fairly interesting game against you (although it may still make some obvious mistakes when the number of next actions to consider gets larger). 

Check the MCTS-1000.mov and MCTS-6000.mov files in the repo for a demo of the correctly implemented MCTS with 1000 and 6000 budgets respectively. There is randomness, so the behavior of your implementation does not need to exactly match the video. 

It is easy to see that good moves should be pretty close to the pieces already on the board. Thus, to accelerate search, we have limited the search to a small "active" area around existing pieces (this area uses black lines on the board, compared to grey lines in the inactive area). 

## Setting up

We'll use [uv](https://github.com/astral-sh/uv) again.
```
uv sync
source .venv/bin/activate
```

## Usage

To run the program, do:
```
uv run main.py
```

To run tests for the winning rate table in several predefined states, do:
```
uv run main.py -t 1
```

To run AI against random policy, do:
```
uv run main.py -t 2
```

The game engine starts with human against a random-play agent. Click any grid intersections and see what the computer does. Press enter to see a random game between two random-play agents (also press enter to pause autoplay and switch back to human vs random). Press 'm' to switch to manually playing both sides.  

More details can be found in `Tests` section.

## Tests

- `uv run main.py -t 1` runs tests for the winning rate table in several predefined states. Note that a budget of 1000 runs and parameter c=1 in the `best_child` function is used in the test cases. Note that the order in the table is important.

- `uv run main.py -t 2` runs your AI against a random policy. Your AI should always win. 

Because the -t 1 tests rely on how the random states are generated, you may have a correct implementation that fails it. Still, the test should be valuable for you to debug. We will only grade the -t 2 tests.

Submission
----
Only submit `ai.py` file on Gradescope for grading.

- Full (5 points): Beat random AI 10/10 times.
- Almost (3 points): Beat random AI > 8/10 times.
- Nothing (0 point): Otherwise.
 
## Due date

May-24 Sunday 11:59pm. 


## Extension (Optional)

The game gives you an opportunity for testing out many approaches that we have covered in class. 
For instance, are there any heuristic evaluation functions you can use to improve the performance? 
Can you use reinforcement learning to obtain value estimates that can supplement MCTS?

We have set up a separate Gradescope submission that pits your AI against our solution AI (not random).
We challenge you to beat our solution AI with your implementation.

If you get any nice results, we would love to hear about your strategy on slack!

This part is completely optional and moreso a thought experiment if you are interested in exploring this direction more.