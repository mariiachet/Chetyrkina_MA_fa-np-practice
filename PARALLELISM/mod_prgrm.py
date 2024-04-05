import concurrent.futures
import numpy as np

def multiply_matrix_elementwise(matrix1, matrix2):
    """
    Перемножает две матрицы поэлементно.

    Args:
        matrix1 (np.array): Первая матрица.
        matrix2 (np.array): Вторая матрица.

    Returns:
        np.array: Матрица-произведение.
    """

    # Проверяем, что матрицы имеют одинаковые размеры
    if matrix1.shape != matrix2.shape:
        raise ValueError("Матрицы должны иметь одинаковые размеры")

    # Создаем пул процессов
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Создаем список задач для выполнения в потоках
        tasks = []
        for i in range(matrix1.shape[0]):
            for j in range(matrix1.shape[1]):
                tasks.append(executor.submit(lambda x, y: x * y, matrix1[i, j], matrix2[i, j]))

        # Пишем результаты в промежуточный файл
        with open("result_matrix.txt", "w") as f:
            for task in tasks:
                f.write(str(task.result()) + "\n")

if __name__ == "__main__":
    # Считываем матрицы из файлов
    matrix1 = np.loadtxt("matrix1.txt", delimiter=",")
    matrix2 = np.loadtxt("matrix2.txt", delimiter=",")

    # Перемножаем матрицы
    multiply_matrix_elementwise(matrix1, matrix2)