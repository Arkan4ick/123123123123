from collections import deque
from typing import Callable, Dict, Any
from dataclasses import dataclass
import unittest


# ===== ОСНОВНОЙ КОД =====

def gen_bin_tree(
    height: int = 5,
    root: int = 5,
    left_branch: Callable[[int], int] = lambda r: r + 1,
    right_branch: Callable[[int], int] = lambda r: r ** 2
) -> Dict[str, Any]:
    if height < 0:
        raise ValueError("height не может быть отрицательным")
    if not callable(left_branch):
        raise TypeError("left_branch должна быть функцией")
    if not callable(right_branch):
        raise TypeError("right_branch должна быть функцией")

    if height == 0:
        return {str(root): []}

    root_dict = {str(root): []}
    queue = deque([(root, root_dict[str(root)], 0)])

    while queue:
        current_value, current_children, current_level = queue.popleft()

        if current_level >= height:
            continue

        left_value = left_branch(current_value)
        right_value = right_branch(current_value)

        left_dict = {str(left_value): []}
        right_dict = {str(right_value): []}

        current_children.append(left_dict)
        current_children.append(right_dict)

        queue.append((left_value, left_dict[str(left_value)], current_level + 1))
        queue.append((right_value, right_dict[str(right_value)], current_level + 1))

    return root_dict


def count_nodes(tree: Dict[str, Any]) -> int:
    if not tree:
        return 0
    count = 1
    for key, children in tree.items():
        for child in children:
            count += count_nodes(child)
    return count


def get_tree_height(tree: Dict[str, Any]) -> int:
    if not tree:
        return -1
    for key, children in tree.items():
        if not children:
            return 0
        max_height = -1
        for child in children:
            max_height = max(max_height, get_tree_height(child))
        return max_height + 1
    return 0


@dataclass
class TreeNode:
    value: int
    left: 'TreeNode' = None
    right: 'TreeNode' = None


def gen_bin_tree_dataclass(
    height: int = 5,
    root: int = 5,
    left_branch: Callable[[int], int] = lambda r: r + 1,
    right_branch: Callable[[int], int] = lambda r: r ** 2
) -> TreeNode:
    if height < 0:
        raise ValueError("height не может быть отрицательным")

    root_node = TreeNode(root)
    queue = deque([(root_node, 0)])

    while queue:
        node, level = queue.popleft()
        if level >= height:
            continue

        left_value = left_branch(node.value)
        right_value = right_branch(node.value)

        node.left = TreeNode(left_value)
        node.right = TreeNode(right_value)

        queue.append((node.left, level + 1))
        queue.append((node.right, level + 1))

    return root_node


def tree_to_dict(node: TreeNode) -> Dict[str, Any]:
    if node is None:
        return {}

    if node.left is None and node.right is None:
        return {str(node.value): []}

    children = []
    if node.left:
        children.append(tree_to_dict(node.left))
    if node.right:
        children.append(tree_to_dict(node.right))

    return {str(node.value): children}


# ===== ТЕСТЫ =====

class TestGenBinTree(unittest.TestCase):

    def test_height_0(self):
        tree = gen_bin_tree(height=0, root=5)
        self.assertEqual(tree, {'5': []})

    def test_height_1(self):
        tree = gen_bin_tree(height=1, root=5)
        self.assertEqual(tree, {'5': [{'6': []}, {'25': []}]})

    def test_height_2(self):
        tree = gen_bin_tree(height=2, root=5)
        expected = {'5': [{'6': [{'7': []}, {'36': []}]}, {'25': [{'26': []}, {'625': []}]}]}
        self.assertEqual(tree, expected)

    def test_custom_params(self):
        tree = gen_bin_tree(height=1, root=14, left_branch=lambda r: 2 - (r - 1), right_branch=lambda r: r * 2)
        self.assertEqual(tree, {'14': [{'-11': []}, {'28': []}]})

    def test_count_nodes(self):
        self.assertEqual(count_nodes(gen_bin_tree(height=0, root=5)), 1)
        self.assertEqual(count_nodes(gen_bin_tree(height=1, root=5)), 3)
        self.assertEqual(count_nodes(gen_bin_tree(height=2, root=5)), 7)
        self.assertEqual(count_nodes(gen_bin_tree(height=3, root=5)), 15)

    def test_tree_height(self):
        self.assertEqual(get_tree_height(gen_bin_tree(height=0, root=5)), 0)
        self.assertEqual(get_tree_height(gen_bin_tree(height=1, root=5)), 1)
        self.assertEqual(get_tree_height(gen_bin_tree(height=2, root=5)), 2)

    def test_errors(self):
        with self.assertRaises(ValueError):
            gen_bin_tree(height=-1, root=5)
        with self.assertRaises(TypeError):
            gen_bin_tree(height=1, root=5, left_branch="not")


