import threading
from queue import Queue

def run_algorithm(algorithm, board, start, end, results_queue):
    try:
        result = algorithm.find_path(board, start, end)
        results_queue.put((algorithm.name, result))
    except Exception as e:
        print(f"Error in {algorithm.name}: {e}")
        results_queue.put((algorithm.name, None))

def run_algorithms_in_parallel(algorithms, board, start, end):
    results = {}
    threads = []
    results_queue = Queue()
    
    for name, algo in algorithms.items():
        thread = threading.Thread(
            target=run_algorithm,
            args=(algo, board, start, end, results_queue)
        )
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    while not results_queue.empty():
        name, result = results_queue.get()
        results[name] = result
    
    return results