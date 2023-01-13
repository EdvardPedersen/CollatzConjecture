#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <omp.h>

#define N 1000000
#define CACHE_SIZE N
#define NUM_THREADS 10



long int collatz(long int n) {
    if(n < 2) return 0;
    if(n % 2 == 0) return collatz(n / 2);
    return collatz(3*n+1);
}

long int collatz_cache(long int n, int *cache){
    if(n > CACHE_SIZE) {
        if(n % 2 == 0) {
            return collatz_cache(n / 2, cache) + 1;
        }
        return collatz_cache(3*n+1, cache) + 1;
    }
    if(cache[n]) return cache[n];
    if(n < 2) return 0;
    if(n % 2 == 0) {
        cache[n] = collatz_cache(n / 2, cache) + 1;
        return cache[n];
    }
    cache[n] = collatz_cache(3*n+1, cache) + 1;
    return cache[n];
}


int main() {
    long int *results = malloc(sizeof(long int) * N);

    printf("STARTING\n");

    clock_t start = clock();
    for(long int i = 0; i < N; i++) {
        results[i] = collatz(i);
    }

    clock_t diff = clock() - start;
    double ms = diff / (double)CLOCKS_PER_SEC;
    printf("C default: Calculated %d values of collatz in %f seconds.\n", N, ms);


    int *cache = calloc(CACHE_SIZE, sizeof(int));
    start = clock();
    for(long int i = 0; i < N; i++) {
        results[i] = collatz_cache(i, cache);
    }
    diff = clock() - start;
    ms = diff / (double)CLOCKS_PER_SEC;
    printf("C cache: Calculated %d values of collatz in %f seconds.\n", N, ms);

    cache = calloc(CACHE_SIZE, sizeof(int));
    double mp_start = omp_get_wtime();
    #pragma omp parallel for
    for(long int i = 0; i < N; i++) {
        results[i] = collatz_cache(i, cache);
    }
    /*for(int i = 0; i < NUM_THREADS; i++) {
        for(int x = i * (N / NUM_THREADS); x < (i+1) * (N/NUM_THREADS); x++) {
            results[i] = collatz_cache(x, cache);
        }
    }*/

    double mp_diff = omp_get_wtime() - mp_start;
    printf("C multithreaded cache: Calculated %d values of collatz in %f seconds.\n", N, mp_diff);
    
}
