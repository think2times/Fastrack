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

int main() {
    int val = 12345;
    test_show_bytes(val);

    // practice 2.7
    const char *m = "mnopqr";
    show_bytes((byte_pointer) m, strlen(m));

    // practice 2.10
    int a = 10;
    int b = 11;
    inplace_swap(&a, &b);
    printf("\na is %d now, b is %d now. \n", a, b);

    // practice 2.11
    int my_numbers[] = {1, 2, 3, 4, 5};
    int size = sizeof(my_numbers) / sizeof(my_numbers[0]);
    reverse_array(my_numbers, size);

    printf("\nReversed array: ");
    for(int i = 0; i < size; i++) printf("%d ", my_numbers[i]);
    printf("\n");

    // page 104
    short x = 12345;
    short mx = -x;

    show_bytes((byte_pointer) &x, sizeof(short));
    show_bytes((byte_pointer) &mx, sizeof(short));

    return 0;
}
