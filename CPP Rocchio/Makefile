# C++11 support on CAEN machines
PATH := /usr/um/gcc-4.7.0/bin:$(PATH) 
LD_LIBRARY_PATH := /usr/um/gcc-4.7.0/lib64 
LD_RUN_PATH := /usr/um/gcc-4.7.0/lib64

all:
	g++ -O3 -std=c++11 -march=native ./Rocchio_Raw/src/Rocchio.cpp -o ./Rocchio_Raw/Rocchio
	g++ -O3 -std=c++11 -march=native ./Rocchio_Weighted/src/Rocchio.cpp -o ./Rocchio_Weighted/Rocchio
	
clean:
	rm -rf ./Rocchio_Raw/Rocchio
	rm -rf ./Rocchio_Weighted/Rocchio