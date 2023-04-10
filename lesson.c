#include <stdio.h>

int main()
{
  int arr[] = {1, 2, 3, 4, 5};
  int size = sizeof(arr) / sizeof(arr[0]);

  for (int i = size - 1; i >= 0; i--)
  {
    printf("%d\n", arr[i]);
  }

  return 0;
}