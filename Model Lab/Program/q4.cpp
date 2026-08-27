#include <stdio.h>
#include <string.h>

int main()
{
    char temp[10][10];
    char expr[10][30];
    int n, i, j, found;

    printf("Enter number of statements: ");
    scanf("%d", &n);

    printf("Enter Three Address Code:\n");

    for (i = 0; i < n; i++)
    {
        scanf("%s = %[^\n]", temp[i], expr[i]);
        getchar();
    }

    printf("\nOptimized Three Address Code:\n");

    for (i = 0; i < n; i++)
    {
        found = -1;

        for (j = 0; j < i; j++)
        {
            if (strcmp(expr[i], expr[j]) == 0)
            {
                found = j;
                break;
            }
        }

        if (found != -1)
            printf("%s = %s\n", temp[i], temp[found]);
        else
            printf("%s = %s\n", temp[i], expr[i]);
    }

    return 0;
}
