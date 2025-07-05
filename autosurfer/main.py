from autosurfer.agent.browser_agent import AutoSurferAgent
from autosurfer.agent.browser.adapters import BrowserSettings, create_browser_adapter


def main():
    print("AutoSurfer Agent Started")
    print("Type 'quit', 'exit', or press Ctrl+C to stop")

    while True:
        try:
            objective = input(
                "\n[Bot] Please tell me what needs to be done: ").strip()

            if objective.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if not objective:
                print("Please provide a valid objective.")
                continue

            # Ask about memory option
            memory_choice = input(
                "\n[Bot] Enable agent memory? (y/n, default: n): ").strip().lower()
            enable_memory = memory_choice in ['y', 'yes']

            # Ask about browser provider
            provider_choice = input(
                "\n[Bot] Use BrowserBase? (y/n, default: n): ").strip().lower()
            browser_provider = "browserbase" if provider_choice in [
                'y', 'yes'] else "playwright"

            print(f"Processing objective: {objective}")
            print(f"Memory: {'ENABLED' if enable_memory else 'DISABLED'}")
            print(f"Browser: {browser_provider.upper()}")

            settings = BrowserSettings(headless=True)
            browser_session = create_browser_adapter(
                browser_provider, settings)
            surfer = AutoSurferAgent(
                objective=objective,
                browser_session=browser_session,
                enable_memory=enable_memory
            )
            surfer.run()

        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user. Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again with a different objective.")
            continue


if __name__ == "__main__":
    main()
