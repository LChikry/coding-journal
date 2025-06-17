/**
 * This program is meant to check if a set of given instructions (Right, Left,
 * Up, or Down as R, L, U, or D) will reach a given final position (x,y) after
 * a number of times executing the instructions.
 *
 * The method used is to estimate the maximum number of times needed
 * to execute the set of given instructions to reach the final position.
 * Then start executing the instructions by checking each time
 * an instruction executed if we reached the position or not.
 * If we reached the maximum number of executions, and we didn't reach it yet
 * The final position. This means that it is impossible to reach the given final
 * position with this set of given instructions.
 */

#include <stdbool.h>
#include <stdio.h>
#include <string.h>

// This function gets called to execute the whole algorithm using all other
// functions. INPUTS:
// - The final position in the x-axis and y-axis
// - The set of given instructions.
// OUTPUTS:
// - Boolean value. True if the position is possible to reach, and false value
// if not.
bool isPositionReached(long int x_final, long int y_final,
                       const char *instructions);

// Counts how many Rights, Lefts, Ups, and Downs that the set of given
// instructions contains.
// INPUTS:
// - The set of given instructions.
// - The number of instructions in one set.
// - The addresses to the variables that will hold how many R,L,U,D exist.
// There are no outputs since the result is passed to the reference variables.
void InstructionsCounter(const char *instructions, int max_instructions,
                         int *rights, int *lefts, int *ups, int *downs);

// Checks if the given set of instructions are oscillating in a given range that
// The final position is not in it.
// INPUTS:
// - The final position in one axis (either the final position on the x-axis or
// y-axis).
// - How many rights||ups (positive moves) depending on the axis you working on.
// - How many lefts||downs (negative move) depending on the axis you working on.
// OUTPUTS:
// - Boolean value, true means the instructions oscillating in a range that the
// final position in one axis doesn't exist, which means, we will not reach the
// final position. In contrast, False means either it is not oscillating or it
// is oscillating but the final position on one axis is in the range of
// oscillation.
bool isOscillationFarAway(long int axis, int max_positive_moves,
                          int max_negative_moves);

// It checks if the number is positive or negative.
// INPUTS:
// - An integer number.
// OUTPUTS:
// - Character 'p' if it's positive, and 'n' if it's negative.
char isPositive(long int axis);

// Estimates the maximum number of times needed to execute the set of given
// instructions to reach the final position in one axis (either final position
// on the x-axis or y-axis).
// INPUTS:
// - The final position in one axis (either x-axis or y-axis).
// - The sign of the final position in one axis.
// - How many rights||ups (positive moves) depending on the axis you working on.
// - How many lefts||downs (negative move) depending on the axis you working on.
// OUTPUTS:
// - the maximum number of times needed to execute the instructions in one axis
// (either on the x-axis or y-axis) to reach the final position on that axis.
int CalcMaxExecutions(long int axis, char axis_sign, int max_positive_moves,
                      int max_negative_moves);

// It returns the difference between two numbers if it is positive. If it is
// equal to zero, or it is negative, the function returns 1.
// INPUTS:
// - two numbers to calculate their difference
// OUTPUTS:
// - the positive difference or 1.
int PositiveDifference(int positive_moves, int negative_moves);

// It keeps track of the number of times we executed all the instructions in the
// set of given instructions. And it stops when we are reaching the maximum
// number of executions needed to reach the final position.
// INPUTS:
// - The set of given instructions.
// - The number of instructions in one set.
// - The maximum number of executions needed to reach the final position.
// - The final position in the x-axis and y-axis
// OUTPUTS:
// - Boolean value, true means we reached the final position. And false means
// the opposite.
bool RoadPlanner(const char *instructions, int max_instructions,
                 long int max_executions, long int x_final, long int y_final);

// It executes the set of given instructions one by one from the initial
// position with checking each time if we reached the final position yet or not.
// INPUTS:
// - The set of given instructions.
// - The number of instructions in one set.
// - The final position in the x-axis and y-axis
// - The initial position we started in the x-axis and y-axis
// OUTPUTS:
// - Boolean value, true means we reached the final position. And false means
// We didn't reach yet the final position this time.
bool PositionMover(const char *instructions, int max_instructions,
                   long int x_final, long int y_final, long int *x_initial,
                   long int *y_initial);

