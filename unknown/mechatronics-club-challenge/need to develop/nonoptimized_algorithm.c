#include <stdbool.h>
#include <stdio.h>
#include <string.h>

typedef struct {
  long int x_final;
  long int y_final;
  char instructions[20];
  char possibility[20];
} directions;

bool isPositionReached(int x_final, int y_final, char *instructions);
void InstructionsCounter(char *instructions, int max_instructions, int *rights,
                         int *lefts, int *ups, int *downs);
char isPositive(int number);
int CalcMaxExecutions(int axis, char axis_sign, int positive_axis,
                      int negative_axis);
int PositiveDifference(int number1, int number2);
bool RoadPlanner(char *instructions, int max_instructions, int max_executions,
                 int x_final, int y_final);
bool PositionMover(char *instructions, int max_instructions, int x_final,
                   int y_final, int *x_initial, int *y_initial);

int main(void) {
  // if (isPositionReached(1, 2, "RRLDUUDL"))  // the first argument is the x_final
  //   printf("Possible\n");
  // else
  //   printf("Impossible\n");

  FILE *test_cases = fopen("casestudy.txt", "r");
  int cnt = 0;
  char temp[20];

  if (NULL == test_cases) {
    printf("File was not found!\n");
    return 1;
  } else {
    while (!feof(test_cases)) {
      fgets(temp, 20, test_cases);
      cnt++;
    }  // the cursor is in EOF
  }

  fseek(test_cases, 0, 0);

  int number_of_tests = 1 + (cnt - 4) / 5;
  char backslash;

  directions x[number_of_tests];

  for (int i = 0; i < number_of_tests; i++) {
    fscanf(test_cases, "%ld", &x[i].x_final);

    fscanf(test_cases, "%ld", &x[i].y_final);

    fscanf(test_cases, "%s", x[i].instructions);

    fscanf(test_cases, "%s", x[i].possibility);
  }

  fclose(test_cases);

  for (int i = 0; i < number_of_tests; i++) {
    bool result =
        isPositionReached(x[i].x_final, x[i].y_final, x[i].instructions);
    if (result) {
      if (strcmp("Possible", x[i].possibility)) {
        printf("%ld\n", x[i].x_final);
        printf("%ld\n", x[i].y_final);
        printf("%s\n", x[i].instructions);
        printf("%s\n", x[i].possibility);
        printf("\n");
      }
    } else {
      if (strcmp("Impossible", x[i].possibility)) {
        printf("%ld\n", x[i].x_final);
        printf("%ld\n", x[i].y_final);
        printf("%s\n", x[i].instructions);
        printf("%s\n", x[i].possibility);
        printf("\n");
      }
    }
  }

  return 0;
}

bool isPositionReached(int x_final, int y_final, char *instructions) {
  int max_instructions = strlen(instructions);

  int rights = 0, lefts = 0, ups = 0, downs = 0;
  InstructionsCounter(instructions, max_instructions, &rights, &lefts, &ups,
                      &downs);

  char x_final_sign = isPositive(x_final);
  char y_final_sign = isPositive(y_final);

  int max_executions = CalcMaxExecutions(x_final, x_final_sign, rights, lefts);
  max_executions += CalcMaxExecutions(y_final, y_final_sign, ups, downs);

  bool result = RoadPlanner(instructions, max_instructions, max_executions,
                            x_final, y_final);

  return result;
}

void InstructionsCounter(char *instructions, int max_instructions, int *rights,
                         int *lefts, int *ups, int *downs) {
  for (int i = 0; i < max_instructions; i++) {
    switch (instructions[i]) {
      case 'U':
        (*ups)++;
        break;

      case 'D':
        (*downs)++;
        break;

      case 'R':
        (*rights)++;
        break;

      case 'L':
        (*lefts)++;
        break;
    }
  }
}

char isPositive(int number) {
  if (number >= 0) {
    return 'p';
  }

  return 'n';
}

int CalcMaxExecutions(int axis, char axis_sign, int positive_axis,
                      int negative_axis) {
  int positive_divider = PositiveDifference(positive_axis, negative_axis);
  int negative_divider = PositiveDifference(negative_axis, positive_axis);

  int result;

  if (axis_sign == 'p') {
    result = (axis / (positive_divider));
    printf("the result before remainder is: %d\n", result);
    result += (axis % (positive_divider));
    printf("the result after remainder is: %d\n", result);
  } else {  // end of positive scenario
    result = (-axis / (negative_divider));
    printf("the result before remainder is: %d\n", result);
    result += (-axis % (negative_divider));
    printf("the result after remainder is: %d\n", result);
  }  // end of negative scenario

  return result;
}

// The following function evaluate the difference between two numbers.
// Then return the value if it's positive, and return 0 if it's <= 0.
int PositiveDifference(int number1, int number2) {
  int result = number1 - number2;

  if (result > 0) {
    return result;
  }

  return 1;
}

bool RoadPlanner(char *instructions, int max_instructions, int max_executions,
                 int x_final, int y_final) {
  int x_initial = 0, y_initial = 0;

  for (int i = 0; i <= max_executions; i++) {
    if (x_initial == x_final && y_initial == y_final) {
      return true;
    }

    if (PositionMover(instructions, max_instructions, x_final, y_final,
                      &x_initial, &y_initial)) {
      return true;
    }
  }

  return false;
}

bool PositionMover(char *instructions, int max_instructions, int x_final,
                   int y_final, int *x_initial, int *y_initial) {
  for (int i = 0; i < max_instructions; i++) {
    switch (instructions[i]) {
      case 'U':
        (*y_initial)++;
        break;

      case 'D':
        (*y_initial)--;
        break;

      case 'R':
        (*x_initial)++;
        break;

      case 'L':
        (*x_initial)--;
        break;
    }

    if ((*x_initial) == x_final && (*y_initial) == y_final) {
      return true;
    }
  }

  return false;
}
