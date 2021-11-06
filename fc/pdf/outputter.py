from typing import Tuple, Union

from reportlab.lib.pagesizes import LETTER, landscape as make_landscape, A4
from reportlab.pdfgen.canvas import Canvas

import fc.ast as ast
from fc.config import GRID_SIZE
from fc.pdf.frame import FrameBuilder, SymbolTable
from .config import Config


class OutputterPDF():
    def __init__(self, frame_size: Union[str, Tuple[int, int]], landscape=False) -> None:
        if type(frame_size) == str:
            if frame_size == 'A4':
                frame_size = A4
            elif frame_size == 'letter':
                frame_size = LETTER
            else:
                frame_size = A4
            if landscape:
                frame_size = make_landscape(frame_size)

        self.config = Config(GRID_SIZE, frame_size)
        self.symbol_table = SymbolTable(self.config)

    def output(self, pdf_name: str, program: ast.Program):
        self.config.set_grid_size(program.grid_size)
        self.canvas = Canvas(pdf_name, self.config.frame_size)

        frame_builder = FrameBuilder(self.config)
        for frame in frame_builder.make_frames(program):
            frame.draw(self.canvas)
            self.canvas.showPage()  # End Current Page
        self.canvas.save()
