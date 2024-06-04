import unittest

from videopy.utils.utils import transform_position


class TestScenario(unittest.TestCase):

    def test_transform_position(self):
        position = ["center", "center"]
        frame = (1000, 1000)
        block = (100, 100)

        transform_without_margin = transform_position(position, frame, block)
        transform_with_margin = transform_position(position, frame, block, 50)

        assert transform_without_margin == (450, 450)
        assert transform_with_margin == (450, 450)

