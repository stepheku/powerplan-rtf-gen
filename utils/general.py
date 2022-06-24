"""
general_utils.py
~~~~~~~~~~~~~~~~~~~
"""

import argparse
from pathlib import Path


def get_args() -> argparse.ArgumentParser:
    """
    Parse arguments to returns a string for the file path that is
    given as an argument of the script
    """
    parser_desc = """
    PowerPlan RTF Generator: uses multiple extracts saved in CSV formats to 
    generate out RTF files (really generates DOCX files)
    """
    parser = argparse.ArgumentParser(
        description=parser_desc
    )

    parser.add_argument("--pathways-file", type=str, default=None, help="Path to the pathway file")
    parser.add_argument("--components-file", type=str, default=None, help="Path to the components file")
    parser.add_argument("--order-comments-file", type=str, default=None, help="Path to the order comments file")
    parser.add_argument("--domain", type=str, default=None, help="Cerner domain from which these extracts came")
    args = parser.parse_args()

    return args

def merge_list_of_numbers(li:list) -> str:
    """
    Given a list of numbers, this will merge consecutive numbers and return
    everything as a string
    """
    li = [int(x) for x in li]
    li.sort()
    last_num = 0
    start_num = 0
    end_num = 0
    output_str = ""
    if len(li) == 1:
        return str(li[0])
    else:
        for idx, num in enumerate(sorted(li)):
            conv_int = int(num)
            if not last_num:
                last_num = conv_int
                start_num = conv_int
                end_num = conv_int
            elif last_num + 1 == conv_int:
                last_num = conv_int
                end_num = conv_int
            else:
                if start_num != end_num:
                    output_str += f"{start_num} to {end_num}, "
                else:
                    output_str += f"{conv_int}, "

                last_num = 0
                start_num = 0
                end_num = 0

            if idx == len(li)-1:
                if start_num != end_num:
                    output_str += f"{start_num} to {end_num}, "
                else:
                    output_str += f"{conv_int}, "

    return output_str[:-2]