# from tqdm.contrib.concurrent import process_map  # or thread_map
# import time
# 
# def _foo(my_number):
#    square = my_number * my_number
#    time.sleep(1)
#    return square 
# 
# if __name__ == '__main__':
#    r = process_map(_foo, range(0, 30), max_workers=2)

from time import sleep
from tqdm import tqdm_notebook as tqdm
from multiprocessing import Pool, freeze_support

def progresser(n):
    # This line is the strange hack
    print(' ', end='', flush=True)

    text = "progresser #{}".format(n)
    for i in tqdm(range(5000), desc=text, position=n):
         sleep(0.001)
        
if __name__ == '__main__':
    freeze_support()
    L = list(range(10))
    print()
    Pool(2).map(progresser, L)