from autosurfer.agent.browser_agent import AutoSurferAgent


if __name__ == "__main__":
    surfer = AutoSurferAgent(
        objective="Go to https://octifytechnologies.com/ and extract details about their business"
    )
    surfer.run()
