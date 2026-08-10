# agent.py
import random


class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        pos = percept.get('agent_pos', (0, 0))
        return random.choice(self.actions_pool)


class SimpleReflexAgent:
    """
    Step 1.2: Simple Reflex Agent
    - Uses strictly IF-THEN Condition-Action rules.
    - No __init__ / no internal memory.
    - Reacts ONLY to the current percept.
    """

    def sense_and_act(self, percept: dict) -> str:
        # Condition-Action Rule 1: IF food_here THEN act (any valid action)
        if percept.get('food_here', False):
            return 'Up'

        # Condition-Action Rule 2: IF wall_ahead THEN change direction
        if percept.get('wall_ahead', False):
            return 'Left'

        # Condition-Action Rule 3: ELSE move forward
        return 'Up'


class ModelBasedAgent:
    """
    Step 1.3: Model-Based Agent
    - Maintains internal memory (__init__) to track state.
    - Uses a Transition Model (how actions change the world)
      and Sensor Model (how percepts update beliefs).
    - Can escape loops because it remembers previous failures.
    """

    def __init__(self):
        # Internal memory state
        self.visited_cells = set()
        self.last_action = None
        self.wall_hits = 0  # Tracks repeated wall encounters

    def sense_and_act(self, percept: dict) -> str:
        wall_ahead = percept.get('wall_ahead', False)
        food_here = percept.get('food_here', False)

        #  SENSOR MODEL + TRANSITION MODEL 
        # Update memory based on what we sensed and what we last did
        if self.last_action is not None:
            # Remember that we visited the cell we moved into
            # (Simplified relative tracker for demonstration)
            self.visited_cells.add(self.last_action)

        # DECISION RULES (querying memory) 
        if food_here:
            action = 'Up'
        elif wall_ahead:
            # Memory-based rule: alternate direction when stuck
            self.wall_hits += 1
            if self.wall_hits % 2 == 1:
                action = 'Left'
            else:
                action = 'Right'
        else:
            # No obstacle, reset wall counter and proceed
            self.wall_hits = 0
            action = 'Up'

        self.last_action = action
        return action


class SearchAgent:
    """
    Practical 3: Problem-Solving Agent using Breadth-First Search (BFS).
    Finds the optimal (shortest) path in a static maze.
    """

    def bfs_search(self, start_pos, goal_pos, walls, grid_size):
        """
        Returns a list of actions ['Up','Down','Left','Right'] or None.
        """
        from collections import deque

        if start_pos == goal_pos:
            return []

        walls_set = set(walls)
        width, height = grid_size

        # Queue holds tuples of (position, path_to_position)
        queue = deque([(start_pos, [])])
        visited = {start_pos}

        # Actions mapped to (dx, dy).  y increases upward.
        actions = {
            'Up': (0, 1),
            'Down': (0, -1),
            'Left': (-1, 0),
            'Right': (1, 0)
        }

        while queue:
            (x, y), path = queue.popleft()

            for action, (dx, dy) in actions.items():
                nx, ny = x + dx, y + dy
                next_pos = (nx, ny)

                if 0 <= nx < width and 0 <= ny < height:
                    if next_pos not in walls_set and next_pos not in visited:
                        new_path = path + [action]

                        if next_pos == goal_pos:
                            return new_path

                        visited.add(next_pos)
                        queue.append((next_pos, new_path))

        # Goal unreachable
        return None