all: cpp c-openmp

cpp: Makefile Collatz.cpp
	g++ -O2 -std=c++2b Collatz.cpp -o henrik

c-openmp: Makefile collatz.c
	gcc -O2 -fopenmp collatz.c -lgomp -o edvard

clean:
	rm edvard henrik
