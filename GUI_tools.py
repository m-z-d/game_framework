from input_pipeline import KeyboardInputAgent

class GUIRoot:
    def __init__(self) -> None:
        self.styling=""
class GUIElement():
    def __init__(self,name:str,sprite) -> None:
        self.name: str=name

    def append_child(self,element:GUIElement):
        element.parent=self
        element.