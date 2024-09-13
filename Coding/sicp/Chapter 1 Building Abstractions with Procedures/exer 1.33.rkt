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
    (check-it (expmod a (- n 1) n)))         ; 检查a^(n-1)是否为n的倍数,且a^(n-1)÷n余数为1
  (try-it (+ 1 (random (- n 1)))))           ; random returns a nonnegative integer less than its integer input(from 1 to n).

; runs the test a given number of times, as specified by a parameter
(define (fast-prime? n times)
  (cond ((< n 2) false)            ; 2是最小的质数,所以小于2的数都不是质数
        ((= times 0) true)
        ((miller-rabin-test n) (fast-prime? n (- times 1)))
        (else false)))

(define (prime? n)
  (fast-prime? n 100))


(define (gcd a b)
  (if (= b 0)
      a
      (gcd b (remainder a b))))


; template of "accumulation of a series".
; recursive implementation
(define (filtered-accumulate-recur combiner null-value term a next b filter)
  (if (> a b)
      null-value
      (if (filter a)
          (combiner (term a) (filtered-accumulate-recur combiner null-value term (next a) next b filter))
          (combiner null-value (filtered-accumulate-recur combiner null-value term (next a) next b filter)))))

; iterative implementation
(define (filtered-accumulate-iter combiner null-value term a next b filter)
  (define (iter a result)
    (if (> a b)
        result
        (if (filter a)
            (iter (next a) (combiner (term a) result))
            (iter (next a) result))))
  (iter a null-value))

; computes the summation of the squares of the prime numbers in the interval a to b
(define (sum-prime-square a b)
  (filtered-accumulate-iter + 0 square a inc b prime?))

; computers the production of all the positive integers less thann that are relatively prime to n
(define (product-prime n)
  (filtered-accumulate-iter * 1 identity 1 inc n prime?))


(sum-prime-square 0 10)
(product-prime 10)
