#include <string.h>

int DigitNameRecognition(char *digit_name) {
  if (strstr(digit_name, "one") != NULL) return 1;
  if (strstr(digit_name, "two") != NULL) return 2;
  if (strstr(digit_name, "six") != NULL) return 6;
  if (strstr(digit_name, "nine") != NULL) return 9;
  if (strstr(digit_name, "zero") != NULL) return 0;
  if (strstr(digit_name, "four") != NULL) return 4;
  if (strstr(digit_name, "five") != NULL) return 5;
  if (strstr(digit_name, "three") != NULL) return 3;
  if (strstr(digit_name, "seven") != NULL) return 7;
  if (strstr(digit_name, "eight") != NULL) return 8;
  return -1;
}

int ReverseDigitNameRecognition(char *digit_name) {
  if (strstr(digit_name, "eno") != NULL) return 1;
  if (strstr(digit_name, "owt") != NULL) return 2;
  if (strstr(digit_name, "xis") != NULL) return 6;
  if (strstr(digit_name, "enin") != NULL) return 9;
  if (strstr(digit_name, "orez") != NULL) return 0;
  if (strstr(digit_name, "ruof") != NULL) return 4;
  if (strstr(digit_name, "evif") != NULL) return 5;
  if (strstr(digit_name, "eerht") != NULL) return 3;
  if (strstr(digit_name, "neves") != NULL) return 7;
  if (strstr(digit_name, "thgie") != NULL) return 8;
  return -1;
}

void WriteTheNumber(int *first_digit, int *last_digit, int to_add) {
  *last_digit = to_add;

  if (*first_digit == -1) {
    *first_digit = to_add * 10;
  }
}