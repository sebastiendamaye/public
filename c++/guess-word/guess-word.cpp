#include <iostream>
#include <ctime>
#include <cstdlib>
#include <string>
using namespace std;

string scramble(string secret);

int main()
{
  string secret, scrambledSecret, guess;
  srand(time(0));

  cout << "PLAYER 1 => Give a word: ";
  cin >> secret;
  system("clear");
  scrambledSecret = scramble(secret);

  do {
    cout << "PLAYER 2: What is the secret: " << scrambledSecret << "? ";
    cin >> guess;
    if (guess != secret)
      cout << "Nope!" << endl;
    else
      cout << "\nBazinga!!!" << endl;
  } while (secret!=guess);

  return 0;
}

string scramble(string secret)
{
  string scrambledSecret;
  int p(0);

  while (secret.size()!=0) {
    p = rand() % secret.size();
    scrambledSecret += secret[p];
    secret.erase(p,1);
  }

  return scrambledSecret;
}
