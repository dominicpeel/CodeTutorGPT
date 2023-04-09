#include <stdio.h>

int main()
{
  int x = 5;
  int *ptr = &x;

  printf("x = %d\n", x);

  *ptr = 100;
  printf("x = %d\n", x);

  return 0;
}
