from grid_game import GridHuntGame
from agent import SimpleReflexAgent, ModelBasedAgent


def run_with_agent(agent_class, label):
    env = GridHuntGame()
    agent = agent_class()

    print(f"\n{'='*50}")
    print(f"  {label}")
    print(f"{'='*50}")

    while not env.is_done():
        percept = env.get_percept(agent)
        action = agent.sense_and_act(percept)
        env.execute_action(agent, action)

        print(
            f"Step {env.steps:2d} | Facing: {env.facing:5s} | "
            f"Percept: {percept} | Action: {action:5s} | Score: {env.score}"
        )

    print(f"--> Game Over! Final Score: {env.score} after {env.steps} steps.")


def run_grid_hunt():
    print("=== UC Berkeley Style Small Grid Hunt Started ===")

    # Step 1.2: Observe the Simple Reflex Agent getting stuck
    run_with_agent(SimpleReflexAgent, "Simple Reflex Agent")

    # Step 1.3: Observe the Model-Based Agent using memory
    run_with_agent(ModelBasedAgent, "Model-Based Agent")


if __name__ == "__main__":
    run_grid_hunt()