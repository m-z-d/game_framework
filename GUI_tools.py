from typing import Any, Literal
from rendering_pipeline import Sprite
from input_pipeline import KeyboardInputAgent

# TODO: Vector type instead of tuples

class GUIElement():
    def __init__(self,parent,name:str,sprite:Sprite,pos:tuple[int,int]) -> None:
        self.name: str=name
        self.position:tuple[int,int]=pos
        parent.append_child(self)
        self._absolute_position: tuple[int,int]=parent.get_absolute_pos(self)
        self.children:list[GUIElement]=[]
    def append_child(self,element):
        element.parent=self
    def get_absolute_pos(self,child:'GUIElement') -> tuple[int, int]:
        if child in self.children:
            return tuple(
                [a+b for a,b in zip(
                    self._absolute_position,child.position #TODO: Rewrite
                    )
                ]
            )  
        else:
            raise ValueError
class GUIRoot(GUIElement):
    def __init__(self,parent,name:str,sprite:Sprite,pos:tuple[int,int]) -> None:
        super().__init__(parent,name,sprite,pos)
        self._absolute_position: tuple[int,int]=(0,0)
        self.styling=""