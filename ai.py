from __future__ import absolute_import, division, print_function
from math import sqrt, log
from game import Game, WHITE, BLACK, EMPTY
import copy
import time
import random

class Node:
    """
    A node in the MCTS tree. Each node contains:
    - state: the current state of the game. A tuple of (player, grid) where player is WHITE or BLACK, and grid is 2D list of the board.
    - num_wins: the number of wins for the player of the parent node
    - num_visits: the number of visits to this node
    - parent: the parent node of this node
    - children: a list of child nodes
    - untried_actions: a list of actions that have not been tried yet
    - is_terminal: bool indicating if the game is over
    """
    # NOTE: modifying this block is not recommended
    def __init__(self, state, actions, parent=None):
        self.state = (state[0], copy.deepcopy(state[1]))
        self.num_wins = 0
        self.num_visits = 0
        self.parent = parent
        self.children = [] #store actions and children nodes in the tree as (action, node) tuples
        self.untried_actions = copy.deepcopy(actions)
        simulator = Game(*state)
        self.is_terminal = simulator.game_over

# NOTE: deterministic_test() requires BUDGET = 1000
# You can try higher or lower values to see how the AI's strength changes
BUDGET = 1000

class AI:
    # NOTE: modifying this block is not recommended because it affects the random number sequences
    def __init__(self, state):
        self.simulator = Game()
        self.simulator.reset(*state) #using * to unpack the state tuple
        self.root = Node(state, self.simulator.get_actions())

    def mcts_search(self):

        #TODO: Implement the main MCTS loop

        iters = 0
        action_win_rates = {} #store the table of actions and their ucb values

        # MCTS main loop: selection, expansion, rollout, backpropagation
        while(iters < BUDGET):
            if ((iters + 1) % 100 == 0):
                # NOTE: if your terminal driver doesn't support carriage returns you can use: 
                # print("{}/{}".format(iters + 1, BUDGET))
                print("\riters/budget: {}/{}".format(iters + 1, BUDGET), end="")

            # 1) Selection: descend the tree to a node to expand
            node = self.select(self.root)

            # 2) Expansion: if node has untried actions, expand one
            if (not node.is_terminal) and len(node.untried_actions) > 0:
                node = self.expand(node)

            # 3) Rollout (simulation) from the selected/expanded node
            reward = self.rollout(node)

            # 4) Backpropagation: update stats up the tree
            self.backpropagate(node, reward)

            iters += 1
        print()

        # Note: Return the best action, and the table of actions and their win values 
        #   For that we simply need to use best_child and set c=0 as return values
        _, action, action_win_rates = self.best_child(self.root, 0)

        return action, action_win_rates

    def select(self, node):

        # Tree policy: descend until a node with untried actions or terminal node
        current = node
        while not current.is_terminal:
            if len(current.untried_actions) > 0:
                return current
            # otherwise pick best child with exploration constant c=1
            best_child_node, _, _ = self.best_child(current, 1)
            # best_child returns the node instance
            current = best_child_node
        return current

    def expand(self, node):

        # TODO: add a new child node from an untried action and return this new node

        child_node = None #choose a child node to grow the search tree

        # NOTE: passing the deterministic_test() requires popping an action like this
        action = node.untried_actions.pop(0)

        # apply the action on the simulator to get the resulting state
        self.simulator.reset(*node.state)
        self.simulator.place(*action)
        new_state = self.simulator.state()
        new_actions = self.simulator.get_actions()

        child_node = Node(new_state, new_actions, parent=node)
        # store as (action, node) tuple per Node.children convention
        node.children.append((action, child_node))

        return child_node

    def best_child(self, node, c=1): 

        # TODO: determine the best child and action by applying the UCB formula

        best_child_node = None # to store the child node with best UCB
        best_action = None # to store the action that leads to the best child
        action_ucb_table = {} # {action: UCB_value}. We will use this for grading to ensure you are computing UCB correctly.

        # NOTE: deterministic_test() requires iterating in this order
        best_val = float('-inf')
        # parent visits for UCB formula; guard against log(0)
        parent_visits = node.num_visits if node.num_visits > 0 else 1
        for (action, child_node) in node.children:
            # compute exploitation (win rate) and exploration term
            if child_node.num_visits == 0:
                # if not visited, exploration priority
                ucb = float('inf') if c > 0 else 0
                win_rate = 0
            else:
                win_rate = float(child_node.num_wins) / float(child_node.num_visits)
                # UCB formula
                ucb = win_rate + c * sqrt(2 * log(parent_visits) / float(child_node.num_visits))

            # fill table with win rate (X-bar) for grading (use 0 for unvisited)
            action_ucb_table[action] = win_rate

            # choose the first child with maximum UCB (strict > to keep first on ties)
            if ucb > best_val:
                best_val = ucb
                best_child_node = child_node
                best_action = action

        return best_child_node, best_action, action_ucb_table

    def backpropagate(self, node, result):

        # Traverse up to the root, updating visit counts and win counts
        current = node
        while current is not None:
            current.num_visits += 1
            # num_wins counts wins for the player of the parent node
            if current.parent is not None:
                parent_player = current.parent.state[0]
                # result is a dict mapping player -> 1/0
                if parent_player in result and result[parent_player] == 1:
                    current.num_wins += 1
            current = current.parent

    def rollout(self, node):

        # perform rollout from node.state using the simulator's random policy
        self.simulator.reset(*node.state)
        # if the node is terminal, no moves to play
        while not self.simulator.game_over:
            move = self.simulator.rand_move()
            self.simulator.place(*move)

        # Determine reward indicator from result of rollout
        reward = {}
        if self.simulator.winner == BLACK:
            reward[BLACK] = 1
            reward[WHITE] = 0
        elif self.simulator.winner == WHITE:
            reward[BLACK] = 0
            reward[WHITE] = 1
        else:
            # no winner (shouldn't happen), set draws to 0
            reward[BLACK] = 0
            reward[WHITE] = 0
        return reward
