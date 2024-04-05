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

    # Определяем количество доступных ядер процессора
    num_workers = os.cpu_count()

    # Создаем пул процессов
    with concurrent.futures.ProcessPoolExecutor(num_workers) as executor:
        # Создаем список задач для выполнения в потоках
        tasks = []
        for i in range(matrix1.shape[0]):
            for j in range(matrix1.shape[1]):
                tasks.append(executor.submit(lambda x, y: x * y, matrix1[i, j], matrix2[i, j]))

        # Ждем завершения выполнения задач
        results = [task.result() for task in tasks]

    # Формируем матрицу-произведение из результатов
    result_matrix = np.array(results).reshape(matrix1.shape)

    return result_matrix


if __name__ == "__main__":
    # Считываем матрицы из файлов
    matrix1 = np.loadtxt("matrix1.txt", delimiter=",")
    matrix2 = np.loadtxt("matrix2.txt", delimiter=",")

    # Перемножаем матрицы
    result_matrix = multiply_matrix_elementwise(matrix1, matrix2)

    # Записываем матрицу-произведение в файл
    np.savetxt("result_matrix.txt", result_matrix, delimiter=",")