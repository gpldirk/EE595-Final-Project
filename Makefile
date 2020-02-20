main:main.o job.o task.o
	g++ -std=c++11 main.o job.o task.o -o main

task.o:task.cpp task.h
	g++ -std=c++11 -c task.cpp

job.o:job.cpp job.h
	g++ -std=c++11 -c job.cpp

main.o:main.cpp
	g++ -std=c++11 -c main.cpp
