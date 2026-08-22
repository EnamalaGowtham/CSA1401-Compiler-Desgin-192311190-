#include <stdio.h>

int main()
{
    printf("OPTIMAL CODE GENERATION SIMULATION\n");
    printf("==================================\n\n");

    printf("Given Expression:\n");
    printf("(a + b) - (c - (d + e))\n");

    /* ==========================================
       PART (a): TWO REGISTER CODE GENERATION
       ========================================== */

    printf("\n\n(a) OPTIMAL CODE USING TWO REGISTERS\n");
    printf("-------------------------------------\n");

    printf("\nSub-expression evaluation order:\n");
    printf("1. d + e\n");
    printf("2. c - (d + e)\n");
    printf("3. a + b\n");
    printf("4. (a + b) - [c - (d + e)]\n");

    printf("\nRegister allocation:\n");
    printf("R1 -> First sub-expression\n");
    printf("R2 -> Second sub-expression\n");

    printf("\nTarget Instructions:\n");

    printf("\nStep 1: Calculate d + e\n");
    printf("MOV R1, d\n");
    printf("ADD R1, e\n");
    printf("R1 = d + e\n");

    printf("\nStep 2: Calculate c - (d + e)\n");
    printf("MOV R2, c\n");
    printf("SUB R2, R1\n");
    printf("R2 = c - (d + e)\n");

    printf("\nStep 3: Calculate a + b\n");
    printf("MOV R1, a\n");
    printf("ADD R1, b\n");
    printf("R1 = a + b\n");

    printf("\nStep 4: Calculate final result\n");
    printf("SUB R1, R2\n");
    printf("R1 = (a + b) - (c - (d + e))\n");

    printf("\nFinal result is stored in R1.\n");

    printf("\nComplete Two-Register Code:\n");
    printf("----------------------------\n");

    printf("MOV R1, d\n");
    printf("ADD R1, e\n");
    printf("MOV R2, c\n");
    printf("SUB R2, R1\n");
    printf("MOV R1, a\n");
    printf("ADD R1, b\n");
    printf("SUB R1, R2\n");

    /* ==========================================
       PART (b): ONE REGISTER CODE GENERATION
       ========================================== */

    printf("\n\n(b) OPTIMAL CODE USING ONE REGISTER\n");
    printf("------------------------------------\n");

    printf("\nOnly register available: R1\n");

    printf("\nIntermediate results must be stored in memory.\n");

    printf("\nStep 1: Calculate d + e\n");
    printf("MOV R1, d\n");
    printf("ADD R1, e\n");
    printf("MOV TEMP1, R1\n");
    printf("TEMP1 = d + e\n");

    printf("\nStep 2: Calculate c - (d + e)\n");
    printf("MOV R1, c\n");
    printf("SUB R1, TEMP1\n");
    printf("MOV TEMP2, R1\n");
    printf("TEMP2 = c - (d + e)\n");

    printf("\nStep 3: Calculate a + b\n");
    printf("MOV R1, a\n");
    printf("ADD R1, b\n");
    printf("MOV TEMP3, R1\n");
    printf("TEMP3 = a + b\n");

    printf("\nStep 4: Calculate final result\n");
    printf("MOV R1, TEMP3\n");
    printf("SUB R1, TEMP2\n");
    printf("MOV RESULT, R1\n");

    printf("\nComplete One-Register Code:\n");
    printf("---------------------------\n");

    printf("MOV R1, d\n");
    printf("ADD R1, e\n");
    printf("MOV TEMP1, R1\n");

    printf("MOV R1, c\n");
    printf("SUB R1, TEMP1\n");
    printf("MOV TEMP2, R1\n");

    printf("MOV R1, a\n");
    printf("ADD R1, b\n");
    printf("MOV TEMP3, R1\n");

    printf("MOV R1, TEMP3\n");
    printf("SUB R1, TEMP2\n");
    printf("MOV RESULT, R1\n");

    /* ==========================================
       COMPARISON
       ========================================== */

    printf("\n\nREGISTER CONSTRAINT COMPARISON\n");
    printf("------------------------------\n");

    printf("\nUsing TWO registers:\n");
    printf("- Intermediate values can remain in registers.\n");
    printf("- Fewer memory accesses are required.\n");
    printf("- Faster code generation.\n");

    printf("\nUsing ONE register:\n");
    printf("- Intermediate values are stored in memory.\n");
    printf("- More MOV instructions are required.\n");
    printf("- More memory accesses are required.\n");

    printf("\nSimulation completed successfully.\n");

    return 0;
}
