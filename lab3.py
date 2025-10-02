def gen_bin_tree(height, root, left_func, right_func):
    """Генерирует бинарное дерево рекурсивно.

    Args:
        height (int): Высота дерева.
        root (int): Значение в корне дерева.
        left_func (function): Функция для вычисления левого потомка.
        right_func (function): Функция для вычисления правого потомка.

    Returns:
        dict: Представление дерева в виде словаря.
    """
    if height == 0:
        return {str(root): []}

    left_val = left_func(root)
    right_val = right_func(root)

    tree = {
        str(root): [
            gen_bin_tree(height - 1, left_val, left_func, right_func),
            gen_bin_tree(height - 1, right_val, left_func, right_func)
        ]
    }
    return tree


def left_func(x):
    return 2 - (x - 1)


def right_func(x):
    return x * 2


def main():
    """Основная функция, генерирующая дерево и выводящая его в формате словаря."""
    root = 14
    height = 2

    tree = gen_bin_tree(height, root, left_func, right_func)
    print(tree)


if __name__ == '__main__':
    main()