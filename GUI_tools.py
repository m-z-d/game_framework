from typing import Any, Literal
from rendering_pipeline import Sprite
from input_pipeline import KeyboardInputAgent


class PositionVector:
    x: int
    y: int

    def __init__(
        self,
        x: int | None = None,
        y: int | None = None,
        xy: "tuple[int, int] | PositionVector |None " = None,
    ) -> None:
        """Creates a position vector from a tuple of integers, another PositionVector or from 2 integer parameters."""
        if xy is not None:
            if isinstance(xy, tuple):
                self.x, self.y = xy
            else:
                self.x, self.y = xy.x, xy.y
        elif x is not None and y is not None:
            self.x, self.y = x, y

    def copy(self):
        return PositionVector(self.x, self.y)

    def scale(self, value: "PositionVector |tuple[int,int]") -> "PositionVector":
        """returns Hadamard product of the 2 vectors. (multiplies each component of vectors together)"""
        result_vector: PositionVector = self.copy()
        if isinstance(value, tuple):
            result_vector.x *= value[0]
            result_vector.y *= value[1]
        elif type(value) == type(self):
            result_vector.x *= value.x
            result_vector.y *= value.y
        else:
            raise ValueError
        return result_vector

    def __len__(self) -> float:
        """Returns vector length"""
        return (self.x**2 + self.y**2) ** 0.5

    def __add__(self, value: "PositionVector |tuple[int,int]") -> "PositionVector":
        "Returns self+value"
        result_vector: PositionVector = self.copy()
        if isinstance(value, tuple):
            result_vector.x += value[0]
            result_vector.y += value[1]
        elif type(value) == type(self):
            result_vector.x += value.x
            result_vector.y += value.y
        else:
            raise ValueError
        return result_vector

    def __rmul__(
        self, value: "float |PositionVector |tuple[int,int]"
    ) -> "PositionVector|float":
        "Returns value*self ; for vector multiplication, works as a dot product."
        result_vector: PositionVector = self.copy()
        if isinstance(value, (float, int)):
            result_vector.x = round(result_vector.x * value)
            result_vector.y = round(result_vector.y * value)
            return result_vector  # scalar product
        else:
            if isinstance(value, tuple):
                return self.x * value[0] + self.y * value[1]  # dot product
            elif type(value) == type(self):
                return self.x * value.x + self.y * value.y  # dot product
            else:
                raise ValueError

    def __radd__(self, value: "PositionVector |tuple[int,int]") -> "PositionVector":
        return self.__add__(value)

    def __mul__(
        self, value: "float |PositionVector |tuple[int,int]"
    ) -> "PositionVector|float":
        return self.__rmul__(value)


class GUIElement:
    def __init__(
        self,
        parent,
        name: str,
        sprite: Sprite | None,
        pos: tuple[int, int] | PositionVector,
    ) -> None:
        self.name: str = name
        self.position: PositionVector = PositionVector(xy=pos)
        parent.append_child(self)
        self._absolute_position: PositionVector = parent.get_absolute_pos(self)
        self.children: list[GUIElement] = []
        self.sprite: Sprite | None = sprite
        self.sprite_nonexistent: bool = sprite is None

    def append_child(self, element):
        element.parent = self

    def get_absolute_pos(self, child: "GUIElement") -> PositionVector:
        if child in self.children:
            return self._absolute_position + child.position
        elif child == self:
            return PositionVector(0, 0)
        else:
            raise ValueError


class GUIRoot(GUIElement):
    def __init__(self, name: str) -> None:
        super().__init__(parent=self, name=name, sprite=None,pos=(0,0))
