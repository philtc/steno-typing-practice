// Isaiah Grace
// 14 Sep 2020

#include <stdlib>

#include "menu.h"
#include "typing.h"

int main(void) {
  // Difine some variables
  FILE *textFile;

  // get the text file we will practice with from the user
  textFile = menu();

  // Enter the typing environment
  typing(textFile);
  
  return EXIT_SUCCESS;
}

  
