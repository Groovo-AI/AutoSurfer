from autosurfer.agent.browser_agent import AutoSurferAgent


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

            print(f"Processing objective: {objective}")
            print(f"Memory: {'ENABLED' if enable_memory else 'DISABLED'}")

            surfer = AutoSurferAgent(
                objective=objective,
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
