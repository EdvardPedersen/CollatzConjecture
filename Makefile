all: cpp c c-openmp

cpp: Makefile Collatz.cpp
	g++ -O2 -std=c++2b Collatz.cpp -o henrik

c: Makefile collatz.c
	gcc -O2 collatz.c -o edvard

c-openmp: Makefile collatz.c
	gcc -O2 -fopenmp collatz.c -o edvard2

clean:
	rm edvard2 edvard henrik
