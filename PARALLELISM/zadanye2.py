import asyncio
import numpy as np
import concurrent.futures

async def generate_matrix(size):
    """
    Генерирует случайную квадратную матрицу заданной размерности.

    Args:
        size (int): Размерность матрицы.

    Returns:
        np.array: Случайная квадратная матрица.
    """

    return np.random.rand(size, size)


async def multiply_matrices(matrix1, matrix2):
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

        # Ждем завершения выполнения задач
        results = [task.result() for task in tasks]

    # Формируем матрицу-произведение из результатов
    result_matrix = np.array(results).reshape(matrix1.shape)

    return result_matrix


async def main():
    # Задаем размерность матриц
    size = 1000

    # Создаем очередь для хранения сгенерированных матриц
    matrix_queue = asyncio.Queue()

    # Создаем задачу для генерации матриц
    generate_task = asyncio.create_task(generate_matrix(size))

    # Создаем задачу для перемножения матриц
    multiply_task = asyncio.create_task(multiply_matrices(*await matrix_queue.get()))

    # Запускаем цикл для получения и перемножения сгенерированных матриц
    while True:
        # Получаем сгенерированную матрицу из очереди
        matrix1 = await matrix_queue.get()

        # Генерируем вторую матрицу
        matrix2 = await generate_matrix(size)

        # Перемножаем матрицы
        multiply_task.set_result(await multiply_matrices(matrix1, matrix2))

        # Проверяем, была ли нажата клавиша для остановки процесса
        if await asyncio.to_thread(lambda: input("Нажмите Enter для остановки: ") == ""):
            break

    # Ожидаем завершения всех задач
    await asyncio.gather(generate_task, multiply_task)


if __name__ == "__main__":
    asyncio.run(main())