int main(void) {

  if (isPositionReached(2, 3, "URR")) {  // x_final, y_final
    printf("Possible\n");
  } else {
    printf("Impossible\n");
  }

  return 0;
}




// This function takes the final position and the set of instructions, then
// checks if the final position is the initial position first. Also, it checks
// if a special case of oscillation occurs or not. After that, it starts to
// calculate the number of instructions in each direction, which will be used to
// estimate the maximum number of steps needed to reach the final position
// to use it as a terminator for the loop. We go with long int since we
// don't know how far the final position is.
bool isPositionReached(long int x_final, long int y_final,
                       const char *instructions) {
  if (0 == x_final && 0 == y_final) {
    return true;
  }  // this if-statement is added to catch the (0,0) case scenario.

  int max_instructions = strlen(instructions);

  int rights = 0, lefts = 0, ups = 0, downs = 0;
  InstructionsCounter(
      instructions, max_instructions, &rights, &lefts, &ups,
      &downs);  // to count number of instructions in each direction

  // these two steps are only to enhance the efficiency  of the algorithm in
  // the cases when oscillation occurs. These two steps are totally optional.
  if (isOscillationFarAway(x_final, rights, lefts)) {
    return false;
  } else if (isOscillationFarAway(y_final, ups, downs)) {
    return false;
  }

  char x_final_sign = isPositive(x_final);  // to know the sign of x or y final;
  char y_final_sign = isPositive(y_final);  // this will be used later

  // calculating the maximum execution of the whole set of instructions needed
  // to reach the final position in one axis through a simple formula. Then we
  // sum the two results of each axis to have the real estimation of how many
  // steps needed to reach the final position in the two dimensions (axis).
  long int max_executions =
      CalcMaxExecutions(x_final, x_final_sign, rights, lefts);
  max_executions += CalcMaxExecutions(y_final, y_final_sign, ups, downs);

  // This function starts to move from the initial position toward the final
  // position (loop) and stops when it reaches the final position or maximum
  // number of executions needed to reach the final position.
  bool result = RoadPlanner(instructions, max_instructions, max_executions,
                            x_final, y_final);

  return result;  // true means, we reach the final position
}

// This function counts the number of steps that the set of instructions
// had in each direction (U, R, L, D) in order to use it to estimate the
// maximum steps needed to reach the final position. The function goes
// through the string character by character and matches the character
// with the corresponding switch case to count the number of steps.
void InstructionsCounter(const char *instructions, int max_instructions,
                         int *rights, int *lefts, int *ups, int *downs) {
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

      default:
        printf(
            "You entered a false instruction. Therefore, the below answer "
            "is "
            "wrong. Please enter a valid instructions R, L, U, or D\n");
    }
  }
}

// This function is totally optional to use, but when we use it, we enhance the
// efficiency of the algorithm.
// The function checks if the sum of steps in both positive and negative
// direction of one axis (either x-axis or y-axis) equal to zero. if yes, this
// mean that we oscillating in a range = [lefts value, rights value] or
// [downs value, ups value] in the axis. Therefore, we check if the final
// position in that axis is in the range or not. if not that's mean we will
// never reach the final position.
bool isOscillationFarAway(long int axis, int max_positive_moves,
                          int max_negative_moves) {
  if (0 == (max_positive_moves - max_negative_moves)) {
    if (axis >= 0) {  // checking if the final position will be in the positive
                      // side or negative side of oscillation range
      if (axis > max_positive_moves) {
        return true;
      }       // end of checking if the axis is not in the oscillation range
    } else {  // end of checking on the positive side
      if (-axis > max_negative_moves) {
        return true;
      }  // end of checking if the axis is not in the oscillation range
    }    // end of checking on the negative side
  }      // end of checking if there is an oscillation

  return false;
}

// I added this function to reduce lines and nested if-statements (readability)
char isPositive(long int axis) {
  if (axis >= 0) {
    return 'p';
  }

  return 'n';
}

