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
@functools.cache
def collatz(n):
    if n < 2:
        return 0
    if n % 2 == 0:
        return collatz(n//2) + 1
    return collatz(3*n+1) + 1

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
def many_collatz(start, end, array):
    for i in range(start, end):
        array[i] = collatz(i)

if __name__ == "__main__":
    start = time.time()
    result = {}
    for n in range(1, N):
        result[n] = default_collatz(n)
    print("DEFAULT: Calculated", f"{Decimal(N):.1E}", "values of collatz in", round((time.time()-start), 3), "seconds.")

    c = Collatz()
    start = time.time()
    for n in range(1, N):
        c.collatz(n)
    print("HENKEBAZZ: Calculated", f"{Decimal(N):.1E}", "values of collatz in", round((time.time()-start), 3), "seconds.")

    start = time.time()
    result = {}
    for n in range(1, N):
        result[n] = collatz(n)
    print("EDVARD: Calculated", f"{Decimal(N):.1E}", "values of collatz in", round((time.time()-start), 3), "seconds.")

    start = time.time()
    result = {}
    for n in range(1, N):
        result[n] = gpt_collatz(n)
    print("ChatGPT: Calculated", f"{Decimal(N):.1E}", "values of collatz in", round((time.time()-start), 3), "seconds.")

    start = time.time()
    result = {}
    for n in range(1, N):
        result[n] = gpt_ocollatz(n)
    print("ChatGPT optimized: Calculated", f"{Decimal(N):.1E}", "values of collatz in", round((time.time()-start), 3), "seconds.")

    start = time.time()
    result = {}
    for n in range(1, N):
        result[n] = gpt_ocollatz2(n)
    print("ChatGPT optimized: Calculated", f"{Decimal(N):.1E}", "values of collatz in", round((time.time()-start), 3), "seconds.")

    start = time.time()
    result = Array('i', N+1, lock=False)
    processes = []
    for n in range(1, N, N//10):
        processes.append(Process(target = many_collatz, args=(n, n+(N//10), result)))
        processes[-1].start()
    for p in processes:
        p.join()
    print("MPMAN: Calculated", f"{Decimal(N):.1E}", "values of collatz in", round((time.time()-start), 3), "seconds.")
