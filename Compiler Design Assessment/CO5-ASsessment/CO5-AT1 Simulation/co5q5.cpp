#include <iostream>
using namespace std;

int main()
{
    int n = 5;
    int x = 10;
    int y = 2;
    int z = 5;
    int w = 8;

    cout << "CODE OPTIMIZATION SIMULATION\n";
    cout << "============================\n\n";

    cout << "Original Expression:\n";
    cout << "a[i]   = x * y + z\n";
    cout << "a[i+n] = x * y + w\n\n";

    // ------------------------------------------------
    // PART (a): COMMON SUBEXPRESSION IDENTIFICATION
    // ------------------------------------------------

    cout << "(a) COMMON SUBEXPRESSION ELIMINATION\n";
    cout << "-------------------------------------\n";

    cout << "\nCommon sub-expression identified:\n";
    cout << "x * y\n";

    cout << "\nOriginal computation inside loop:\n";
    cout << "t1 = x * y\n";
    cout << "t2 = t1 + z\n";
    cout << "a[i] = t2\n";
    cout << "t3 = x * y\n";
    cout << "t4 = t3 + w\n";
    cout << "a[i+n] = t4\n";

    cout << "\nThe expression x * y is calculated twice.\n";

    // ------------------------------------------------
    // CODE MOTION
    // ------------------------------------------------

    cout << "\nCODE MOTION\n";
    cout << "-----------\n";

    cout << "Since x * y does not depend on i,\n";
    cout << "it can be moved outside the loop.\n";

    cout << "\nOptimized computation:\n";
    cout << "t = x * y\n";
    cout << "for (i = 0; i < n; i++)\n";
    cout << "{\n";
    cout << "    a[i] = t + z;\n";
    cout << "    a[i+n] = t + w;\n";
    cout << "}\n";

    // ------------------------------------------------
    // OPTIMIZED C++ CODE
    // ------------------------------------------------

    cout << "\nOPTIMIZED C++ CODE\n";
    cout << "------------------\n";

    cout << "int t = x * y;\n";
    cout << "for (int i = 0; i < n; i++)\n";
    cout << "{\n";
    cout << "    a[i] = t + z;\n";
    cout << "    a[i+n] = t + w;\n";
    cout << "}\n";

    // ------------------------------------------------
    // TAC
    // ------------------------------------------------

    cout << "\nOPTIMIZED THREE ADDRESS CODE\n";
    cout << "----------------------------\n";

    cout << "t1 = x * y\n";
    cout << "i = 0\n";
    cout << "L1: if i >= n goto L2\n";
    cout << "t2 = t1 + z\n";
    cout << "a[i] = t2\n";
    cout << "t3 = t1 + w\n";
    cout << "a[i+n] = t3\n";
    cout << "i = i + 1\n";
    cout << "goto L1\n";
    cout << "L2: End\n";

    // ------------------------------------------------
    // PART (b): ANALYSIS
    // ------------------------------------------------

    cout << "\n(b) ANALYSIS OF OPTIMIZED CODE\n";
    cout << "------------------------------\n";

    cout << "\nNumber of loop iterations: " << n << endl;

    int originalMultiplications = 2 * n;
    int optimizedMultiplications = 1;

    cout << "\nOriginal number of x*y computations: "
         << originalMultiplications << endl;

    cout << "Optimized number of x*y computations: "
         << optimizedMultiplications << endl;

    cout << "\nMultiplication reduction: "
         << originalMultiplications - optimizedMultiplications
         << endl;

    // ------------------------------------------------
    // SIMULATE ORIGINAL EXECUTION
    // ------------------------------------------------

    cout << "\nORIGINAL CODE SIMULATION\n";
    cout << "------------------------\n";

    for (int i = 0; i < n; i++)
    {
        int t1 = x * y;
        int value1 = t1 + z;

        int t2 = x * y;
        int value2 = t2 + w;

        cout << "Iteration " << i
             << ": x*y calculated twice"
             << ", a[i] = " << value1
             << ", a[i+n] = " << value2 << endl;
    }

    // ------------------------------------------------
    // SIMULATE OPTIMIZED EXECUTION
    // ------------------------------------------------

    cout << "\nOPTIMIZED CODE SIMULATION\n";
    cout << "-------------------------\n";

    int t = x * y;

    cout << "x * y calculated once = " << t << endl;

    for (int i = 0; i < n; i++)
    {
        int value1 = t + z;
        int value2 = t + w;

        cout << "Iteration " << i
             << ": reused x*y"
             << ", a[i] = " << value1
             << ", a[i+n] = " << value2 << endl;
    }

    // ------------------------------------------------
    // BENEFITS
    // ------------------------------------------------

    cout << "\nBENEFITS OF OPTIMIZATION\n";
    cout << "------------------------\n";

    cout << "1. Common sub-expression x*y is calculated only once.\n";
    cout << "2. Loop-invariant computation is moved outside the loop.\n";
    cout << "3. Number of multiplications is reduced.\n";
    cout << "4. Execution time is reduced.\n";
    cout << "5. Computed value is reused in every iteration.\n";

    cout << "\nSimulation completed successfully.\n";

    return 0;
}
