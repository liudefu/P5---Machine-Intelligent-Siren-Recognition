from unittest import TestCase
from clip_split import _find_smallest_length


class Test_find_smallest_length(TestCase):
    def test__find_smallest_length1(self):
        # arrange
        trainls = [[1,2,3], [1,2], [1,2,3,4]]
        testls = [[1,2,3], [1,2], [1,2,3,4]]
        # act
        len = _find_smallest_length(trainls, testls)

        # assert
        assert len == 2

    def test__find_smallest_length2(self):
        # arrange
        trainls = [[1,2,3], [1,2], [1,2,3,4]]
        testls = [[1,2,3], [1,2,3,4], [1,2,3,4]]
        # act
        len = _find_smallest_length(trainls, testls)

        # assert
        assert len == 2

    def test__find_smallest_length3(self):
        # arrange
        trainls = [[1,2,3], [1,2,3,4], [1,2,3,4]]
        testls = [[1,2,3], [1,2,3,4], [1,2,3,4]]
        # act
        len = _find_smallest_length(trainls, testls)

        # assert
        assert len == 3

    def test__find_smallest_length4(self):
        # arrange
        trainls = [[1,2,3], [], [1,2,3,4]]
        testls = [[1,2,3], [1,2], [1,2,3,4]]
        # act
        len = _find_smallest_length(trainls, testls)

        # assert
        assert len == 0