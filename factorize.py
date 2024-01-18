import sys
import timeit
import time
from multiprocessing import Manager, Process, Pool

# def factorize(*number):
#     # YOUR CODE HERE
#     raise NotImplementedError() # Remove after implementation


# a, b, c, d  = factorize(128, 255, 99999, 10651060)

# assert a == [1, 2, 4, 8, 16, 32, 64, 128]
# assert b == [1, 3, 5, 15, 17, 51, 85, 255]
# assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
# assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

def factorize_worker(num):
    # return [i for i in range(1, num+1) if num%i == 0]
    return list(filter(lambda x: num % x == 0, range(1, num + 1)))

def factorize_worker_results(num, results):
    factors = factorize_worker(num)
    results.append((num, factors))

def factorize_single_synchronous_process(*numbers):
    numbers_dict = {str(number): [] for number in numbers}
    for num in numbers:
        factors = factorize_worker(num)
        numbers_dict[str(num)].extend(factors)
    return numbers_dict

def factorize_multi_processing(*numbers):
    manager = Manager()
    with manager:
        numbers_list = manager.list(numbers)
        results = manager.list()
        processes = []
        for _ in range(len(numbers_list)):
            num = numbers_list.pop()
            process = Process(target=factorize_worker_results, args=(num, results))
            process.start()
            processes.append(process)
        [process.join() for process in processes]
        # Extract results from the shared list and format them as a dictionary
        numbers_dict = {str(num): factors for num, factors in results}
        return numbers_dict
    

def factorize_parallel(*numbers):
    pool = Pool()
    with pool:
        results = pool.map(factorize_worker, numbers)
    numbers_dict = {str(num[-1]):num for num in results}
    return numbers_dict
        
if __name__=="__main__":
    numbers = tuple(int(arg) for arg in sys.argv[1:])
    print("check with module - time: ")
    start_time_func = time.time()
    result = factorize_single_synchronous_process(*numbers)
    print(result)
    end_time_func = time.time()
    print("execution time for factorize_single_synchronous_process: ", end_time_func - start_time_func)
    
    start_time_func = time.time()
    factorize_multi_processing(*numbers)
    end_time_func = time.time()
    print("execution time for factorize_multi_processing: ", end_time_func - start_time_func)
    
    start_time_func = time.time()
    factorize_parallel(*numbers)
    end_time_func = time.time()
    print("execution time for factorize_parallel: ", end_time_func - start_time_func)
    
    print("Check with module - timeit: ")

    # Define a callable function for timeit
    def timeit_factorize_single_synchronous_process():
        factorize_single_synchronous_process(*numbers)

    setup_code = "from __main__ import timeit_factorize_single_synchronous_process"
    stmt = "timeit_factorize_single_synchronous_process()"
    times = timeit.repeat(stmt=stmt, setup=setup_code, repeat=20, number=1)
    average = sum(times) / len(times)
    print(f"Execution time for factorize_single_synchronous_process: ", average)
    
    def timeit_factorize_multi_processing():
            factorize_multi_processing(*numbers)
            
    setup_code = "from __main__ import timeit_factorize_multi_processing"
    stmt = "timeit_factorize_multi_processing()"
    times = timeit.repeat(stmt=stmt, setup=setup_code, repeat=20, number=1)
    average = sum(times) / len(times)
    print(f"Execution time for factorize_multi_processing: ", average)
    
    def timeit_factorize_parallel():
            factorize_parallel(*numbers)

    setup_code = "from __main__ import timeit_factorize_parallel"
    stmt = "timeit_factorize_parallel()"
    times = timeit.repeat(stmt=stmt, setup=setup_code, repeat=20, number=1)
    average = sum(times) / len(times)
    print(f"Execution time for factorize_parallel: ", average)
