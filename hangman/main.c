#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include "main.h"
#include "words.h"
#define MOVES 10

int main(int argc, char *argv[])
{
  /***
   * INIT
   */
  int moves = MOVES;
  char secret[100] = "";
  // pick random word
  pickRandomWord(secret);

  int i = 0;
  // Mem alloc for found letters array (based on size of secret)
  int *foundLetters = NULL;
  foundLetters = malloc(sizeof(int)*strlen(secret));
  if (foundLetters==NULL) exit(1);
  // Init found letters array with zero
  for (i=0; i<strlen(secret); i++) foundLetters[i] = 0;
  // Init guessed letter
  char guessedLetter = 0;

  /***
   * PROG
   */
  printf("Welcome to Hangman!\n");

  while(moves > 0 && isWinner(secret, foundLetters)==0) {
    printf("\n%d moves left\n", moves);
    printf("What is the secret word? ");
    dispWord(secret, foundLetters);
    printf("\nLetter? ");
    guessedLetter = getLetter();
    checkWord(guessedLetter, secret, foundLetters, &moves);
  }

  if (moves > 0) {
    printf("\n*** YOU WIN ***\nThe secret is: %s\n", secret);
  } else {
    printf("\n*** YOU LOSE ***\nThe secret was: %s\n", secret);
  }

  free(foundLetters);

  return 0;
}

char getLetter()
{
  char c = 0;
  // Save 1st key
  c = getchar();
  // Purge all other keys (incl. ENTER)
  while(getchar()!='\n');
  return toupper(c);
}

int isWinner(char secret[], int foundLetters[])
{
  int i = 0;

  for (i=0; i<strlen(secret); i++) {
    if(foundLetters[i] == 0) return 0;
  }
  return 1;
}

void dispWord(char secret[], int foundLetters[])
{
  int i = 0;

  for (i=0; i<strlen(secret); i++) {
    if(foundLetters[i] == 1) printf("%c", toupper(secret[i]));
    else printf("%c", '*');
  }
}

void checkWord(char guessedLetter, char secret[], int foundLetters[], int *moves)
{
  int i = 0;
  int flagDecrementmoves = 1;

  for (i=0; i<strlen(secret); i++) {
    if(guessedLetter == toupper(secret[i])) {
      // If character is good, we place the letters
      if (foundLetters[i] == 0) {
        foundLetters[i] = 1;
        flagDecrementmoves = 0;
      }
    }
  }
  if (flagDecrementmoves == 1) *moves -= 1;
}

