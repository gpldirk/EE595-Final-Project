CC = g++ -std=c++11
CFLAG = -Wall -g
OBJ = main.o job.o task.o base.o

main: $(OBJ)
	$(CC) $(CFLAG) $(OBJ) -o $@
	#$(CC) $(CFLAG) $(OBJ) -o -g -fsanitize=address $@

.cpp.o:
	$(CC) $(CFLAG) -c $<

clean:
	-rm -f *.o


