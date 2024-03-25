from typing import Any

import fire

from soda.scan import Scan


def check(
    scan_name: str, check_subdir: str, data_source: str = "online_retail"
) -> Any:  # noqa E501
    print("Running Soda Scan...")
    config_file = "configuration.yml"
    checks_path = "./checks"

    if check_subdir:
        checks_path += f"/{check_subdir}"

    # Configure Scan object
    scan = Scan()
    scan.set_verbose()
    scan.add_configuration_yaml_file(config_file)
    scan.set_data_source_name(data_source)
    scan.add_sodacl_yaml_files(checks_path)
    scan.set_scan_definition_name(scan_name)

    # Run scan and get results
    result = scan.execute()
    print(scan.get_logs_text())

    if result != 0:
        raise ValueError("Scan Scan Failed")
    return result


if __name__ == "__main__":
    fire.Fire(check)
