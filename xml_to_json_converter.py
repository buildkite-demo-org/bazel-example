import uuid
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any


def is_failure(testsuite) -> bool:
    return testsuite.get('failures') == "0" or testsuite.get('errors') == "0"


def get_failure_reason(root) -> str:
    return str(root.find(".//error").attrib['message'])


def generate_json_from_xml(xfile_path: Path) -> str:
    with open(xfile_path, 'r', encoding='utf-8') as xml_file:
        xml_input = xml_file.read()

    # Parse the XML
    root = ET.fromstring(xml_input)

    # Initialize an empty list to hold all test results
    test_results: List[Dict[str, Any]] = []

    # Iterate through test suites
    for testsuite in root.findall('testsuite'):
        # Initialize a dictionary to hold test result data
        test_result: Dict[str, Any] = {
            "id": str(uuid.uuid4()),
            "scope": "Analytics::Upload associations",
            "name": testsuite.get('name').split("/")[-1],
            "location": None,
            "file_name": testsuite.get('name'),
            "result": "passed" if not is_failure(testsuite) else "failed",
            "failure_reason": None if not is_failure(testsuite) else get_failure_reason(root),
            "failure_expanded": [],
            "history": {
                "start_at": None,
                "end_at": None,
                "duration": testsuite.get('time'),
                "children": []
            }
        }

        # Iterate through test cases
        for testcase in testsuite.findall('testcase'):
            current_time = datetime.now()
            duration_seconds = int(testcase.get("duration"))
            end_at = current_time
            start_at = current_time - timedelta(seconds=duration_seconds)

            span: Dict[str, Any] = {
                "section": testcase.get('name'),
                "start_at": str(start_at),
                "end_at": str(end_at),
                "duration": str(duration_seconds),
                "detail": {}
            }
            test_result['history']['children'].append(span)

            # Logic for extracting other details would go here

        # Add the test_result dictionary to our list
        test_results.append(test_result)

    # Convert the list of test results to JSON
    json_output: str = json.dumps(test_results, indent=2)

    return json_output


xml_file_path = Path('./test.xml')

# Call the function and print the JSON result
json_output = generate_json_from_xml(xml_file_path)

with open("./test.json", "w") as file:
    file.write(json_output)

print(json_output)
