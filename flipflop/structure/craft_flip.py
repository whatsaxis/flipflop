from flipflop.structure.flip import Flip


class CraftFlip(Flip):
    """Craft Flip class, encompassing data about a craft flip."""

    materials: tuple[tuple[str, int]]

    def __init__(self, item_id: str, profit: int, materials: tuple[tuple[str, int]]):
        super().__init__(item_id, profit)

        self.materials = materials
