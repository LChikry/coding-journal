typedef struct {
  long int x_final;
  long int y_final;
  char instructions[20];
  char possibility[20];
} directions;

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






#include <stdio.h>
#include <string.h>

void fill_the_x_y_goal(int*, int*);  // this function to fill the variables
int if_reach_xy_goal(
    char*, int, int, int*,
    int*);  // this funciton to operate over the path and check.
int check(int*, int*, int, int, int, int, int, int,
          char*);  // this function is to check if if will reach it at the end
                   // of the path

int OneLastTime(char* path, int goal_x, int goal_y, int* x, int* y);

int main() {
  int x = 0, y = 0, check_x_y;

  check_x_y = if_reach_xy_goal("LRRLUDD", -1, 100, &x, &y);

  if (check_x_y == 1) {
    printf("Possible\n");
  } else if (check_x_y == 0) {
    printf("Impossible\n");
  }
  return 0;
}

void fill_the_x_y_goal(int* x, int* y) {
  printf("enter your x goal: ");
  scanf("%d", x);
  printf("enter your y goal: ");
  scanf("%d", y);
  getchar();
}

int if_reach_xy_goal(char* path, int goal_x, int goal_y, int* x, int* y) {
  int count_R = 0, count_L = 0, count_U = 0,
      count_D = 0;                   // I started counting the L R U D
                                     // printf("hereherehere\n");
  if (goal_x == 0 && goal_y == 0) {  // I checked if the x and y final are equal
                                     // to 0 in this case it will alway be true
    return 1;
  }

  int steps = strlen(path);
  for (int i = 0; i < steps; i++) {
    switch (path[i]) {
      case 'R':
        (*x) = *x + 1;
        count_R++;
        if ((*x) == goal_x && (*y) == goal_y) {
          return 1;
        }
        break;
      case 'L':
        (*x) = *x - 1;
        count_L++;
        if ((*x) == goal_x && (*y) == goal_y) {
          return 1;
        }
        break;
      case 'U':
        (*y) = *y + 1;
        count_U++;
        if ((*x) == goal_x && (*y) == goal_y) {
          return 1;
        }
        break;
      case 'D':
        (*y) = *y - 1;
        count_D++;
        if ((*x) == goal_x && (*y) == goal_y) {
          return 1;
        }
        break;
      default:
        printf("Invalid value in the path, please refill your path");
        return -1;
    }
  }

  if (check(x, y, goal_x, goal_y, count_R, count_L, count_U, count_D, path)) {
    return 1;
  } else {
    return 0;
  }
}

int check(int* x, int* y, int goal_x, int goal_y, int count_R, int count_L,
          int count_U, int count_D, char* path) {
  int i = 0, tmp;

  if (count_R == count_L) {  // if x sum is equal to 0 in that case y_final will
                             // be the multiple of y
    if (goal_x == 0 && (*y) % goal_y == 0) {  //!
      return 1;
    }
  }
  if (count_U == count_D) {  // if y sum is equal to 0 in that ce x_final will
                             // be the multiple of x
    if (goal_y == 0 && (*x) % goal_x == 0) {  //!
      return 1;
    }
  } else if ((float)*x / (*y) == (float)goal_x / goal_y &&
             (*x) - (*y) ==
                 goal_x - goal_y) {  // if non of the conditions is true we will
                                     // check if the factors are equal
    return 1;
  }
  if (0 == i) {
    tmp = *x;
    *x = goal_x / (*x) * (*x);
    *y = *x - (tmp - *y);

    return (OneLastTime(path, goal_x, goal_y, x, y));
  }

  return 0;
}

int OneLastTime(char* path, int goal_x, int goal_y, int* x, int* y) {
  int steps = strlen(path);

  for (int i = 0; i < steps; i++) {
    switch (path[i]) {
      case 'R':
        (*x) = *x + 1;
        if ((*x) == goal_x && (*y) == goal_y) {
          return 1;
        }
        break;
      case 'L':
        (*x) = *x - 1;
        if ((*x) == goal_x && (*y) == goal_y) {
          return 1;
        }
        break;
      case 'U':
        (*y) = *y + 1;
        if ((*x) == goal_x && (*y) == goal_y) {
          return 1;
        }
        break;
      case 'D':
        (*y) = *y - 1;
        if ((*x) == goal_x && (*y) == goal_y) {
          return 1;
        }
        break;
      default:
        printf("Invalid value in the path, please refill your path");
        return -1;
    }
  }

  return 0;
}