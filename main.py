import xml.etree.ElementTree as ET
import os
import re
import csv

def process_xml(xml_file, csv_writer):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        method_name = root.attrib.get('name', 'Unknown')
        print_count = len(root.findall('.//print'))

        assert_count = len(root.findall('.//assertEquals')) + \
                       len(root.findall('.//assertTrue')) + \
                       len(root.findall('.//assertFalse'))

        duplicates = detect_duplicate_asserts(root)
        duplicate_count = len(duplicates)

        asserts_without_message = detect_assertion_roulette(root)

        unknown_test = detect_unknown_test(root)

        empty_test = detect_empty_test(root)

        literal_count = sum(
            count_literals_in_expression(assert_elem.attrib.get('expected', '')) +
            count_literals_in_expression(assert_elem.attrib.get('actual', ''))
            for assert_elem in root.findall('.//assertEquals')
        )

        exception_count = len(root.findall('.//try'))
        if_count = len(root.findall('.//if'))
        else_count = len(root.findall('.//else'))
        for_loop_count = len(root.findall('.//LoopFor'))
        conditional_count = if_count + else_count + for_loop_count

        csv_writer.writerow([
            method_name,
            literal_count,
            print_count,
            duplicate_count,
            "Yes" if asserts_without_message else "No",
            "Yes" if unknown_test else "No",
            "Yes" if empty_test else "No",
            exception_count,
            conditional_count
        ])
    except ET.ParseError as e:
        print(f"Error parsing XML file: {xml_file}\nError: {e}")

def detect_duplicate_asserts(root):
    asserts = {}
    duplicates = []

    for assert_elem in root.findall('.//assertEquals'):
        expected = assert_elem.attrib.get('expected', '')
        actual = assert_elem.attrib.get('actual', '')

        key = (expected, actual)

        if key in asserts:
            duplicates.append(key)
        else:
            asserts[key] = 1

    return duplicates

def detect_assertion_roulette(root):
    asserts_without_message = 0
    assert_count = 0

    for assert_elem in root.findall('.//assertEquals'):
        message = assert_elem.attrib.get('message', '')
        assert_count += 1

        if not message:
            asserts_without_message += 1

    return asserts_without_message > 1 and assert_count > 1

def detect_unknown_test(root):
    has_assertions = len(root.findall('.//assertEquals')) > 0 or \
                     len(root.findall('.//assertTrue')) > 0 or \
                     len(root.findall('.//assertFalse')) > 0

    test_expected = root.find('.//Test') is not None and \
                   root.find('.//Test').get('expected') is not None

    return not has_assertions and not test_expected

def detect_empty_test(root):
    return len(root.findall('.//assertEquals')) == 0 and \
           len(root.findall('.//assertTrue')) == 0 and \
           len(root.findall('.//assertFalse')) == 0 and \
           len(root.findall('.//print')) == 0

def count_literals_in_expression(expression):
    literals_count = 0
    literals_count += len(re.findall(r'<literalNumber>(\d+)</literalNumber>', expression))
    literals_count += len(re.findall(r'<literalString>(.*?)</literalString>', expression))
    return literals_count

def read_xml_files_from_folder(folder, csv_file):
    if not os.path.exists(folder):
        print(f"The folder {folder} was not found.")
        return
    
    with open(csv_file, 'w', newline='') as output_csv:
        csv_writer = csv.writer(output_csv)
        csv_writer.writerow(["Tested Method", "Magic Literal", "Redundant Print", "Duplicated Assert", 
                             "Assertion Roulette", "Unknown Test", "Empty Test", "Number of Exceptions", 
                             "Number of Conditionals"])

        for filename in os.listdir(folder):
            if filename.endswith(".xml"):
                full_path = os.path.join(folder, filename)
                print(f"Reading file: {full_path}")
                process_xml(full_path, csv_writer)

folder_xml = r'C:\Users\nacla\OneDrive\desktop\André\xmlTestGenerator\saida'
output_csv_file = 'output.csv'

read_xml_files_from_folder(folder_xml, output_csv_file)

print("Processing completed!")
