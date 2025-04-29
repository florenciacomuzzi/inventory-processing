import re
from typing import List


def remove_line(file_path: str, line_numbers: List[int]) -> None:
    """
    Remove a specific line from a file.
    
    Args:
        :param file_path: Path to the file
        :param line_numbers:
    """
    # Read all lines from the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line_number in line_numbers:
        # Check if the line number is valid
        if line_number < 1 or line_number > len(lines):
            raise ValueError(f"Line number {line_number} is out of range. File has {len(lines)} lines.")

        # Remove the specified line (adjusting for 0-based index)
        lines.pop(line_number - 1)
    
    # Write the remaining lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

def remove_empty_lines(file_path: str) -> None:
    """
    Remove empty lines from a file.

    Args:
        file_path (str): Path to the file
    """
    # Read all lines from the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Filter out empty lines
    non_empty_lines = [line for line in lines if line.strip()]

    # Write the non-empty lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(non_empty_lines)

def remove_nontable_lines(file_path: str) -> None:
    """
    Remove non-table lines from a file.

    Args:
        file_path (str): Path to the file
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    table_lines = []
    for line in lines:
        if not line.startswith('('): # TODO make more robust
            table_lines.append(line)

    # Write the table lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(table_lines)