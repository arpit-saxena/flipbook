from __future__ import annotations

from typing import Dict, Iterable, List, Set, Tuple, Union

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader

import fc.ast as ast
from .config import Config


class SymbolException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Image:
    def __init__(self, ast_image: ast.Image, config: Config) -> None:
        self.name = ast_image.name
        self.image_reader = ImageReader(ast_image.path)
        self.size = (ast_image.size_x * config.grid_square_width,
                     ast_image.size_y * config.grid_square_height)


class SymbolTable:
    def __init__(self, config) -> None:
        self._symbols: Dict[str, Union[Image, ast.Object]] = {}
        self.config = config

    def add_symbol(self, object: ast.Object) -> Union[Image, ast.Object]:
        if object.name in self._symbols:
            raise SymbolException(f"Redefinition of name {name}")

        if type(object) == ast.Image:
            object = Image(object, self.config)
        self._symbols[object.name] = object
        return object

    def find_symbol(self, name: str) -> Union[Image, ast.Object, None]:
        return self._symbols.get(name)


class Frame:
    def __init__(self) -> None:
        self.images: List[Tuple[Image, Tuple[int, int]]] = []

    def add_image(self, image: Image, pos: Tuple[int, int]) -> None:
        self.images.append((image, pos))

    def draw(self, canvas: Canvas):
        for image, pos in self.images:
            canvas.drawImage(image.image_reader, pos[0], pos[1], image.size[0],
                             image.size[1], preserveAspectRatio=True, mask='auto')


class FrameBuilder:
    def __init__(self, config: Config) -> None:
        self.symbol_table = SymbolTable(config)
        self.config = config

    def make_frames(self, program: ast.Program) -> Iterable[Frame]:
        max_frame_num = program.get_max_frame_num()
        self.frames = [Frame() for _ in range(max_frame_num)]
        for object in program.objects:
            self.symbol_table.add_symbol(object)

        main_scene = self.symbol_table.find_symbol("main")
        if main_scene is None:
            raise SymbolException(f"'main' scene not found")
        elif type(main_scene) != ast.Scene:
            raise SymbolException(
                f"'main' name needs to be for a scene, not {type(main_scene)}")

        # Main scene starts at (0, 0)
        self._draw_scene(main_scene, (0, 0))
        return self.frames

    def _draw_scene(self, scene: ast.Scene, position: Tuple[int, int], start_frame: int = 0, frame_offset: int = -1):
        if frame_offset == -1:
            min_frame = start_frame
            max_frame = len(self.frames)-1
        else:
            min_frame = start_frame+frame_offset
            max_frame = start_frame+frame_offset

        for scene_elem in scene.scene_elements:
            object = self.symbol_table.find_symbol(scene_elem.object_name)

            object_offset = (
                scene_elem.pos_x * self.config.grid_square_width, scene_elem.pos_y * self.config.grid_square_height)

            object_pos = (position[0] + object_offset[0],
                          position[1] + object_offset[1])

            if object is None:
                raise SymbolException(
                    f"object {scene_elem.object_name} used before definition")
            elif type(object) == Image:
                self._draw_image(object, object_pos, min_frame, max_frame)
            elif type(object) == ast.Scene:
                self._draw_scene(object, object_pos, start_frame, frame_offset)
            elif type(object) == ast.Tween:
                if frame_offset == -1:
                    for frame_num in range(min_frame, max_frame+1):
                        self._draw_tween(object, object_pos,
                                         start_frame, frame_num-start_frame)
                else:
                    self._draw_tween(object, object_pos,
                                     start_frame, frame_offset)
            else:
                raise Exception(f"Don't know how to draw type {type(object)}")

    def _draw_image(self, image: Image, pos: Tuple[int, int], min_frame=0, max_frame=-1) -> None:
        if max_frame == -1:
            max_frame = len(self.frames)

        for i in range(min_frame, max_frame+1):
            self.frames[i].add_image(image, pos)

    def _draw_tween(self, tween: ast.Tween, pos: Tuple[int, int], start_frame: int, frame_offset: int):
        # A tween can actually have another tween as a member too which would
        # mean that the max frame we've calculated isn't correct.
        # We ignore this problem now and leave it for later.
        # TODO: Fix frame count calculation

        iter = tween.frame_desc_list.irange(maximum=frame_offset, reverse=True)
        try:
            frame_off_beg = next(iter)
            beg_idx_x, beg_idx_y = tween.frame_desc_list[frame_off_beg]
            frame_off_end = next(
                tween.frame_desc_list.irange(minimum=frame_off_beg+1))
            end_idx_x, end_idx_y = tween.frame_desc_list[frame_off_end]

            num_frames = frame_off_end - frame_off_beg
            completion_frac = (frame_offset - frame_off_beg) / num_frames

            pos_x = self.config.grid_square_width * \
                (beg_idx_x + completion_frac * (end_idx_x - beg_idx_x))
            pos_y = self.config.grid_square_height * \
                (beg_idx_y + completion_frac * (end_idx_y - beg_idx_y))
        except StopIteration:  # We're past or at the end of the tween frame sequence
            # Get max frame
            _, (idx_x, idx_y) = tween.frame_desc_list.items()[-1]
            pos_x = idx_x * self.config.grid_size[0]
            pos_y = idx_y * self.config.grid_size[1]

        pos = (pos[0] + pos_x, pos[1] + pos_y)
        frame_num = start_frame + frame_offset

        tweened_obj = self.symbol_table.find_symbol(tween.object_name)
        if tweened_obj is None:
            raise SymbolException(
                f"Object named {tween.object_name} not found. Referred in tween {tween.name}")
        elif type(tweened_obj) == Image:
            self._draw_image(tweened_obj, pos,
                             min_frame=frame_num, max_frame=frame_num)
        elif type(tweened_obj) == ast.Tween:
            self._draw_tween(tweened_obj, pos, start_frame, frame_offset)
        elif type(tweened_obj) == ast.Scene:
            self._draw_scene(tweened_obj, pos, start_frame, frame_offset)
        else:
            raise Exception(
                f"Don't know how to tween type {type(tweened_obj)}")
