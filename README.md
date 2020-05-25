# PYGO - Python-based go-compiler

![Logotype](https://github.com/qnbhd/pygo/blob/master/misc/logo.png)

![License](https://img.shields.io/github/license/qnbhd/pygo)

# Запуск

Для того, чтобы скомпилировать программу необходимо запустить main.py с двумя параметрами:
+ SourceFile - файл с кодом
+ ProgramName - название программы 

```
python main.py SourceFile ProgramName
```

Пример запуска:

```
python main.py example.go Prog1
```

Результат работы компилятора будет создан в папке projects с именем вашей программы.

+ В папке bin находится файл ассемблера, исполняемый файл программы и obj-файл.
+ В папке logs находятся сведения от
  + Лексера (файл lex) cо списком токенов, которые он смог получить
  + Парсера (файл ast) с абстрактным синтаксическим деревом
  + Таблицы переменных (файл vars)
  

# Сведения о компиляторе

## Лексер

Производится лексический анализ входного файла и разбиение его на токены.

+ Распознаёт практически все лексемы языка <\b>Go<\b>
+ Не реализована поддержка комментариев


## Парсер

На вход поступает список токенов, созданных лексическим анализатором. По правилам языка и списку токенов строится
абстрактное синтаксическое дерево (AST)

+ Дерево растёт в ширину и может иметь много потомков

Пример AST:

```
+-PROGRAM 
   +-STATEMENT_LIST 
      +-STATEMENT_LIST 
         +-PACKAGE 'main'
      +-STATEMENT_LIST 
         +-STATEMENT_LIST 
            +-STATEMENT_LIST 
               +-SET 
                  +-VARIABLE_DECLARATION 'b'
                  +-INTEGER_CONST '5'
            +-SET 
               +-VARIABLE_DECLARATION 'c1'
               +-INTEGER_CONST '6'
         +-FOR 
            +-SET 
               +-VARIABLE_DECLARATION 'i'
               +-INTEGER_CONST '0'
            +-LESS 
               +-USING_VARIABLE 'i'
               +-INTEGER_CONST '10'
            +-SET 
               +-USING_VARIABLE 'i'
               +-ADD 
                  +-USING_VARIABLE 'i'
                  +-INTEGER_CONST '1'
            +-STATEMENT_LIST 
               +-PRINT 
                  +-USING_VARIABLE 'i'

```

построенного по программе

```go
package main

import (
    "fmt"
)

func main() {

    b := 5
    c1 := 6


    for i:=0; i < 10; i = i + 1 {
        fmt.Print(i)
    }
}
```

Парсер распознаёт следующие конструкции:

+ Математические выражения, операторы ```+, -, *, /```

+ Цикл for
```go
for <assignment>; <condition>; <assignment> 
{
        // code
}
```

+ Условия if-else
```go
if <condition> {
    // code
} else {
    // code
}
```

+ Оператор вывода ```fmt.Print()```

- Тип всего один - число, указания типов также нет

+ Операторы package, import сделаны формально для корректности программ на входном языке


## Генератор кода

Принимает на вход построенное AST-дерево и строит по нему комманды макроассемблера (MASM32).


## Разработчики

[<img alt="qnbhd" src="https://avatars0.githubusercontent.com/u/6369915?s=117&u=c1f9b58a96ebf950b2547b67fc06f54f5a8fa7a3" width="117">](https://github.com/qnbhd)[<img alt="TheXaver" src="https://avatars0.githubusercontent.com/u/18555344?s=117&u=2cf5d9e4ad349d7c16b5e59bc0382d98a90860a9" width="117">](https://github.com/TheXaver)

## Лицензия

GNU GPLv3


Copyright (c) 2020 Konstantin Templin & Andrei Gavrilov
