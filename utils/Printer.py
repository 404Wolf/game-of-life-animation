from time import sleep

class Printer:
    """
    A class for printing frames to the console for animation.

    Attributes:
        number_of_lines: The number of lines to print and then redraw.
    """

    def __init__(self, initial_frame: str = None, number_of_lines: int = None):
        if initial_frame:
            self._number_of_lines = initial_frame.count("\n") + 1
            self._draw_frame(initial_frame)
        else:
            self._number_of_lines = number_of_lines
            self._draw_frame()

    def _build_control_sequence(self, operator: str, modifier: int | str = None, control_sequence_introducer='\033[') -> str:
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

    def _move_cursor_to_index(self, row: int = 1, col: int = 1, **kwargs):
        """
        Moves cursor to a given index, defaults to (1,1).

        Arguments:
            **kwargs: Additional keyword arguments to pass to the print function.
        """
        kwargs["end"] = ""
        print(self._build_control_sequence("H", f"{row};{col}"), **kwargs)

    def _validate_frame(self, frame: str) -> None:
        """
        Validate that the frame has the correct number of lines.

        Arguments:
            frame: The frame to validate.
        """
        if (newline_count := frame.count("\n")) != self._number_of_lines - 1:
            raise ValueError(f"Expected {self._number_of_lines} lines, got {newline_count + 1}")

    def _draw_frame(self, frame: str = None):
        """
        Draw the initial frame.
        """
        if frame is not None:
            self._validate_frame(frame)
            print(frame, end="", flush=True)
            return
        print("\n" * (self._number_of_lines - 1), end="", flush=True)

    def redraw_frame(self, string: str) -> None:
        """
        Print the content to the console, ensuring that it has the correct number of lines.

        Arguments:
            *args: The content to print.
            **kwargs: Additional keyword arguments to pass to the print function.
        """
        self._validate_frame(string)
        self._move_cursor_to_index()
        print(string, end="", flush=True)
