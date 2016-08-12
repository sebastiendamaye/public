#ifndef DEF_HANGMAN
#define DEF_HANGMAN
char getLetter();
void dispWord(char secret[], int foundLetters[]);
int isWinner(char secret[], int foundLetters[]);
void checkWord(char guessedLetter, char secret[], int foundLetters[], int *moves);
#endif
