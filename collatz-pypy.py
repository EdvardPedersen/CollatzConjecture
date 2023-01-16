from decimal import Decimal
import time
import functools
from multiprocessing import Process, Array

N = 1000000

# Baseline
def default_collatz(n):
    if n < 2:
        return 0
    if n % 2 == 0:
        return default_collatz(n//2) + 1
    return default_collatz(3*n+1) + 1

# Written by Henrik
class Collatz:
    def __init__(self):
        self.checked = {1: 0}

    def collatz(self, n):
        if n in self.checked:
            return self.checked[n]
        if n % 2 == 0:
            self.checked[n] = self.collatz(n // 2) + 1
            return self.checked[n]
        self.checked[n] = self.collatz((n*3)+1) + 1
        return self.checked[n]

# Written by Edvard
def iterative_collatz(n):
    iterations = 0
    while n != 1:
        iterations += 1
        if n % 2 == 0:
            n = n // 2
        else:
            n = (n*3)+1
    return iterations

class MemoizedIterative:
    def __init__(self):
        self.cache = {}

    def collatz(self, n):
        iterations = 0
        temp_cache = {n: 0}
        while n != 1:
            if n in self.cache:
                for num in temp_cache:
                    self.cache[num] = (iterations - temp_cache[num]) + self.cache[n]
                return self.cache[n] + iterations
            iterations += 1
            if n % 2 == 0:
                n = n // 2
            else:
                n = (n*3)+1
            temp_cache[n] = iterations
        for num in temp_cache:
            self.cache[num] = iterations - temp_cache[num]
        return iterations

# Written by Edvard
class ArrayCollatz:
    def __init__(self, cache_size=1000000):
        self.cache = []
        for i in range(cache_size):
            self.cache.append(0)
        self.cache_size = cache_size

    def collatz(self, n):
        if n >= self.cache_size:
            if n % 2 == 0:
                return self.collatz(n//2) + 1
            return self.collatz(3*n+1) + 1
        if self.cache[n] != 0:
            return self.cache[n]
        if n < 2:
            return 0
        if n % 2 == 0:
            self.cache[n] = self.collatz(n//2) + 1
            return self.cache[n]
        self.cache[n] =  self.collatz(3*n+1) + 1
        return self.cache[n]

# Written by Edvard
# @functools.cache
# def collatz(n):
#     if n < 2:
#         return 0
#     if n % 2 == 0:
#         return collatz(n//2) + 1
#     return collatz(3*n+1) + 1

# Written by ChatGPT from prompt "write python program for the collatz conjecture with memoization"
def gpt_collatz(n, memo={}):
    if n == 1:
        return 1
    elif n in memo:
        return memo[n]
    elif n % 2 == 0:
        memo[n] = 1 + gpt_collatz(n // 2, memo)
        return memo[n]
    else:
        memo[n] = 1 + gpt_collatz(3 * n + 1, memo)
        return memo[n]

# Written by ChatGPT with prompt "optimize the code"
def gpt_ocollatz(n):
    memo = {1: 1}
    def helper(n):
        if n in memo:
            return memo[n]
        elif n % 2 == 0:
            memo[n] = 1 + helper(n // 2)
            return memo[n]
        else:
            memo[n] = 1 + helper(3 * n + 1)
            return memo[n]
    return helper(n)

# Written by ChatGPT with prompt "that was slower"
def gpt_ocollatz2(n):
    memo = {1: 1}
    while n not in memo:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        memo[n] = memo.get(n, 1) + 1
    return memo[n]
# Further prompts do not fix the problem

# Multiprocessing helper
# def many_collatz(start, end, array):
#     for i in range(start, end):
#         array[i] = collatz(i)

def benchmark_algorithm(function, description):
    start = time.time()
    result = {}
    for n in range(1, N):
        result[n] = function(n)
    end = round((time.time()-start), 3)
    print(description, ": Calculated {:} values of collatz in {} seconds".format(N, end))

if __name__ == "__main__":
    benchmark_algorithm(default_collatz, "Default recursive")
    benchmark_algorithm(iterative_collatz, "Default iterative")
    c = MemoizedIterative()
    benchmark_algorithm(c.collatz, "Memoized iterative")
    c = Collatz()
    benchmark_algorithm(c.collatz, "Class-based memoization")
    c = ArrayCollatz()
    benchmark_algorithm(c.collatz, "Class-based cache")
    # benchmark_algorithm(collatz, "Functools-based memoization")
    benchmark_algorithm(gpt_collatz, "ChatGPT memoization")
    benchmark_algorithm(gpt_ocollatz, "\"Optimized\" ChatGPT memoization")
    benchmark_algorithm(gpt_ocollatz2, "Even more \"optimized\" ChatGPT memoization")


#     start = time.time()
#     result = Array('i', N+1, lock=False)
#     processes = []
#     for n in range(1, N, N//10):
#         processes.append(Process(target = many_collatz, args=(n, n+(N//10), result)))
#         processes[-1].start()
#     for p in processes:
#         p.join()
#     print("Multiprocessing-based: Calculated", "{:.1E}".format(Decimal(N)), "values of collatz in", round((time.time()-start), 3), "seconds.")
