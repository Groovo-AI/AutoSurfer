from autosurfer.agent.browser_agent import AutoSurferAgent

RUN_TEST_MODE = False

if __name__ == "__main__":
    # Go to chrome and open linkedin
    # task = input("Please tell me task: ")
    surfer = AutoSurferAgent()
    task = "Go to my feed and like first three posts, You might need to scroll the posts to find the like button"
    if not RUN_TEST_MODE:
        surfer.run(task)
    else:
        surfer.run_test()
