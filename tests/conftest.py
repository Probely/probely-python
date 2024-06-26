from pathlib import Path
from typing import Callable, Dict

import pytest
import yaml

from probely_cli.cli import build_parser


@pytest.fixture
def cli_parser():
    command_parser = build_parser()
    return command_parser


@pytest.fixture()
def create_testable_yaml_file(tmp_path: Path) -> Callable:
    """
    Returns function that generates temporary yaml file ideal
    to test file parameter of CLI commands.
    """

    def _create_testable_yaml_file(file_name: str, file_content: Dict) -> str:
        yaml_content = yaml.dump(file_content)

        testable_yaml_file: Path = tmp_path / file_name
        testable_yaml_file.write_text(yaml_content)

        return str(testable_yaml_file)

    return _create_testable_yaml_file


@pytest.fixture()
def valid_scans_start_api_response():
    scan = {
        "id": "3epwuyBoKQKN",
        "target": {
            "id": "3NnoNEvCLtsc",
            "name": "",
            "site": {
                "id": "2rKyx8J7SpFa",
                "name": "",
                "desc": "",
                "url": "http://testphp.vulnweb.com",
                "host": "testphp.vulnweb.com",
                "has_form_login": False,
                "form_login_url": "",
                "form_login_check_pattern": "",
                "form_login": [],
                "logout_detection_enabled": False,
                "has_sequence_login": False,
                "has_sequence_navigation": False,
                "has_basic_auth": False,
                "basic_auth": {"username": "", "password": ""},
                "headers": [],
                "cookies": [],
                "whitelist": [],
                "blacklist": [],
                "changed": "2024-06-19T16:58:44.469510Z",
                "changed_by": {
                    "id": "-sDw5iRCtV3Y",
                    "email": "probely@probe.ly",
                    "name": "Probely",
                },
                "auth_enabled": False,
                "logout_condition": "any",
                "check_session_url": "",
                "has_otp": False,
                "otp_secret": "",
                "otp_algorithm": "SHA1",
                "otp_digits": 6,
                "otp_field": "",
                "otp_submit": "",
                "otp_login_sequence_totp_value": "",
                "otp_type": "totp",
                "otp_url": "",
                "stack": [
                    {"id": "3XxEPJEIygTD", "name": "PHP", "desc": ""},
                    {"id": "Dzjp24cG2ZcY", "name": "Nginx", "desc": ""},
                    {"id": "TXZw0LjnntGH", "name": "Ubuntu", "desc": ""},
                ],
                "verified": True,
                "verification_token": "1088ec72-9c15-42f6-b676-e7d108feda18",
                "verification_date": None,
                "verification_method": "",
                "verification_last_error": "",
                "api_scan_settings": None,
            },
            "type": "single",
            "desc": "",
            "labels": [],
            "has_assets": False,
            "report_fileformat": "pdf",
            "scanning_agent": None,
            "teams": [],
            "blackout_period": None,
        },
        "status": "queued",
        "started": None,
        "completed": None,
        "scan_profile": "full",
        "lows": 0,
        "mediums": 0,
        "highs": 0,
        "created": "2024-06-25T10:21:09.552387Z",
        "unlimited": False,
        "changed": "2024-06-25T10:21:09.952933Z",
        "changed_by": {"id": "2aDq6BEzAK5u", "email": "", "name": "CLI_dev"},
        "stack": [],
        "crawler": {"state": "", "status": [], "warning": [], "error": []},
        "fingerprinter": {"state": "", "count": 0, "warning": [], "error": []},
        "scanner": {"state": "", "status": [], "warning": [], "error": []},
        "target_options": {
            "site": {
                "id": "2rKyx8J7SpFa",
                "name": "",
                "desc": "",
                "url": "http://testphp.vulnweb.com",
                "host": "testphp.vulnweb.com",
                "has_form_login": False,
                "form_login_url": "",
                "form_login_check_pattern": "",
                "form_login": [],
                "logout_detection_enabled": False,
                "has_sequence_login": False,
                "has_basic_auth": False,
                "basic_auth": {"username": "", "password": ""},
                "headers": [],
                "cookies": [],
                "whitelist": [],
                "blacklist": [],
                "changed": "2024-06-19T16:58:44.469510Z",
                "changed_by": {
                    "id": "-sDw5iRCtV3Y",
                    "email": "probely@probe.ly",
                    "name": "Probely",
                },
                "auth_enabled": False,
                "logout_condition": "any",
                "check_session_url": "",
                "has_otp": False,
                "otp_secret": "",
                "otp_algorithm": "SHA1",
                "otp_digits": 6,
                "otp_field": "",
                "otp_submit": "",
                "otp_login_sequence_totp_value": "",
                "otp_type": "totp",
            },
            "has_assets": False,
            "scanning_agent": None,
        },
        "has_sequence_navigation": False,
        "incremental": False,
        "reduced_scope": False,
        "crawl_sequences_only": False,
        "ignore_blackout_period": False,
        "user_data": None,
    }
    return scan
