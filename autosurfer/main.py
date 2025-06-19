from autosurfer.agent.browser_agent import AutoSurferAgent


if __name__ == "__main__":
    surfer = AutoSurferAgent(
        objective="Go to instagram and check if logged in"
    )
    surfer.run()
