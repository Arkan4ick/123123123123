import unittest

def sum(nums, target):
    if type(target) is not int: return 'Nan'
    for x in nums:
        if type(x) is not int: return 'Nan'
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return 'Nan'


class Testsum(unittest.TestCase):
    def test_example1(self):
        self.assertEqual(sum([2,7,11,15], 9), [0,1])

    def test_example2(self):
        self.assertEqual(sum([3,2,4], 6), [1,2])

    def test_example3(self):
        self.assertEqual(sum([3,3], 6), [0,1])

    def test_no_solution(self):
        self.assertEqual(sum([1,2,3], 7), 'Nan')

    def test_negative_numbers(self):
        self.assertEqual(sum([-1, -2, -3, -4], -6), [1,3])

    def test_0(self):
        self.assertEqual(sum([0,4,3,0], 0), [0,3])

    def test_large_numbers(self):
        self.assertEqual(sum([1000000, 500000, 700000], 1500000), [0,1])

    def test_duplicates(self):
        self.assertEqual(sum([1,5,1,5], 10), [1,3])

    def test_first_last(self):
        self.assertEqual(sum([2,8,7,5], 7), [0,3])

    def test_2_nums(self):
        self.assertEqual(sum([10, -10], 0), [0,1])

    def test_empty_nums(self):
        self.assertEqual(sum([], 7), 'Nan')

    def test_1_nums(self):
        self.assertEqual(sum([5], 5), 'Nan')

    def test_float_nums(self):
        self.assertEqual(sum([1, 2.5, 3], 5), 'Nan')

    def test_float_targ(self):
        self.assertEqual(sum([1, 2, 3], 5.0), 'Nan')

    def test_str_nums(self):
        self.assertEqual(sum([1, "a", 3], 4), 'Nan')

    def test_str_targ(self):
        self.assertEqual(sum([1, 2, 3], "6"), 'Nan')

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)
