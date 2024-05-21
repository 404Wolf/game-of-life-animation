from time import sleep

class Printer:
    """
    A class for printing frames to the console for animation.

    Attributes:
        number_of_lines: The number of lines to print and then redraw.
    """

    def __init__(self, number_of_lines: int):
        self._number_of_lines = number_of_lines
        self._draw_frame()

    def _build_control_sequence(self, operator: str, modifier: int = None, control_sequence_introducer='\033[') -> str:
        """
        Build the control sequence to move the cursor up by the number of lines.

        Arguments:
            operator: The action that we are taking. A one character string.
            modifier: The thing that comes after the [ to modify things like the number of lines to erase.
        """
        modifier = str(modifier) if modifier is not None else ""
        assert len(operator) == 1, f"Operator must be a single character, got {operator}"
        return f"{control_sequence_introducer}{modifier}{operator}"

    def _remove_n_lines_above(self, number_of_lines: int, **kwargs) -> None:
        """
        Remove a specific number of lines above the current cursor position.

        Arguments:
            number_of_lines: The number of lines to remove.
            **kwargs: Additional keyword arguments to pass to the print function. "end" is set to "" automatically.
        """
        kwargs["end"] = ""
        print(self._build_control_sequence("F", number_of_lines), **kwargs)
        print(self._build_control_sequence("J"), **kwargs)

    def _draw_frame(self):
        """
        Draw the initial frame.
        """
        print("\n" * (self._number_of_lines - 1), end="", flush=True)

    def redraw_frame(self, string: str) -> None:
        """
        Print the content to the console, ensuring that it has the correct number of lines.

        Arguments:
            *args: The content to print.
            **kwargs: Additional keyword arguments to pass to the print function.
        """
        if (lines_in_string := string.count("\n")) != self._number_of_lines - 1:
            raise ValueError(f"Expected {self._number_of_lines} lines, got {lines_in_string + 1}")
        self._remove_n_lines_above(self._number_of_lines - 1, flush=False)
        print(string, end="", flush=True)
