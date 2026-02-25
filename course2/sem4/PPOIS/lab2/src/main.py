try:
    from .app import AppController, MainView, PlayerRepository
except ImportError:
    from app import AppController, MainView, PlayerRepository


def main() -> None:
    controller = AppController(PlayerRepository())
    view = MainView(controller)
    controller.bind_view(view)
    controller.run()


if __name__ == "__main__":
    main()
