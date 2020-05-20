package main

func main() {
    b := 5
    c := 5

    b = 100


    for i := 0; i <= 10; i = i + 1 {
        b = b + i
    }

    if b == 100 && c != 100 {
        b = b + i * 8 - c + 98 * b * b / c
    }
    else {
        b = 1
    }

}