[Building Abstractions with Data]()

# 1. Introduction to Data Abstraction

## Exercise 2.1
> Exercise 2.1: Define a better version of $make-rat$ that handles both positive and negative arguments. $make-rat$ should normalize the sign so that if the rational number is positive, both the numerator and denominator are positive, and if the rational number is negative, only the numerator is negative.
---
> 第一章学完了，今天开始学习第二章，目前还没有遇到什么问题，这道题也比较简单，只要注意到“分子分母同时为正，或者分子为负，分母为正，不需要改变符号；分子分母同时为负,或者分子为正,分母为负,分子分母都需要改变符号”这一点，就可以很容易地实现题目要求。
```
; (make-rat ⟨n⟩ ⟨d ⟩) returns the rational number whose numerator is the integer ⟨n⟩ and whose denominator is the integer ⟨d ⟩.
(define (make-rat n d)
  (let ((n (/ n (gcd n d)))
        (d (/ d (gcd n d))))
    ; 分子分母同时为正，或者分子为负，分母为正，不需要改变符号
    ; 分子分母同时为负,或者分子为正,分母为负,分子分母都需要改变符号
    (if (or (and (positive? n) (positive? d))
            (and (negative? n) (positive? d)))
        (cons n d)
        (cons (- 0 n) (- 0 d)))))

; (numer ⟨x⟩) returns the numerator of the rational number ⟨x⟩.
(define (numer x) (car x))

; (denom ⟨x⟩) returns the denominator of the rational number ⟨x⟩.
(define (denom x) (cdr x))

(define (add-rat x y)
  (make-rat (+ (* (numer x) (denom y))
               (* (numer y) (denom x)))
            (* (denom x) (denom y))))

(define (sub-rat x y)
  (make-rat (- (* (numer x) (denom y))
               (* (numer y) (denom x)))
            (* (denom x) (denom y))))

(define (mul-rat x y)
  (make-rat (* (numer x) (numer y))
            (* (denom x) (denom y))))

(define (div-rat x y)
  (make-rat (* (numer x) (denom y))
            (* (denom x) (numer y))))

(define (equal-rat? x y)
  (= (* (numer x) (denom y))
     (* (numer y) (denom x))))

(define (print-rat x)
  (newline)
  (display (numer x))
  (display "/")
  (display (denom x)))


(print-rat (make-rat -1 2))
(print-rat (make-rat 1 2))

(define neg-one-half (make-rat -1 2))
(define one-third (make-rat 1 3))

(print-rat (add-rat neg-one-half one-third))
(print-rat (add-rat neg-one-half neg-one-half))
(print-rat (sub-rat neg-one-half one-third))
(print-rat (mul-rat neg-one-half one-third))
(print-rat (div-rat neg-one-half one-third))

; 执行结果
-1/2
1/2
-1/6
-1/1
-5/6
-1/6
-3/2
```
> 可以看出这里还是有改进空间，-1/1 写成 -1 就行，利用 $gcd$ 就可以实现，不过我暂时不改了，也许后面有道题目会让做这个事情，到时候再说。