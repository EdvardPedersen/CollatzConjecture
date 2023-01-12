#include <iostream>
#include <string>
#include <unordered_map>
#include <chrono>

class Collatz
{
public:
    Collatz();
    ~Collatz();
    unsigned int collatz(unsigned int n);
    void printValues();
private:
    std::unordered_map<int, int> values;
};

Collatz::Collatz() {
	this->values.insert(std::pair<int, int>(1, 0));
}

Collatz::~Collatz() {
}

unsigned int Collatz::collatz(unsigned int n) {
	if (this->values.contains(n)) {
		return this->values[n];
	}
	if (n % 2 == 0) {
		this->values.insert(std::pair<int, int>(n, this->collatz(n / 2) + 1));
		return this->values[n];
	}
	this->values.insert(std::pair<int, int>(n, this->collatz(((n * 3) + 1) / 2) + 2));
	return this->values[n];
}

void Collatz::printValues() {
	for (const std::pair<int, int> p : this->values) {
		std::cout << "Key " << p.first << " Value " << p.second << std::endl;
	}
}

int main()
{
    long int N = 1000000;
    Collatz c;

    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 1; i <= N; i++) {
        c.collatz(i);
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

    //c.printValues();
    std::cout << "C++ Memoized: Calculated " << N << " values of collatz in " << (duration.count() / 1000.0) << " seconds " << std::endl;

    return 0;
}
