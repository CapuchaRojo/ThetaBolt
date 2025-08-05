# Main application entrypoint

from core.controller import Controller


def main():
    """Initializes and starts the agent swarm."""
    controller = Controller()
    controller.start_swarm()


if __name__ == "__main__":
    main()
