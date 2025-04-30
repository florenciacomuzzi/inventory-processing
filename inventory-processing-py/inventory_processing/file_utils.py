from typing import List, TextIO, Union, Any
from io import StringIO
import requests


def _get_lines_from_stream(stream: Union[TextIO, StringIO, requests.Response]) -> List[str]:
    """
    Helper function to get lines from different types of streams.
    
    Args:
        stream: Input stream (TextIO, StringIO, or requests.Response)

    Returns:
        List[str]: List of lines from the stream
    """
    if isinstance(stream, requests.Response):
        # For requests.Response, decode the content and split into lines
        return stream.content.decode('utf-8').splitlines(keepends=True)
    else:
        # For TextIO and StringIO, use readlines
        return stream.readlines()


def remove_line(stream: Union[TextIO, StringIO, requests.Response], line_numbers: List[int]) -> StringIO:
    """
    Remove specific lines from a stream.
    
    Args:
        stream: Input stream to process (TextIO, StringIO, or requests.Response)
        line_numbers: List of line numbers to remove (1-based indexing)

    Returns:
        StringIO: New stream with specified lines removed
    """
    # Read all lines from the stream
    lines = _get_lines_from_stream(stream)

    for line_number in line_numbers:
        # Check if the line number is valid
        if line_number < 1 or line_number > len(lines):
            raise ValueError(f"Line number {line_number} is out of range. Stream has {len(lines)} lines.")

        # Remove the specified line (adjusting for 0-based index)
        lines.pop(line_number - 1)
    
    # Create a new StringIO with the remaining lines
    output_stream = StringIO()
    output_stream.writelines(lines)
    output_stream.seek(0)  # Reset stream position to beginning
    
    return output_stream


def remove_empty_lines(stream: Union[TextIO, StringIO, requests.Response]) -> StringIO:
    """
    Remove empty lines from a stream.

    Args:
        stream: Input stream to process (TextIO, StringIO, or requests.Response)

    Returns:
        StringIO: New stream with empty lines removed
    """
    # Read all lines from the stream
    lines = _get_lines_from_stream(stream)

    # Filter out empty lines
    non_empty_lines = [line for line in lines if line.strip()]

    # Create a new StringIO with the non-empty lines
    output_stream = StringIO()
    output_stream.writelines(non_empty_lines)
    output_stream.seek(0)  # Reset stream position to beginning
    
    return output_stream


def remove_nontable_lines(stream: Union[TextIO, StringIO, requests.Response]) -> StringIO:
    """
    Remove non-table lines from a stream.

    Args:
        stream: Input stream to process (TextIO, StringIO, or requests.Response)

    Returns:
        StringIO: New stream with non-table lines removed
    """
    # Read all lines from the stream
    lines = _get_lines_from_stream(stream)

    # Filter out non-table lines
    table_lines = [line for line in lines if not line.startswith('(')]  # TODO make more robust

    # Create a new StringIO with the table lines
    output_stream = StringIO()
    output_stream.writelines(table_lines)
    output_stream.seek(0)  # Reset stream position to beginning
    
    return output_stream

