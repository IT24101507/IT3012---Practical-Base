# agent.py
import random
from collections import deque
import heapq 


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
    Practical 3: Problem-Solving Agent.
    Implements BFS, DFS, and UCS to find paths to food.
    """

    def __init__(self):
        self.plan = [] 
        self.active_algo = 'BFS'  #BFS, DFS, UCS

    def sense_and_act(self, percept: dict) -> str:
        """
        Forms a complete plan and executes it step-by-step.
        """
        # Extract global state from percept
        start_pos = percept.get('agent_pos') 
        goal_list = percept.get('all_food', [])
        walls = set(percept.get('walls', []))
        grid_size = percept.get('grid_size', (10, 10))

        # 2. Check if self.plan is empty
        if not self.plan:
            if not goal_list or not start_pos:
                return 'Up' # Default if no goals exist

            # 3. Find the closest food pellet (using Manhattan distance)
            start_node = tuple(start_pos)
            closest_food = min(goal_list, key=lambda g: abs(g[0]-start_node[0]) + abs(g[1]-start_node[1]))
            goal_node = tuple(closest_food)

            # Execute the search method matching self.active_algo
            if self.active_algo == 'BFS':
                self.plan = self.bfs_search(start_node, goal_node, walls, grid_size)
            elif self.active_algo == 'DFS':
                self.plan = self.dfs_search(start_node, goal_node, walls, grid_size)
            elif self.active_algo == 'UCS':
                self.plan = self.ucs_search(start_node, goal_node, walls, grid_size)

        # 4. Return the first action from the plan
        if self.plan:
            return self.plan.pop(0)
        
        return 'Up' # Stay put or move forward if no plan could be made

    def get_neighbors(self, pos, walls, grid_size):
        """Helper to find valid adjacent tiles."""
        x, y = pos
        width, height = grid_size
        actions = {
            'Up': (0, 1),
            'Down': (0, -1),
            'Left': (-1, 0),
            'Right': (1, 0)
        }
        neighbors = []
        for action, (dx, dy) in actions.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in walls:
                neighbors.append((action, (nx, ny)))
        return neighbors

    def bfs_search(self, start_pos, goal_pos, walls, grid_size):
        """BFS: Explores the shallowest nodes first using a FIFO queue."""
        if start_pos == goal_pos: return []

        queue = deque([(start_pos, [])])
        visited = {start_pos}

        while queue:
            current_pos, path = queue.popleft() # FIFO

            for action, next_pos in self.get_neighbors(current_pos, walls, grid_size):
                if next_pos == goal_pos:
                    return path + [action]
                if next_pos not in visited:
                    visited.add(next_pos)
                    queue.append((next_pos, path + [action]))
        return []

    def dfs_search(self, start_pos, goal_pos, walls, grid_size):
        """DFS: Explores the deepest nodes first using a LIFO stack."""
        if start_pos == goal_pos: return []

        stack = [(start_pos, [])]
        visited = {start_pos}

        while stack:
            current_pos, path = stack.pop() # LIFO

            if current_pos == goal_pos:
                return path

            for action, next_pos in self.get_neighbors(current_pos, walls, grid_size):
                if next_pos not in visited:
                    visited.add(next_pos)
                    stack.append((next_pos, path + [action]))
        return []

    def ucs_search(self, start_pos, goal_pos, walls, grid_size):
        """UCS: Explores based on lowest path cost g(n) using a Priority Queue."""
        # Priority Queue stores: (total_cost, current_pos, path)
        pq = [(0, start_pos, [])]
        visited = {} # Stores the cheapest cost found to reach a node

        while pq:
            cost, current_pos, path = heapq.heappop(pq)

            if current_pos == goal_pos:
                return path

            # Graph Search check: only proceed if this is a cheaper path
            if current_pos in visited and visited[current_pos] <= cost:
                continue
            visited[current_pos] = cost

            for action, next_pos in self.get_neighbors(current_pos, walls, grid_size):
                new_cost = cost + 1 # Assuming uniform cost of 1 per move
                heapq.heappush(pq, (new_cost, next_pos, path + [action]))
        return []