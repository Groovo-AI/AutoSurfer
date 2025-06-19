from autosurfer.agent.browser_agent import AutoSurferAgent

RUN_TEST_MODE = False

if __name__ == "__main__":
    # Go to chrome and open linkedin
    # task = input("Please tell me task: ")
    surfer = AutoSurferAgent()
    task = ""
    if not RUN_TEST_MODE:
        surfer.run(task)
    else:
        surfer.run_test()
