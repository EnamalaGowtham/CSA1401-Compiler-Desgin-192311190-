#include <stdio.h>

int main()
{
    printf("DAG CONSTRUCTION AND OPTIMIZED CODE GENERATION\n");
    printf("================================================\n\n");

    /* ---------------------------------------------
       GIVEN BASIC BLOCK
       --------------------------------------------- */

    printf("GIVEN BASIC BLOCK\n");
    printf("-----------------\n");

    printf("1. d := b * c\n");
    printf("2. e := a + b\n");
    printf("3. b := b * c\n");
    printf("4. a := e - d\n");

    /* ---------------------------------------------
       PART A: DAG CONSTRUCTION
       --------------------------------------------- */

    printf("\n(a) DAG CONSTRUCTION\n");
    printf("--------------------\n");

    printf("\nStep 1: Operand Nodes\n");
    printf("Leaf nodes: a, b, c\n");

    printf("\nStep 2: Operator Nodes\n");

    printf("\nNode N1: b * c\n");
    printf("       (*)\n");
    printf("      /   \\\n");
    printf("     b     c\n");

    printf("\nNode N2: a + b\n");
    printf("       (+)\n");
    printf("      /   \\\n");
    printf("     a     b\n");

    printf("\nNode N3: e - d\n");
    printf("       (-)\n");
    printf("      /   \\\n");
    printf("     e     d\n");

    /* ---------------------------------------------
       COMMON SUB-EXPRESSION
       --------------------------------------------- */

    printf("\nCOMMON SUB-EXPRESSION DETECTION\n");
    printf("-------------------------------\n");

    printf("Expression 'b * c' occurs twice.\n");
    printf("1. d := b * c\n");
    printf("2. b := b * c\n");

    printf("\nDAG uses only ONE node for b * c.\n");

    printf("\nDAG REPRESENTATION\n");
    printf("------------------\n");

    printf("             (-)\n");
    printf("            /   \\\n");
    printf("           e     d\n");
    printf("          /       \\\n");
    printf("        (+)       (*)\n");
    printf("       /   \\     /   \\\n");
    printf("      a     b   b     c\n");

    printf("\nLabels:\n");
    printf("(*) -> d, b\n");
    printf("(+) -> e\n");
    printf("(-) -> a\n");

    /* ---------------------------------------------
       REDUNDANT COMPUTATION ELIMINATION
       --------------------------------------------- */

    printf("\nREDUNDANT COMPUTATION ELIMINATION\n");
    printf("---------------------------------\n");

    printf("Original:\n");
    printf("d = b * c\n");
    printf("b = b * c\n");

    printf("\nOptimized idea:\n");
    printf("t1 = b * c\n");
    printf("d = t1\n");
    printf("b = t1\n");

    printf("\nTherefore, b * c is calculated only once.\n");

    /* ---------------------------------------------
       PART B: ONE REGISTER CODE GENERATION
       --------------------------------------------- */

    printf("\n(b) OPTIMIZED CODE USING ONE REGISTER\n");
    printf("-------------------------------------\n");

    printf("\nOnly register used: R1\n");

    printf("\nStep 1: Preserve original b\n");
    printf("MOV R1, b\n");
    printf("MOV d, R1\n");
    printf("MOV temp, R1\n");

    printf("\nStep 2: Calculate e = a + b\n");
    printf("MOV R1, a\n");
    printf("ADD R1, temp\n");
    printf("MOV e, R1\n");

    printf("\nStep 3: Calculate common expression b * c\n");
    printf("MOV R1, b\n");
    printf("MUL R1, c\n");
    printf("MOV d, R1\n");
    printf("MOV b, R1\n");

    printf("\nStep 4: Calculate a = e - d\n");
    printf("MOV R1, e\n");
    printf("SUB R1, d\n");
    printf("MOV a, R1\n");

    /* ---------------------------------------------
       FINAL OPTIMIZED CODE
       --------------------------------------------- */

    printf("\nFINAL OPTIMIZED TARGET CODE\n");
    printf("---------------------------\n");

    printf("MOV R1, b\n");
    printf("MOV d, R1\n");
    printf("MOV temp, R1\n");

    printf("MOV R1, a\n");
    printf("ADD R1, temp\n");
    printf("MOV e, R1\n");

    printf("MOV R1, temp\n");
    printf("MUL R1, c\n");
    printf("MOV d, R1\n");
    printf("MOV b, R1\n");

    printf("MOV R1, e\n");
    printf("SUB R1, d\n");
    printf("MOV a, R1\n");

    /* ---------------------------------------------
       REGISTER USAGE
       --------------------------------------------- */

    printf("\nREGISTER USAGE\n");
    printf("--------------\n");

    printf("R1 -> Holds one intermediate value at a time.\n");
    printf("temp -> Preserves the original value of b.\n");
    printf("d -> Stores b * c.\n");
    printf("e -> Stores a + b.\n");
    printf("a -> Stores final result e - d.\n");

    printf("\nSimulation completed successfully.\n");

    return 0;
}
