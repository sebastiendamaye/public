hangman: main.o words.o
	gcc -o hangman main.o words.o

main.o: main.c words.h
	gcc -c main.c

words.o: words.c words.h
	gcc -c words.c

clean:
	rm -f hangman main.o words.o
