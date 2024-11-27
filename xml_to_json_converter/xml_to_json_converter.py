import sys
import uuid
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

def open_xml_file(path: str) -> str:
    with open(Path(path), "r") as file:
        return file.read()

def open_xml_files(base_path: Path) -> Dict[str, str]:
    xml_files_content = {}

    # Iterate over all XML files with the name "test.xml" in the directory and subdirectories
    for xml_file in base_path.rglob('test.xml'):
        # Read the content of the XML file
        with open(xml_file, 'r', encoding='utf-8') as file:
            xml_content = file.read()

        # Get the name of the directory containing the XML file
        directory_name = xml_file.parent.name

        # Add the content to the dictionary using the directory name as the key
        xml_files_content[directory_name] = xml_content

    return xml_files_content


def is_successful(testsuite) -> bool:
    return testsuite.get('failures') == "0" and testsuite.get('errors') == "0"


def get_failure_reason(root) -> str:
    return str(root.find(".//error").attrib['message'])


def generate_json_from_xml(xml: str) -> str:
    # Parse the XML
    root = ET.fromstring(xml)

    # Initialize an empty list to hold all test results
    test_results: List[Dict[str, Any]] = []

    # Iterate through test suites
    for testsuite in root.findall('testsuite'):
        # Initialize a dictionary to hold test result data
        foo = is_successful(testsuite)

        name = testsuite.get('name').split("/")[-1]
        scope = name.split("_")[-1]

        test_result: Dict[str, Any] = {
            "id": str(uuid.uuid4()),
            "scope": f"Analytics::Upload associations::{scope}",
            "name": name,
            "location": None,
            "file_name": testsuite.get('name'),
            "result": "passed" if is_successful(testsuite) else "failed",
            "failure_reason": None if is_successful(testsuite) else get_failure_reason(root),
            "failure_expanded": [],
            "history": {}
        }

        # Iterate through test cases
        for testcase in testsuite.findall('testcase'):
            current_time: datetime = datetime.now()
            duration_seconds = int(testcase.get("duration"))
            end_at: datetime = current_time
            start_at: datetime = current_time - timedelta(seconds=duration_seconds)

            history: Dict[str, Any] = {
                "start_at": int(start_at.timestamp()),
                "end_at": int(end_at.timestamp()),
                "duration": int(duration_seconds),
                "children": []
            }
            test_result['history'] = history

            # Logic for extracting other details would go here

        # Add the test_result dictionary to our list
        test_results.append(test_result)

    # Convert the list of test results to JSON
    json_output: str = json.dumps(test_results, indent=2)

    return json_output


def write_json_test_data_file(file_name: str, json_content: str) -> None:
    with open(f"./test-data-{file_name}-{datetime.now().timestamp()}.json", "w") as file:
        print(f"Writing ./test-data-{file_name}-{datetime.now().timestamp()}.json")
        file.write(json_content)



if __name__ == "__main__":
    print("### Starting XML to JSON converter ###")
    BASE_PATH: Path = Path("/tmp/bazel/execroot/_main/bazel-out/k8-fastbuild/testlogs").resolve()

    print(f"Path to bazel cache: {BASE_PATH}")

    for dir_name, xml_content in open_xml_files(BASE_PATH).items():
        print(f"Found {dir_name}/test.xml")
        json_output: str = generate_json_from_xml(xml_content)
        write_json_test_data_file(dir_name, json_output)

# if __name__ == "__main__":
#     path_to_test_xml: str = sys.argv[1]
#     print(f"Got path to test.xml: {path_to_test_xml}")
#     xml = open_xml_file(path_to_test_xml)
#     json: str = generate_json_from_xml(xml)
#     file_name = path_to_test_xml.split("/")[-2] + ".json"
#     print(json)
#     print(f"Write: {file_name}")
#     # write_json_test_data_file(file_name, json)
