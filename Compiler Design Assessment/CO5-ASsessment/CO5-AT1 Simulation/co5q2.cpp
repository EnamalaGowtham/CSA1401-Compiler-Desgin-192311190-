#include <stdio.h>

int main()
{
    printf("INTERMEDIATE CODE AND TARGET CODE GENERATION\n");
    printf("==============================================\n\n");

    /* ------------------------------------------------
       PART A: THREE ADDRESS CODE
       Expression:
       x = (a+b)*(c-d) + ((e/f)*(a+b))
       ------------------------------------------------ */

    printf("(a) THREE ADDRESS CODE (TAC)\n");
    printf("----------------------------\n");

    printf("1.  t1 = a + b\n");
    printf("2.  t2 = c - d\n");
    printf("3.  t3 = t1 * t2\n");
    printf("4.  t4 = e / f\n");
    printf("5.  t5 = a + b\n");
    printf("6.  t6 = t4 * t5\n");
    printf("7.  t7 = t3 + t6\n");
    printf("8.  x = t7\n");

    /* ------------------------------------------------
       SUB-EXPRESSIONS
       ------------------------------------------------ */

    printf("\nSUB-EXPRESSIONS\n");
    printf("---------------\n");

    printf("1. (a + b)\n");
    printf("2. (c - d)\n");
    printf("3. (a + b) * (c - d)\n");
    printf("4. (e / f)\n");
    printf("5. (a + b)\n");
    printf("6. (e / f) * (a + b)\n");
    printf("7. Final addition\n");

    /* ------------------------------------------------
       OPERATOR PRECEDENCE
       ------------------------------------------------ */

    printf("\nORDER OF EVALUATION\n");
    printf("-------------------\n");

    printf("1. Parentheses are evaluated first.\n");
    printf("2. Addition and subtraction inside parentheses.\n");
    printf("3. Multiplication and division.\n");
    printf("4. Final addition.\n");
    printf("5. Result is assigned to x.\n");

    /* ------------------------------------------------
       PART B: TARGET CODE
       ------------------------------------------------ */

    printf("\n(b) TARGET CODE GENERATION\n");
    printf("--------------------------\n");

    printf("\nCalculate (a + b):\n");
    printf("MOV R1, a\n");
    printf("ADD R1, b\n");
    printf("R1 = a + b\n");

    printf("\nCalculate (c - d):\n");
    printf("MOV R2, c\n");
    printf("SUB R2, d\n");
    printf("R2 = c - d\n");

    printf("\nCalculate (a+b)*(c-d):\n");
    printf("MUL R1, R2\n");
    printf("R1 = (a+b)*(c-d)\n");

    printf("\nCalculate (e / f):\n");
    printf("MOV R2, e\n");
    printf("DIV R2, f\n");
    printf("R2 = e/f\n");

    printf("\nCalculate second (a + b):\n");
    printf("MOV R3, a\n");
    printf("ADD R3, b\n");
    printf("R3 = a+b\n");

    printf("\nCalculate (e/f)*(a+b):\n");
    printf("MUL R2, R3\n");
    printf("R2 = (e/f)*(a+b)\n");

    printf("\nCalculate final result:\n");
    printf("ADD R1, R2\n");
    printf("R1 = (a+b)*(c-d) + (e/f)*(a+b)\n");

    printf("\nStore result:\n");
    printf("MOV x, R1\n");

    /* ------------------------------------------------
       REGISTER USAGE
       ------------------------------------------------ */

    printf("\nREGISTER USAGE\n");
    printf("--------------\n");

    printf("R1 -> First product and final result\n");
    printf("R2 -> Second product\n");
    printf("R3 -> Second (a+b) intermediate result\n");

    /* ------------------------------------------------
       COMPLETE TARGET CODE
       ------------------------------------------------ */

    printf("\nCOMPLETE TARGET CODE\n");
    printf("--------------------\n");

    printf("MOV R1, a\n");
    printf("ADD R1, b\n");
    printf("MOV R2, c\n");
    printf("SUB R2, d\n");
    printf("MUL R1, R2\n");
    printf("MOV R2, e\n");
    printf("DIV R2, f\n");
    printf("MOV R3, a\n");
    printf("ADD R3, b\n");
    printf("MUL R2, R3\n");
    printf("ADD R1, R2\n");
    printf("MOV x, R1\n");

    printf("\nSimulation completed successfully.\n");

    return 0;
}
