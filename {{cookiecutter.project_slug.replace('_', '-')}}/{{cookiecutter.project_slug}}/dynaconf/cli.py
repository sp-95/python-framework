from typing import Mapping

import fire
from loguru import logger

from {{cookiecutter.project_slug}}.dynaconf import settings


class Main:
    def __init__(self, env: str = "development") -> None:
        settings.setenv(env)

    @staticmethod
    def project_name() -> str:
        logger.info(f"Project Name: {settings.name}")
        return settings.name

    @staticmethod
    def database(key: str = "") -> Mapping[str, str]:
        if key:
            result = {key: settings.database[key]}
            logger.info(f"{key.title()}: {result}")
        else:
            result = settings.database
            logger.info(f"Database: {result}")
        return result


def main() -> None:
    fire.Fire(Main)


if __name__ == "__main__":
    main()
