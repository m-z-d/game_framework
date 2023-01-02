from math import * # pyright: reportWildcardImportFromLibrary=false 
  # yes it's a wildcard import but math is a limited library and the functions are standard
from dataclasses import dataclass
from typing import Literal,Callable,Any,NoReturn
from threading import Thread
from sys import platform
from logging import log as l,basicConfig,INFO,WARNING,DEBUG
basicConfig(filename="input_debug.log")

@dataclass
class EventObject:
    value:str
class KeyboardInputAgent():
    def __init__(self,starting_mode:Literal["single-key","sequence"]="single-key") -> None:
        self._sk_input:Callable[[],str]
        self.thread: Thread=Thread(target=self._loop,daemon=True)
        self.input_cache: list[str]=[]
        self.mode=starting_mode
        self._event_listeners:dict[str,list[Callable[[EventObject],Any]]]={
            "InputEvent":[],
            "SingleKeyEvent":[],
            "SequenceEvent":[]
        }
    def set_mode(self,mode:Literal["single-key","sequence"]) -> None:
        if mode is Literal["single-key","sequence"]:
            self.mode: Literal['single-key', 'sequence']=mode
    def add_listener(self,event:Literal["InputEvent","SingleKeyEvent","SequenceEvent"],function:Callable[[EventObject],Any]):
        """Adds a function `f(x)` to  
        the list of functions that will be called at  
        `event`'s realisation with x as `EventObject`"""
        self._event_listeners[event].append(function)
    def get_listeners(self,event:Literal["InputEvent","SingleKeyEvent","SequenceEvent"]) ->list[Callable[[EventObject],Any]]:
        """Gets all functions `f(x)` from  
        the list of functions that will be called at  
        `event`'s realisation"""
        return self._event_listeners[event]
    def remove_listener(self,event:Literal["InputEvent","SingleKeyEvent","SequenceEvent"],function:Callable[[EventObject],Any]):
        """Removes a function `f(x)` from  
        the list of functions listening to `event`'s realisation"""
        try:self._event_listeners[event].remove(function)
        except ValueError:pass

    def _loop(self) -> None:
        while True:
            if self.mode=='single-key':
                input=self._sk_input()
            elif self.mode=='sequence':
                input=self._seq_input()
            else: raise
    def _seq_input(self) -> str:return input()
    def _sk_input_windows(self) -> str:
        from msvcrt import getch
        return getch().decode(encoding="ascii",errors="ignore")
    def _sk_input_linux(self) -> str:  #TODO: make and verify this code on a linux install
        return ""

    def init(self) -> None:
        """start listening for input on command line, also checks which OS it is run on and uses appropriate method of input"""
        if platform.startswith("win32"):
            l(level=INFO,msg="input:daemon starting,configured for 'win32' platform")
            self._sk_input=self._sk_input_windows
        elif platform.startswith("linux"):
            l(level=INFO,msg="input:daemon starting,configured for 'linux' platform")
            self._sk_input=self._sk_input_linux
        else:
            l(level=WARNING,msg="input:Unsupported platform, defaulting to linux behaviour.")
            l(level=INFO,msg="input:daemon starting,configured for 'linux' platform")
            self._sk_input=self._sk_input_linux
        self.thread.start()



a=KeyboardInputAgent()