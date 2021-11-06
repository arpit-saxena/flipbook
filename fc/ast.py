from __future__ import annotations

from collections import namedtuple
from typing import List
from .config import GRID_SIZE

from sortedcontainers import SortedDict


class Object:
    def __init__(self, name: str) -> None:
        self.name = name


class SceneElement:
    def __init__(self, object_name: str, pos_x: int, pos_y: int) -> None:
        self.object_name = object_name
        self.pos_x = pos_x
        self.pos_y = pos_y


class Scene(Object):
    def __init__(self, name: str, scene_elements: List[SceneElement]) -> None:
        super().__init__(name)
        self.scene_elements = scene_elements

    def get_max_frame_num(self): return 0


class Image(Object):
    def __init__(self, name: str, size_x: int, size_y: int, path: str) -> None:
        super().__init__(name)
        self.size_x = size_x
        self.size_y = size_y
        self.path = path

    def get_max_frame_num(self): return 0


class TweenFrameDesc:
    def __init__(self, frame_num: int, pos_x: int, pos_y: int) -> None:
        self.frame_num = frame_num
        self.pos_x = pos_x
        self.pos_y = pos_y


class Tween(Object):
    def __init__(self, name: str, object_name: str,
                 frame_desc_list: List[TweenFrameDesc]) -> None:
        super().__init__(name)
        self.object_name = object_name
        self.frame_desc_list = SortedDict()
        for frame_desc in frame_desc_list:
            self.frame_desc_list[frame_desc.frame_num] = frame_desc.pos_x, frame_desc.pos_y

    def get_max_frame_num(self):
        return self.frame_desc_list.keys()[-1]


class Program:
    Grid = namedtuple('Grid', ['size_x', 'size_y'])

    def __init__(self) -> None:
        self.objects = []
        self.grid_size = GRID_SIZE
        self.grid_explicit = False

    def add_grid(self, size_x, size_y) -> Program:
        if self.grid_explicit:
            raise RuntimeError("Can't have more than one grid directives!")
        self.grid_explicit = True
        self.grid_size = tuple((size_x, size_y))
        return self

    def add_object(self, object: Object) -> Program:
        self.objects.append(object)
        return self

    def get_max_frame_num(self) -> int:
        return max(obj.get_max_frame_num() for obj in self.objects)
