from lark import Lark, Transformer

from typing import List, TextIO

from lark.lexer import Token
from lark.visitors import Discard

from .config import GRAMMAR_PATH
from .ast import Image, Object, Program, SceneElement, Tween, TweenFrameDesc, Scene


class TreeToProgram(Transformer):
    def __init__(self) -> None:
        super().__init__()
        self._program = Program()

    def grid(self, tok: Token):
        size_x, size_y = tok
        self._program.grid_size = (size_x, size_y)
        return Discard

    def identifier(self, tok: Token):
        string, = tok
        print(string)
        return string

    def image(self, tok: Token):
        ident, size_x, size_y, path = tok
        path = path[1:-1]
        return Image(ident, size_x, size_y, path)

    def frame_desc(self, tok: Token):
        frame_num, pos_x, pos_y = tok
        return TweenFrameDesc(frame_num, pos_x, pos_y)

    def frame_desc_list(self, tok: List[TweenFrameDesc]):
        return tok

    def tween(self, tok: Token):
        name, obj_name, frame_list = tok
        return Tween(name, obj_name, frame_list)

    def scene_element(self, tok: Token):
        object_name, pos_x, pos_y = tok
        return SceneElement(object_name, pos_x, pos_y)

    def scene_element_list(self, tok: List[SceneElement]):
        return tok

    def scene(self, tok: Token):
        name, scene_element_list = tok
        return Scene(name, scene_element_list)

    def program(self, tok: List[Object]):
        for obj in tok:
            if obj is not Discard:
                self._program.add_object(obj)
        return self._program


class Parser:
    def __init__(self) -> None:
        with open(GRAMMAR_PATH, 'r') as f:
            self.parser = Lark(f.read(), parser='lalr',
                               transformer=TreeToProgram())

    def parse(self, f: TextIO) -> Program:
        return self.parser.parse(f.read())
