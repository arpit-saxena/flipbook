from __future__ import annotations

from collections import namedtuple
from typing import List
from .config import GRID_SIZE


class Object:
    pass


class SceneElement:
    def __init__(self, object_name: str, pos_x: int, pos_y: int) -> None:
        self.object_name = object_name
        self.pos_x = pos_x
        self.pos_y = pos_y


class Scene(Object):
    def __init__(self, name: str, scene_elements: List[SceneElement]) -> None:
        self.name = name
        self.scene_elements = scene_elements


class Image(Object):
    def __init__(self, name: str, size_x: int, size_y: int, path: str) -> None:
        self.name = name
        self.size_x = size_x
        self.size_y = size_y
        self.path = path


class TweenFrameDesc:
    def __init__(self, frame_num: int, pos_x: int, pos_y: int) -> None:
        self.frame_num = frame_num
        self.pos_x = pos_x
        self.pos_y = pos_y


class Tween(Object):
    def __init__(self, name: str, object_name: str,
                 frame_desc_list: List[TweenFrameDesc]) -> None:
        self.name = name
        self.object_name = object_name
        self.frame_desc_list = frame_desc_list


class Program:
    Grid = namedtuple('Grid', ['size_x', 'size_y'])

    def __init__(self) -> None:
        self.objects = []
        self.grid_size = GRID_SIZE

    def add_header(self, header) -> Program:
        if type(header) == Program.Grid:
            self.grid_size = header.size_x, header.size_y
        else:
            raise f"Unknown header type {type(header)}"

        return self

    def add_object(self, object: Object) -> Program:
        self.objects.append(object)
        return self