// This function estimates the maximum number of steps needed to reach our final
// position in just one axis using a simple equation. And the sum of the two
// axis estimation is the final maximum number of executions the instruction
// needed to reach the final position (x, y).
int CalcMaxExecutions(long int axis, char axis_sign, int max_positive_moves,
                      int max_negative_moves) {
  // We calculate the absolute  difference between the positive moves and
  // negative moves since one may hold back the other. Hence, more steps are
  // needed to reach the goal. (the result of this function always >= 1, see its
  // definition).
  int positive_divider =
      PositiveDifference(max_positive_moves, max_negative_moves);

  long int result;

  // Axis represents the final position, which also represents how many steps
  // the final position is far away from the start point which is (0, 0).
  //
  // Positive divider is how many steps we do towards (or backward) the final
  // position when we execute all the instructions unless it = 0, we put 1.
  //
  // Therefore, if we need to calculate how many steps we need, we take how many
  // steps the target is far away (Axis) divided by how many steps we make each
  // time (Positive_divider; that's why we put 1 instead of 0) That is going to
  // give us how many times we need to execute all the instructions to get to
  // the target if it is reachable.
  //
  // However, since the division operation may result in a double_type answer
  // which indicates that we will reach the final position in one of the middle
  // or first instruction. We need to convert this decimal part to an integer
  // number to be clear to us because it's hard to determine which instruction
  // meant by the decimal part. Therefore, we convert the decimal part into
  // integer with the remainder operator and added it to the original result
  // that is saved without the decimal part.
  if (axis_sign == 'p') {
    result = axis / positive_divider;
    result += (axis % (positive_divider));
  } else {  // end of positive scenario
    result = -axis / positive_divider;
    result += (-axis % positive_divider);
  }  // end of negative scenario

  return result;
}

// The following function calculates the difference between two numbers.
// Then return the result with a positive sign even if it was negative, and
// return 1 if the result = 0.
// This difference represents how many steps we are making towards our final
// position when executing all the set of given instructions.
int PositiveDifference(int positive_moves, int negative_moves) {
  int result = positive_moves - negative_moves;

  if (result > 0) {
    return result;  // we return the value directly since it is already > 0.
  } else if (result < 0) {
    return -result;  // we change the sign of the result to be positive with
                     // keeping the same value.
  }

  return 1;  // we return 1 in place of 0 since we'll use it in the denominator.
}

// This function keeps track of how many times we executed all the instructions
// so we can stop when we'll reach the estimated number of how many times we
// need to execute all the instructions in order to get to the final position.
// Also, it checks if we reached the final position or not when executing the
// instruction one by one through another function.
bool RoadPlanner(const char *instructions, int max_instructions,
                 long int max_executions, long int x_final, long int y_final) {
  long int x_initial = 0, y_initial = 0;  // we start from (0,0)

  for (long int i = 0; i <= max_executions; i++) {
    if (PositionMover(instructions, max_instructions, x_final, y_final,
                      &x_initial, &y_initial)) {
      return true;
    }  // end of the checker that sees if we reach the target in the while
       // executed one of the instructions

  }  // end of the tracker that sees how many times we executed all the
     // instructions.

  return false;  // since we didn't reach the final position although we took
                 // all the necessary steps to reach the final position.
}

// this function moves as the instructions tell (U = y+1, and L = x-1, etc), and
// checks if we reached the final position after each one instruction was
// executed. We passed by reference since the function ends after one set of
// instruction, and we need to continue where we left off when we called the
// function previously.
// I created this function to enhance readability and maintain good code.
bool PositionMover(const char *instructions, int max_instructions,
                   long int x_final, long int y_final, long int *x_initial,
                   long int *y_initial) {
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

      default:
        printf(
            "You entered a false instruction. Therefore, the below answer "
            "is "
            "wrong. Please enter a valid instructions R, L, U, or D\n");
    }

    // We check each time one instruction is executed if reaches the final
    // position since we don't know when we going to reach the final position if
    // it is reachable.
    if ((*x_initial) == x_final && (*y_initial) == y_final) {
      return true;  // we reached the target
    }
  }

  return false;  // we didn't reach the target yet.
}