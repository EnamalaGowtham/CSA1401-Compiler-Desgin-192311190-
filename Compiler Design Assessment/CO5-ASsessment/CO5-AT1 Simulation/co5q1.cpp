#include <stdio.h>

int main()
{
    printf("INTERMEDIATE CODE GENERATION SIMULATION\n");
    printf("========================================\n\n");

    /* Part A: Three Address Code */
    printf("(a) THREE ADDRESS CODE (TAC)\n");
    printf("----------------------------\n");

    printf("1.  sum = 0\n");
    printf("2.  i = 0\n");
    printf("3.  L1: if i > 10 goto L2\n");
    printf("4.  t1 = a[i]\n");
    printf("5.  t2 = sum + t1\n");
    printf("6.  sum = t2\n");
    printf("7.  i = i + 1\n");
    printf("8.  goto L1\n");
    printf("9.  L2: End\n\n");

    /* Part B: Leaders */
    printf("(b) BASIC BLOCK AND CONTROL FLOW ANALYSIS\n");
    printf("-------------------------------------------\n");

    printf("\n1. LEADER STATEMENTS\n");
    printf("--------------------\n");
    printf("Leader 1: Statement 1 -> sum = 0\n");
    printf("Leader 2: Statement 3 -> L1: if i > 10 goto L2\n");
    printf("Leader 3: Statement 4 -> t1 = a[i]\n");
    printf("Leader 4: Statement 9 -> L2: End\n");

    /* Basic Blocks */
    printf("\n2. BASIC BLOCKS\n");
    printf("---------------\n");

    printf("\nBasic Block B1:\n");
    printf("  1. sum = 0\n");
    printf("  2. i = 0\n");

    printf("\nBasic Block B2:\n");
    printf("  3. if i > 10 goto L2\n");

    printf("\nBasic Block B3:\n");
    printf("  4. t1 = a[i]\n");
    printf("  5. t2 = sum + t1\n");
    printf("  6. sum = t2\n");
    printf("  7. i = i + 1\n");
    printf("  8. goto L1\n");

    printf("\nBasic Block B4:\n");
    printf("  9. End\n");

    /* CFG */
    printf("\n3. CONTROL FLOW GRAPH (CFG)\n");
    printf("---------------------------\n");

    printf("\nB1 -> B2\n");
    printf("B2 -> B3  (if i <= 10)\n");
    printf("B2 -> B4  (if i > 10)\n");
    printf("B3 -> B2  (after i = i + 1)\n");

    printf("\nCFG Representation:\n\n");

    printf("       +--------+\n");
    printf("       |   B1   |\n");
    printf("       |sum=0   |\n");
    printf("       |i=0     |\n");
    printf("       +---+----+\n");
    printf("           |\n");
    printf("           v\n");
    printf("       +--------+\n");
    printf("       |   B2   |\n");
    printf("       |i > 10? |\n");
    printf("       +--+--+--+\n");
    printf("        Yes  No\n");
    printf("         |    |\n");
    printf("         v    v\n");
    printf("      +----+ +--------+\n");
    printf("      | B4 | |   B3   |\n");
    printf("      |End | |a[i]    |\n");
    printf("      +----+ |sum+t1  |\n");
    printf("             |i=i+1   |\n");
    printf("             +---+----+\n");
    printf("                 |\n");
    printf("                 +----> B2\n");

    printf("\nSimulation completed successfully.\n");

    return 0;
}
