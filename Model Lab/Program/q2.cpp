#include <stdio.h>
#include <string.h>
#include <ctype.h>

int isInteger(char str[])
{
    int i = 0;

    if (str[0] == '-' || str[0] == '+')
        i++;

    if (str[i] == '\0')
        return 0;

    while (str[i] != '\0')
    {
        if (!isdigit(str[i]))
            return 0;
        i++;
    }

    return 1;
}

int isFloat(char str[])
{
    int i = 0, dot = 0, digit = 0;

    if (str[0] == '-' || str[0] == '+')
        i++;

    while (str[i] != '\0')
    {
        if (str[i] == '.')
        {
            dot++;
        }
        else if (isdigit(str[i]))
        {
            digit = 1;
        }
        else
        {
            return 0;
        }

        i++;
    }

    return (dot == 1 && digit == 1);
}

int main()
{
    char word[50];
    int integers = 0, floats = 0;

    printf("Enter C program:\n");
    printf("Enter # to stop:\n\n");

    while (scanf("%s", word) == 1)
    {
        if (strcmp(word, "#") == 0)
            break;

        /* Remove ; , and other symbols */
        int len = strlen(word);

        while (len > 0 &&
               (word[len - 1] == ';' ||
                word[len - 1] == ',' ||
                word[len - 1] == ')'))
        {
            word[len - 1] = '\0';
            len--;
        }

        if (isFloat(word))
            floats++;
        else if (isInteger(word))
            integers++;
    }

    printf("\nInteger Constants = %d", integers);
    printf("\nFloating-Point Constants = %d\n", floats);

    return 0;
}
