import timeit
from collections import deque
from typing import Callable, Dict, Any, List, Tuple
import matplotlib.pyplot as plt


# ===== РЕКУРСИВНАЯ РЕАЛИЗАЦИЯ =====

def build_tree_recursive(
    height: int,
    root: int = 14,
    left_branch: Callable[[int], int] = lambda r: 2 - (r - 1),
    right_branch: Callable[[int], int] = lambda r: r * 2
) -> Dict[str, Any]:
    """Строит бинарное дерево рекурсивно"""
    if height < 0:
        return {}
    if height == 0:
        return {str(root): []}
    
    left_value = left_branch(root)
    right_value = right_branch(root)
    
    left_tree = build_tree_recursive(height - 1, left_value, left_branch, right_branch)
    right_tree = build_tree_recursive(height - 1, right_value, left_branch, right_branch)
    
    children = []
    if left_tree:
        children.append(left_tree)
    if right_tree:
        children.append(right_tree)
    
    return {str(root): children}


# ===== НЕРЕКУРСИВНАЯ РЕАЛИЗАЦИЯ =====

def build_tree_iterative(
    height: int,
    root: int = 14,
    left_branch: Callable[[int], int] = lambda r: 2 - (r - 1),
    right_branch: Callable[[int], int] = lambda r: r * 2
) -> Dict[str, Any]:
    """Строит бинарное дерево нерекурсивно (через очередь)"""
    if height < 0:
        return {}
    
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


# ===== ИЗМЕРЕНИЕ ВРЕМЕНИ =====

def measure_time(func: Callable, height: int, root: int = 14) -> float:
    """Измеряет время выполнения функции"""
    left = lambda r: 2 - (r - 1)
    right = lambda r: r * 2
    
    timer = timeit.Timer(
        lambda: func(height, root, left, right)
    )
    return timer.timeit(number=1)


def run_benchmark(max_height: int = 15) -> Tuple[List[int], List[float], List[float]]:
    """Запускает бенчмарк для обеих реализаций"""
    heights = []
    recursive_times = []
    iterative_times = []
    
    print("Измерение времени работы...\n")
    print(f"{'Height':<8} {'Recursive (s)':<20} {'Iterative (s)':<20}")
    print("-" * 50)
    
    for h in range(max_height + 1):
        try:
            # Рекурсивная версия
            rec_time = measure_time(build_tree_recursive, h)
            
            # Нерекурсивная версия
            iter_time = measure_time(build_tree_iterative, h)
            
            heights.append(h)
            recursive_times.append(rec_time)
            iterative_times.append(iter_time)
            
            print(f"{h:<8} {rec_time:<20.6f} {iter_time:<20.6f}")
            
        except RecursionError:
            print(f"{h:<8} RecursionError      {iter_time:<20.6f}")
            heights.append(h)
            recursive_times.append(None)
            iterative_times.append(iter_time)
            break
    
    print("-" * 50)
    return heights, recursive_times, iterative_times


# ===== ПОСТРОЕНИЕ ГРАФИКА =====

def plot_comparison(heights: List[int], recursive_times: List[float], iterative_times: List[float]):
    """Строит график сравнения"""
    # Фильтруем None значения
    valid_indices = [i for i in range(len(heights)) if recursive_times[i] is not None]
    
    heights_valid = [heights[i] for i in valid_indices]
    recursive_valid = [recursive_times[i] for i in valid_indices]
    iterative_valid = [iterative_times[i] for i in valid_indices]
    
    plt.figure(figsize=(12, 6))
    
    plt.plot(heights_valid, recursive_valid, 'o-', label='Recursive', linewidth=2, markersize=6)
    plt.plot(iterative_valid, iterative_times, 's-', label='Iterative', linewidth=2, markersize=6)
    
    plt.xlabel('Tree Height', fontsize=12)
    plt.ylabel('Time (seconds)', fontsize=12)
    plt.title('Binary Tree Construction: Recursive vs Iterative', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.savefig('tree_comparison.png', dpi=150)
    print("\n✓ График сохранён в tree_comparison.png")
    plt.show()


# ===== ВЫВОДЫ =====

def print_conclusions(heights: List[int], recursive_times: List[float], iterative_times: List[float]):
    """Выводит выводы сравнения"""
    print("\n" + "=" * 60)
    print("ВЫВОДЫ")
    print("=" * 60)
    
    # Найти точку, где рекурсия сломалась
    recursion_limit = None
    for i in range(len(recursive_times)):
        if recursive_times[i] is None:
            recursion_limit = heights[i]
            break
    
    if recursion_limit:
        print(f"\n1. Рекурсия сломалась на высоте {recursion_limit}")
        print(f"   (превышен лимит рекурсии, обычно ~1000)")
    else:
        print(f"\n1. Обе реализации работают до высоты {max(heights)}")
    
    # Сравнение скорости
    valid_indices = [i for i in range(len(recursive_times)) if recursive_times[i] is not None]
    if valid_indices:
        last_idx = valid_indices[-1]
        rec_time = recursive_times[last_idx]
        iter_time = iterative_times[last_idx]
        
        ratio = rec_time / iter_time if iter_time > 0 else 0
        print(f"\n2. На последней измеренной высоте:")
        print(f"   Рекурсивная: {rec_time:.6f} сек")
        print(f"   Нерекурсивная: {iter_time:.6f} сек")
        print(f"   Отношение: {ratio:.2f}x")


# ===== ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ =====

def run_examples():
    """Запускает примеры использования"""
    print("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ\n")
    print("=" * 60)
    
    print("\n1. Рекурсивная версия (height=2):")
    tree = build_tree_recursive(height=2)
    print(tree)
    
    print("\n2. Нерекурсивная версия (height=2):")
    tree = build_tree_iterative(height=2)
    print(tree)
    
    print("\n3. Проверка что результаты одинаковые:")
    rec = build_tree_recursive(height=3)
    iter = build_tree_iterative(height=3)
    print(f"   Рекурсивная == Нерекурсивная: {rec == iter}")
    
    print("\n4. Пользовательские параметры:")
    tree = build_tree_recursive(
        height=2,
        root=10,
        left_branch=lambda r: r + 1,
        right_branch=lambda r: r * 2
    )
    print(f"   root=10, left=r+1, right=r*2:")
    print(f"   {tree}")


# ===== ГЛАВНАЯ ФУНКЦИЯ =====

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'bench':
            max_h = int(sys.argv[2]) if len(sys.argv) > 2 else 15
            heights, rec_times, iter_times = run_benchmark(max_h)
            plot_comparison(heights, rec_times, iter_times)
            print_conclusions(heights, rec_times, iter_times)
        elif sys.argv[1] == 'examples':
            run_examples()
        else: pass
    else:
        print("Использование:")
        print("  python main.py bench [max_height]  - запустить бенчмарк")
        print("  python main.py examples             - показать примеры")
        print("\nПример:")
        print("  python main.py bench 15")
