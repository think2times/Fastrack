#lang racket

(require "../modules/base.rkt")

; calculate the remainder of base^exp modulo m
(define (expmod base exp m)
  (cond ((= exp 0) 1)
        ((even? exp)
         (remainder
          (sqmod (expmod base (/ exp 2) m) m)
          m))
        (else
         (remainder
          (* base (expmod base (- exp 1) m))
          m))))

; Return 0 if `x^2 mod m` is equal to `1 mod m` and x != m - 1 and x != 1;
; x^2 otherwise."
(define (sqmod x m)  
  (cond ((and (= (remainder (square x) m) 1)    ; 1 mod m = 1 
              (not (= x (- m 1))) 
              (not (= x 1)))
         0)
        (else (square x))))

; Miller-Rabin test
; if n is a prime number and a is any positive integer less than n, then a raised to the (n-1)-st power is congruent to 1 modulo n.
; we pick a random number a < n and raise a to the (n 1)-st power modulo n to test if it is congruent to 1 modulon.
(define (miller-rabin-test n)
  (define (try-it a)
    (define (check-it x)
      (and (not (= x 0)) (= x 1)))
    (check-it (expmod a (- n 1) n)))         ; 检查a^(n-1)是否为n的倍数，且a^(n-1)÷n余数为1
  (try-it (+ 1 (random (- n 1)))))           ; random returns a nonnegative integer less than its integer input(from 1 to n).

; runs the test a given number of times, as specified by a parameter
(define (fast-prime? n times)
  (cond ((< n 2) false)            ; 2是最小的质数，所以小于2的数都不是质数
        ((= times 0) true)
        ((miller-rabin-test n) (fast-prime? n (- times 1)))
        (else false)))

(define (prime? n)
  (fast-prime? n 100))


(prime? 2)
(prime? 3)
(prime? 5)
(prime? 7)
(prime? 0)
(prime? 1)
(prime? 4)
(prime? 6)
(prime? 8)
(prime? 9)
(prime? 561)      ; 能被3整除
(prime? 1105)     ; 能被5整除
(prime? 1729)     ; 能被7整除
(prime? 2465)     ; 能被5整除
(prime? 2821)     ; 能被7整除
(prime? 6601)     ; 能被7整除
