#include <stdio.h>

int return_102() {
    int val102 = 102;

    return val102;
}
int return_101() {
    int val=101;
    return_102();
    return 101;
}

int main() {
    int age=201;
    double height;
    char name[100];
    char buf[100];
    char a_char;
    char char2;

    char unit;
    char trailing;
    int num_read=202;
    int number;

    return_101();

    for(int ii = 0; ii < 20; ii++) {
        printf("Enter number followed by unit:");

        fgets(buf, sizeof(buf), stdin);
        num_read = sscanf(buf, "%d %c %c", &number, &unit, &trailing);
        printf("You entered: %d %c %c\n", number, unit, trailing);

        if (num_read < 2) {
            printf("Error: failed to enter number and unit\n");
        }
        if (num_read > 2) {
            printf("Error: After one character unit, no extra characters allowed\n");
        }
            
        int jj = 321;
    }

/*
num_read = sscanf("234 E", "%d %c %c", &age, &a_char, &char2);

num_read = sscanf("notNumber E", "%d %c%c", &age, &a_char, &char2);
num_read = sscanf("234 E", "%d %c%c", &age, &a_char, &char2);
num_read = sscanf("234 E", "%d %c %c", &age, &a_char, &char2);
num_read = sscanf("234 Ex", "%d %c%c", &age, &a_char, &char2);
num_read = sscanf("234 E y", "%d %c %c", &age, &a_char, &char2);
num_read = sscanf("234 Ey", "%d %c %c", &age, &a_char, &char2);
num_read = sscanf("234 E", "%d %c %c", &age, &a_char, &char2);

printf("Enter a char, anything trailing :");
num_read = scanf("%c%99s", &a_char, name);
printf("You entered char: %c (num_read=%d), name: %s\n",
a_char, num_read, name);

num_read = scanf("%c", &a_char);
printf("You entered char: %c (num_read=%d)\n", a_char, num_read);

printf("Enter a char, anything trailing :");
num_read = scanf("%c", &a_char);
printf("You entered char: %c (num_read=%d)\n", a_char, num_read);
*/

    return 0;
}

