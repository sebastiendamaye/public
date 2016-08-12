#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include "words.h"
#define MAXWORDLEN 100

int pickRandomWord(char *secret)
{
  FILE *f = NULL;
  char ch = 0;
  int nwords = 0;
  srand(time(NULL));
  int randnum = 0;
  int i = 0;

  // open words file
  f = fopen("words.txt", "r");
  if(f==NULL) {
    printf("Error opening file");
    return 1;
  }

  // count number of words in file
  while ((ch=getc(f)) != EOF) {
    if(ch=='\n') nwords++;
  }

  // pick random word
  randnum = (rand() % nwords) + 1;
  rewind(f);
  while (i!=randnum) {
    fgets(secret, MAXWORDLEN, f);
    i++;
  }
  
  // Remove \n at the end of the word
  secret[strlen(secret)-1] = '\0';

  /*
  //disp file info
  puts("===== DEBUG =====");
  printf("%d words\n", nwords);
  printf("%d\n", randnum);
  printf("%s\n", secret);
  printf("Len: %d\n", strlen(secret));
  puts("=================");
  */

  fclose(f);  
 
  return 0;
}