class TestFamily1(unittest.TestCase):

    def test_f1_h0(self):
        tree = gen_bin_tree(height=0, root=5, left_branch=lambda r: r + 1, right_branch=lambda r: r ** 2)
        self.assertEqual(tree, {'5': []})

    def test_f1_h1(self):
        tree = gen_bin_tree(height=1, root=5, left_branch=lambda r: r + 1, right_branch=lambda r: r ** 2)
        self.assertEqual(tree, {'5': [{'6': []}, {'25': []}]})

    def test_f1_h2(self):
        tree = gen_bin_tree(height=2, root=5, left_branch=lambda r: r + 1, right_branch=lambda r: r ** 2)
        expected = {'5': [{'6': [{'7': []}, {'36': []}]}, {'25': [{'26': []}, {'625': []}]}]}
        self.assertEqual(tree, expected)


class TestFamily2(unittest.TestCase):

    def test_f2_h0(self):
        tree = gen_bin_tree(height=0, root=10, left_branch=lambda r: r ** 2, right_branch=lambda r: 2 * (r + 4))
        self.assertEqual(tree, {'10': []})

    def test_f2_h1(self):
        tree = gen_bin_tree(height=1, root=10, left_branch=lambda r: r ** 2, right_branch=lambda r: 2 * (r + 4))
        self.assertEqual(tree, {'10': [{'100': []}, {'28': []}]})


class TestDataclass(unittest.TestCase):

    def test_dataclass_h0(self):
        node = gen_bin_tree_dataclass(height=0, root=5)
        self.assertEqual(node.value, 5)
        self.assertIsNone(node.left)

    def test_dataclass_h1(self):
        node = gen_bin_tree_dataclass(height=1, root=5)
        self.assertEqual(node.value, 5)
        self.assertEqual(node.left.value, 6)
        self.assertEqual(node.right.value, 25)

    def test_tree_to_dict(self):
        node = gen_bin_tree_dataclass(height=1, root=5)
        result = tree_to_dict(node)
        self.assertEqual(result, {'5': [{'6': []}, {'25': []}]})


# ===== ПРИМЕРЫ =====

def run_examples():
    print("Пример 1: height=0, root=5")
    tree = gen_bin_tree(height=0, root=5)
    print(tree)
    print()

    print("Пример 2: height=1, root=5")
    tree = gen_bin_tree(height=1, root=5)
    print(tree)
    print()

    print("Пример 3: height=2, root=5")
    tree = gen_bin_tree(height=2, root=5)
    print(tree)
    print()

    print("Пример 4: root=14, left=2-(r-1), right=r*2")
    tree = gen_bin_tree(
        height=2,
        root=14,
        left_branch=lambda r: 2 - (r - 1),
        right_branch=lambda r: r * 2
    )
    print(tree)
    print()

    print("Пример 5: Параметризованный вход ([5,0], [5,1], [5,2])")
    inp = ([5, 0], [5, 1], [5, 2])
    for root, height in inp:
        tree = gen_bin_tree(height=height, root=root)
        print(f"root={root}, height={height}: {count_nodes(tree)} узлов")
    print()

    print("Пример 6: root=10, left=r**2, right=2*(r+4)")
    for h in range(3):
        tree = gen_bin_tree(height=h, root=10, 
                           left_branch=lambda r: r ** 2,
                           right_branch=lambda r: 2 * (r + 4))
        print(f"height={h}: {tree}")
    print()

    print("Пример 7: Проверка высоты деревьев")
    for h in range(4):
        tree = gen_bin_tree(height=h, root=5)
        detected = get_tree_height(tree)
        print(f"height={h}: обнаружена {detected}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=[''], exit=False, verbosity=2)
    elif len(sys.argv) > 1 and sys.argv[1] == 'examples':
        run_examples()
    else:
        print("Использование:")
        print("  python main.py test      - запустить тесты")
        print("  python main.py examples  - запустить примеры")
