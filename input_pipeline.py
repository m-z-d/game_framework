from dataclasses import dataclass
from typing import Literal, Callable, Any
from threading import Thread
from sys import platform
from logging import log as l, basicConfig, INFO, WARNING, DEBUG

basicConfig(filename="input_debug.log")


@dataclass
class EventObject:
    """Base event class, inherited by all event types"""

    value: str
    extra_arguments: list = []


class InputEvent(EventObject):
    """Class for input events. used with `KeyboardInputAgent`.\n
    the event's `value` is the input characters.\n
    the event's `extra_arguments` should be empty when triggered by a `KeyboardInputAgent`.\n
    the event's `input_type` is the context to determine how an event should be handled. 
    Most useful when a function is set to listen to more than one type of `InputEvent`
    """

    input_type: Literal[
        "InputEvent", "SingleKeyEvent", "SequenceEvent", "SpecialEvent"
    ] = "InputEvent"


class KeyboardInputAgent:  # TODO: make sequenced mode only accessible by sending an event to the agent.
    """Interface for user input.
    functions as either single-key (Real Time) or sequenced input (buffered)"""

    def __init__(
        self, starting_mode: Literal["single-key", "sequence"] = "single-key"
    ) -> None:
        self._sk_input: Callable[[], str]
        self.thread: Thread = Thread(target=self._loop, daemon=True)
        self.input_cache: list[str] = []
        self.mode = starting_mode
        self._event_listeners: dict[str, list[Callable[[InputEvent], Any]]] = {
            "InputEvent": [],
            "SingleKeyEvent": [],
            "SequenceEvent": [],
        }

    def set_mode(self, mode: Literal["single-key", "sequence"]) -> None:
        if mode is Literal["single-key", "sequence"]:
            self.mode: Literal["single-key", "sequence"] = mode

    def add_listener(
        self,
        event: Literal["InputEvent", "SingleKeyEvent", "SequenceEvent"],
        function: Callable[[InputEvent], Any],
    ):
        """Adds a function `f(x)` to
        the list of functions that will be called at
        `event`'s realisation with x as `InputEvent`"""
        self._event_listeners[event].append(function)

    def get_listeners(
        self, event: Literal["InputEvent", "SingleKeyEvent", "SequenceEvent"]
    ) -> list[Callable[[InputEvent], Any]]:
        """Gets all functions currently listening to `event`'s realisation"""
        return self._event_listeners[event]

    def remove_listener(
        self,
        event: Literal["InputEvent", "SingleKeyEvent", "SequenceEvent"],
        function: Callable[[InputEvent], Any],
    ):
        """Removes a function `f(x)` from
        the list of functions listening to `event`'s realisation. Raises errors if function or event is nonexistent.
        """
        assert event in self._event_listeners
        self._event_listeners[event].remove(function)

    def _loop(self) -> None:
        while True:
            input = ""
            if self.mode == "single-key":
                input = self._sk_input()
                if input is "":
                    continue
                else:
                    for listener in self._event_listeners["SingleKeyEvent"]:
                        listener(InputEvent(value=input))
            elif self.mode == "sequence":
                input = self._seq_input()
                for listener in self._event_listeners["SequenceEvent"]:
                    listener(InputEvent(value=input))
            for listener in self._event_listeners["InputEvent"]:
                listener(InputEvent(value=input))

    def _seq_input(self) -> str:
        return input()

    def _sk_input_windows(self) -> str:
        from msvcrt import getch

        return getch().decode(encoding="ascii", errors="ignore")

    def _sk_input_linux(
        self,
    ) -> str:  # TODO: make and verify this code on a linux install
        raise NotImplementedError

    def init(self) -> None:
        """start listening for input on command line, also checks which OS it is run on and uses appropriate method of input"""
        if platform.startswith("win32"):
            l(level=INFO, msg="input:daemon starting,configured for 'win32' platform")
            self._sk_input = self._sk_input_windows
        elif platform.startswith("linux"):
            l(level=INFO, msg="input:daemon starting,configured for 'linux' platform")
            self._sk_input = self._sk_input_linux
        else:
            l(
                level=WARNING,
                msg="input:Unsupported platform, defaulting to linux behaviour.",
            )
            l(level=INFO, msg="input:daemon starting,configured for 'linux' platform")
            self._sk_input = self._sk_input_linux
        self.thread.start()
