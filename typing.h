#ifndef TYPING_H
#define TYPING_H

#include <stdlib.h>
#include <stdio.h>

void typing(FILE *textFile);

// loads a chunk of tex from the file, starting at the index, into a buffer
char *loadChunk(FILE *textFile, int index);

// print
void printActiveLine(char* chunk, int chunkIndex);
void printNextLine(char* chunk, int chunkIndex);


#endif
