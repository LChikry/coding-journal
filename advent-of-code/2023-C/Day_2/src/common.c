#include <string.h>
#include "../include/common.h"

 int WhatColor(char *string_line) {
  if (strstr(string_line, "green") != NULL) return GREEN;
  if (strstr(string_line, "red") != NULL) return RED;
  if (strstr(string_line, "blue") != NULL) return BLUE;

  return -1;
}