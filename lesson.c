#include <stdio.h>

int main()
{
  int *arr = malloc(10 * sizeof(int));
  for (int i = 0; i < 10; i++)
  {
    arr[i] = i;
  }
  for (int i = 0; i < 10; i++)
  {
    printf("%d\n", arr[i]);
  }
  free(arr);

  return 0;
}