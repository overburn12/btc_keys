import time
import multiprocessing
import math

#---- modules ---------------
import btc_keys
#----------------------------


def find_vanity_worker(vanity_words, iterations_per_worker, queue):
    last_time = time.time()
    iteration = 0
    last_iteration_count = 0

    while iteration < iterations_per_worker:
        private_key, p2pkh_address = btc_keys.generate_key_pair()
        
        # Check if the address starts with any of the vanity words
        for vanity_word in vanity_words:
            if p2pkh_address.startswith('1' + vanity_word):
                queue.put((True, {
                    "iteration": iteration,
                    "vanity_word": vanity_word,
                    "private_key": private_key,
                    "p2pkh_address": p2pkh_address
                }))
                return
        
        iteration += 1
        
        if time.time() - last_time >= 1.0:  # send iteration totals every second
            last_time = time.time()
            this_iteration_count = iteration - last_iteration_count
            last_iteration_count = iteration
            queue.put((False, {
                "iteration": this_iteration_count
            }))
        
    this_iteration_count = iteration - last_iteration_count
    last_iteration_count = iteration
    queue.put((False, {
        "iteration": this_iteration_count,
        "stop": True
    }))


def find_vanity(vanity_words, num_processes=4, iterations_per_worker=100000):
    queue = multiprocessing.Queue()
    start_time = time.time()
    print_interval = 5.0
    total_iterations = 0
    last_time_check = start_time
    last_iterations = total_iterations
    
    # Start worker processes
    worker_processes = []
    for _ in range(num_processes):
        worker = multiprocessing.Process(target=find_vanity_worker, args=(vanity_words, iterations_per_worker, queue))
        worker.start()
        worker_processes.append(worker)
    print(f"loaded {num_processes} workers")

    while True:
        # Check the queue for new data
        while not queue.empty():
            found, data = queue.get()
            if found:
                end_time = time.time()
                elapsed_time = end_time - start_time
                hours = math.floor(elapsed_time / 3600)
                minutes = math.floor((elapsed_time % 3600) / 60)
                seconds = elapsed_time % 60

                print(f"Vanity address found after {total_iterations} iterations and {hours} hours, {minutes} minutes, and {seconds:.2f} seconds!")
                print(f"Vanity Word: {data['vanity_word']}")
                print("Private Key:", data['private_key'])
                print("P2PKH Address:", data['p2pkh_address'])
                for worker in worker_processes:
                    worker.terminate()
                return
            else:
                total_iterations += data['iteration']

        if time.time() - last_time_check >= print_interval:
            last_time_check = time.time()
            this_iterations = total_iterations - last_iterations
            last_iterations = total_iterations
            print(f"Iteration: {total_iterations}, Checks per second: {(this_iterations / print_interval):.2f}")

        # Check if all workers have finished
        if all(not worker.is_alive() for worker in worker_processes):
            print('all workers done...')
            break

    print('done')
    for worker in worker_processes:
        worker.join()


#--------------------------------------------------------------------------
# main
#--------------------------------------------------------------------------

if __name__ == "__main__":
    vanity_words = ['Bitcoin', 'Nick', 'Kane']
    find_vanity(vanity_words, num_processes=multiprocessing.cpu_count() - 10, iterations_per_worker=100000)

