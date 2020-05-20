package main

func main() {
    result := 0

    b := 5
    c1 := 6

    b = 50

    if b == 100 {
        for i := 0; i <= 10; i = i + 1 {
            b = b + i
        }
    } else if b < 100 && c1 == 5 {
        b = 1000
    } else if b < 100 && c1 == 6 {
        b = 2000
    }




    result = b
}