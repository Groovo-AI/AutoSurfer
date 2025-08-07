from autosurfer.agent.browser_agent import AutoSurferAgent
from autosurfer.agent.browser.adapters import BrowserSettings, create_browser_adapter
from pathlib import Path


def is_browser_session_valid(browser_session):
    """Check if the browser session is still valid"""
    try:
        # Try to access the page to see if it's still responsive
        # Use a simple JavaScript evaluation instead of title() which might fail
        browser_session.page.evaluate("() => document.readyState")
        return True
    except Exception:
        return False


def main():
    print("AutoSurfer Agent Started")
    print("Type 'quit', 'exit', or press Ctrl+C to stop")

    # Ask about memory option once at the beginning
    enable_memory = True

    browser_provider = "browserbase"

    print(f"Memory: {'ENABLED' if enable_memory else 'DISABLED'}")
    print(f"Browser: {browser_provider.upper()}")
    print("Configuration set for all objectives.")

    # Create browser session once
    user_data_dir = str(
        Path("~/Library/Application Support/Autosurfer/Browser/Profile1").expanduser())
    settings = BrowserSettings(
        headless=False, user_data_dir=user_data_dir
    )
    browser_session = create_browser_adapter(browser_provider, settings)

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

            # Check if browser session is still valid, recreate if needed
            if not is_browser_session_valid(browser_session):
                print("Browser session was closed, recreating...")
                try:
                    browser_session.close()
                except:
                    pass  # Ignore errors when closing invalid session
                browser_session = create_browser_adapter(
                    browser_provider, settings)
                print("Browser session recreated successfully.")

            print(f"Processing objective: {objective}")

            surfer = AutoSurferAgent(
                objective=objective,
                browser_session=browser_session,
                enable_memory=enable_memory,
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
