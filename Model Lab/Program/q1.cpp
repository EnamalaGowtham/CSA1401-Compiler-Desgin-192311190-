#include <stdio.h>
#include <string.h>
#include <ctype.h>

int isKeyword(char word[])
{
    char keywords[][10] = {
        "int", "float", "char", "double",
        "if", "else", "for", "while",
        "return", "void"
    };

    int i;

    for (i = 0; i < 10; i++)
    {
        if (strcmp(word, keywords[i]) == 0)
            return 1;
    }

    return 0;
}

int main()
{
    char word[50];
    int keywords = 0, identifiers = 0;

    printf("Enter C program:\n");
    printf("Enter # to stop:\n\n");

    while (scanf("%s", word) == 1)
    {
        if (strcmp(word, "#") == 0)
            break;

        /* Remove common symbols */
        int len = strlen(word);

        while (len > 0 && !isalnum(word[len - 1]) &&
               word[len - 1] != '_')
        {
            word[len - 1] = '\0';
            len--;
        }

        if (isKeyword(word))
        {
            keywords++;
        }
        else if (isalpha(word[0]) || word[0] == '_')
        {
            identifiers++;
        }
    }

    printf("\nTotal Keywords = %d", keywords);
    printf("\nTotal Identifiers = %d\n", identifiers);

    return 0;
}
