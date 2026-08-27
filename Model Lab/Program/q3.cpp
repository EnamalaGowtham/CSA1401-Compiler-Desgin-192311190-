#include <stdio.h>
#include <string.h>

int main()
{
    char input[20];
    int i = 0;

    printf("Enter input string: ");
    scanf("%s", input);

    strcat(input, "$");

    printf("\nParsing Table:\n");
    printf("S -> aAB\n");
    printf("A -> b | epsilon\n");
    printf("B -> c\n");

    printf("\nParsing Steps:\n");

    /* S -> aAB */
    if (input[i] == 'a')
    {
        printf("S -> aAB\n");
        printf("Match a\n");
        i++;
    }
    else
    {
        printf("Rejected\n");
        return 0;
    }

    /* A -> b | epsilon */
    if (input[i] == 'b')
    {
        printf("A -> b\n");
        printf("Match b\n");
        i++;
    }
    else
    {
        printf("A -> epsilon\n");
    }

    /* B -> c */
    if (input[i] == 'c')
    {
        printf("B -> c\n");
        printf("Match c\n");
        i++;
    }
    else
    {
        printf("Rejected\n");
        return 0;
    }

    if (input[i] == '$')
        printf("\nInput Accepted\n");
    else
        printf("\nInput Rejected\n");

    return 0;
}
