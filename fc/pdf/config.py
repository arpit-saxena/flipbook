from typing import Tuple


class Config:
    def __init__(self, grid_size: Tuple[int, int], frame_size: Tuple[int, int]) -> None:
        self.frame_size = frame_size
        self.set_grid_size(grid_size)

    def set_grid_size(self, grid_size: Tuple[int, int]):
        self.grid_size = grid_size
        self.grid_square_width = self.frame_size[0] / self.grid_size[0]
        self.grid_square_height = self.frame_size[1] / self.grid_size[1]
