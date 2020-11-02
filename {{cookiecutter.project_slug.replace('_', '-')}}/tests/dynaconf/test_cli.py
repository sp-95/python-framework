#!/usr/bin/env python
"""Tests for `{{ cookiecutter.project_slug }}` package."""
from pathlib import Path

import pytest
from _pytest.logging import LogCaptureFixture
from dynaconf.vendor.box.exceptions import BoxKeyError

from {{cookiecutter.project_slug}}.dynaconf.cli import Main


class TestMain:
    @staticmethod
    def test_project_name(caplog: LogCaptureFixture) -> None:
        project_name = Main.project_name()
        assert "Project Name: " in caplog.text
        assert project_name == "{{ cookiecutter.project_slug.replace('_', '-') }}"

    @staticmethod
    def test_database(caplog: LogCaptureFixture) -> None:
        with pytest.raises(BoxKeyError):
            Main.database(key="test")

        # dynaconf sets your default env to 'development'
        database = Main.database()
        assert "Database: " in caplog.text
        expected = {
            "host": "localhost",
            "user": "dev_user",
        }
        if Path("configs/.secrets.yaml").exists():
            expected.update({"password": "dev_password"})
        assert database == expected

        database = Main("default").database("user")
        assert "User: " in caplog.text
        assert database == {"user": "default"}

        # Once your env is set it won't change
        database = Main.database("user")
        assert "User: " in caplog.text
        assert database == {"user": "default"}
