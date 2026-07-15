from controller.main_controller import MainController
from controller.sample_controller import SampleController
from repository.sample_repository import SampleRepository


def main():
    sample_repo = SampleRepository("data/samples.json")
    sample_controller = SampleController(sample_repo)
    main_controller = MainController(sample_controller)
    main_controller.run()


if __name__ == "__main__":
    main()
