from app.config.container import Container

def main():
    container = Container()

    orchestrator_service = container.orchestrator_service()
    orchestrator_service.execute_service()


if __name__ == "__main__":
    main()