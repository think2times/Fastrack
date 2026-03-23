#include <stdio.h>
#include <string.h>

typedef unsigned char *byte_pointer;

void show_bytes(byte_pointer start, size_t len) {
    int i;
    for (i=0; i < len; i++)
        printf(" %.2x", start[i]);
    printf("\n");
}

void show_int(int x) {
    show_bytes((byte_pointer) &x, sizeof(int));
}

void show_float(float x) {
    show_bytes((byte_pointer) &x, sizeof(float));
}

void show_pointer(void *x) {
    show_bytes((byte_pointer) &x, sizeof(void *));
}

void test_show_bytes(int val) {
    int ival = val;
    float fval = val;
    int *pval = &val;
    show_int(ival);
    show_float(fval);
    show_pointer(pval);
}

void inplace_swap(int *x, int *y) {
    *y = *x ^ *y;  /* Step 1 */
    *x = *x ^ *y;  /* Step 2 */
    *y = *x ^ *y;  /* Step 3 */
}

void reverse_array(int a[], int cnt) {
    int first, last;
    for (first = 0, last = cnt-1;
         first < last;
         first++, last--)
         inplace_swap(&a[first], &a[last]);
}

/* Declarations of functions implementing operations bis and bic */
int bis(int x, int m) {
    return x | m;
}

int bic(int x, int m) {
    return bis(x, x & ~m);
}

/* Compute x|y using only calls to functions bis and bic */
int bool_or(int x, int y) {
    int result = bis(x, y);
    return result;
}

/* Compute x^y using only calls to functions bis and bic */
int bool_xor(int x, int y) {
    int result = bis(bic(x, y), bic(y, x));
    return result;
}

int fun2(unsigned x) {
    return ((int) x << 24) >> 24;
}

int main() {
    int x = 0xEDCBA987;
    printf("0x%X\n", fun2(x));

    return 0;
}
