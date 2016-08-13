#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
/*
Description
    Show current time (HH:MM:SS) in ASCII art. Press Ctrl+C to stop

    Example:

     88888    88888       88   88  8888888       88888   8888888
    88   88  88   88      88   88  88           88   88  88
         88      88       88   88  88                88  88
       88       888   88  8888888  888888   88     88    888888
      88         88            88       88        88          88
     88      88   88  88       88       88  88   88           88
    8888888   88888            88  888888       8888888  888888

Author:
    Sébastien Damaye

Rev:
    2016-08-13 12:00
*/

int main(int argc, char *argv[])
{
  // Init
  int row=0, i=0;
  int hms[] = {0, 0, 11, 0, 0, 11, 0, 0};
  const char *digits[12][7] = {
    {" 88888 ", "88   88", "88   88", "88   88", "88   88", "88   88", " 88888 "},
    {"     88", "    888", "     88", "     88", "     88", "     88", "     88"},
    {" 88888 ", "88   88", "     88", "   88  ", "  88   ", " 88    ", "8888888"},
    {" 88888 ", "88   88", "    88 ", "   888 ", "    88 ", "88   88", " 88888 "},
    {"88   88", "88   88", "88   88", "8888888", "     88", "     88", "     88"},
    {"8888888", "88     ", "88     ", "888888 ", "     88", "     88", "888888 "},
    {" 888888", "88     ", "88     ", "888888 ", "88   88", "88   88", " 88888 "},
    {"8888888", "     88", "    88 ", "  88   ", " 88    ", "88     ", "88     "},
    {" 88888 ", "88   88", "88   88", " 88888 ", "88   88", "88   88", " 88888 "},
    {" 88888 ", "88   88", "88   88", " 888888", "     88", "     88", "888888 "},
    {" 88888 ", "88   88", "88   88", "88   88", "88   88", "88   88", " 88888 "},
    {"  ", "  ", "88", "  ", "  ", "88", "  "}
  };
  time_t epoch_time;
  struct tm *tm_p;

  while(1) {
      system("clear");

      // Get current time
      epoch_time = time( NULL );
      tm_p = localtime( &epoch_time );

      // Hours
      hms[0] = tm_p->tm_hour/10;
      hms[1] = tm_p->tm_hour%10;

      // Minutes
      hms[3] = tm_p->tm_min/10;
      hms[4] = tm_p->tm_min%10;

      // Seconds
      hms[6] = tm_p->tm_sec/10;
      hms[7] = tm_p->tm_sec%10;

      // Display time in ASCII art
      for (row=0; row<7; row++) {
        for (i=0; i<8; i++) {
          printf( digits[hms[i]][row]);
          printf("  ");
        }
        printf("\n");
      }
      puts("\n(Press Ctrl+C to stop)");
    sleep(1);
  }

  return 0;
}
