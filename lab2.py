import unittest


def get_user_input():
    """
    Запрашивает у пользователя:
    - способ ввода: диапазон или список
    - целевое число
    - тип поиска (бинарный или последовательный)

    Возвращает:
        tuple: (nums, target, guess_type)
    """
    while True:
        choice = input("Введите '1', чтобы ввести диапазон, или '2', чтобы ввести список: ").strip()
        if choice == '1':
            a = int(input('Введите минимальное число в диапазоне: '))
            b = int(input('Введите максимальное число в диапазоне: '))
            nums = list(range(a, b + 1))
            break
        elif choice == '2':
            nums = input('Введите числа через пробел: ')
            try:
                nums = list(map(int, nums.split()))
                if not nums:
                    print("Список не может быть пустым.")
                    continue
            except ValueError:
                print("Пожалуйста, введите только числа, разделённые пробелом.")
                continue
            break
        else:
            print("Некорректный выбор. Введите 1 или 2.")

    target = int(input('Введите целевое число: '))
    guess_type = int(input('Выберите тип поиска (1 — бинарный, 2 — последовательный): '))
    return nums, target, guess_type


def binary_search(nums, target):
    """
    Выполняет бинарный поиск в отсортированном списке.

    Args:
        nums (list): Отсортированный список целых чисел.
        target (int): Целевое число для поиска.

    Returns:
        list or None: Список [цель, количество шагов], если найдено; иначе None.
    """
    count = 0
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        count += 1
        if nums[mid] == target:
            return [target, count]
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return None


def sequential_search(nums, target):
    """
    Выполняет последовательный поиск в списке.

    Args:
        nums (list): Список целых чисел.
        target (int): Целевое число для поиска.

    Returns:
        list or None: Список [цель, количество шагов], если найдено; иначе None.
    """
    for i, num in enumerate(nums, start=1):
        if num == target:
            return [target, i]
    return None


def main(guess_type, nums, target):
    """
    Основная функция, которая вызывает нужный метод поиска.

    Args:
        guess_type (int): 1 — бинарный, 2 — последовательный.
        nums (list): Список чисел.
        target (int): Целевое число.

    Returns:
        list or str: Результат поиска или сообщение об ошибке.
    """
    if guess_type == 1:
        sorted_nums = sorted(nums)  # Бинарный поиск требует сортировки
        result = binary_search(sorted_nums, target)
    elif guess_type == 2:
        result = sequential_search(nums, target)
    else:
        return 'Пожалуйста, введите корректный номер (1 или 2)'

    if result is None:
        return f'Цель {target} не найдена в списке.'
    return result


def run_main():
    try:
        nums, target, guess_type = get_user_input()
        result = main(guess_type, nums, target)
        print(result)
    except ValueError:
        print("Ошибка: введено не число.")


class TestSearchFunctions(unittest.TestCase):
    """
    Тесты для функций бинарного и последовательного поиска.
    """

    def test_binary_search_found(self):
        """Тест: бинарный поиск находит элемент."""
        nums = [1, 2, 3, 4, 5]  # Уже отсортирован
        self.assertEqual(binary_search(nums, 3), [3, 1])

    def test_binary_search_not_found(self):
        """Тест: бинарный поиск не находит элемент."""
        nums = [1, 2, 3, 4, 5]  # Уже отсортирован
        self.assertIsNone(binary_search(nums, 6))

    def test_sequential_search_found(self):
        """Тест: последовательный поиск находит элемент."""
        nums = [5, 3, 1, 4, 2]  # Не отсортирован
        self.assertEqual(sequential_search(nums, 4), [4, 4])

    def test_sequential_search_not_found(self):
        """Тест: последовательный поиск не находит элемент."""
        nums = [5, 3, 1, 4, 2]  # Не отсортирован
        self.assertIsNone(sequential_search(nums, 6))

    def test_main_binary_search_with_unsorted_list(self):
        """Тест: main вызывает бинарный поиск с неотсортированным списком."""
        nums = [5, 3, 1, 4, 2]
        self.assertEqual(main(1, nums, 3), [3, 1])

    def test_main_sequential_search_with_unsorted_list(self):
        """Тест: main вызывает последовательный поиск с неотсортированным списком."""
        nums = [5, 3, 1, 4, 2]
        self.assertEqual(main(2, nums, 4), [4, 4])

    def test_main_invalid_guess_type(self):
        """Тест: main возвращает сообщение об ошибке при неверном типе поиска."""
        nums = [1, 2, 3]
        self.assertEqual(main(3, nums, 2), 'Пожалуйста, введите корректный номер (1 или 2)')


if __name__ == '__main__':
    unittest.main()
