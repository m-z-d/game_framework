from threading import Thread
from typing import Callable, Any,Iterable,Mapping


class RenderThread(Thread):
    def __init__(self, group: None = ..., target: Callable[..., object] | None = ...,
                 name: str | None = ..., args: Iterable[Any] = ...,
                 kwargs: Mapping[str, Any] | None = ..., *, daemon: bool | None = ...,parentRenderer) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._parent=parentRenderer


class Renderer():
    """
    (values used are rounded to 4 ndigits)"""
    def __init__(self) -> None:
        self.thread = RenderThread(parentRenderer=self,target=self.rendering_loop)
        self._time_from_last_frame_seconds: float=0.000
        self._time_between_frames_seconds: float=0.0167  #default: 60fps

    def set_framerate(self,framerate_frames_per_second) -> None:
        self._time_between_frames_seconds=round(1/framerate_frames_per_second,4)
    
    def rendering_loop(self):
        pass
