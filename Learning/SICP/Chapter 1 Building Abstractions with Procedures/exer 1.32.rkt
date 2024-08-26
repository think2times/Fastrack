#lang racket

(require "../modules/base.rkt")

; template of "accumulation of a series".
; use recursive
(define (accumulate-recur combiner null-value term a next b)
  (if (> a b)
      null-value
      (combiner (term a)
                (accumulate-recur combiner null-value term (next a) next b))))

; use iter
(define (accumulate-iter combiner null-value term a next b)
  (define (iter a result)
    (if (> a b)
        result
        (iter (next a) (combiner (term a) result))))
  (iter a null-value))

; computes the summation of two numbers
(define (sum a b)
  (accumulate-recur + 0 identity a inc b))

; computers the production of two numbers
(define (product a b)
  (accumulate-recur * 1 identity a inc b))


; computes the factorial of the integers in the given number.
(define (factorial n)
  (define (identity x) x)
  (accumulate-iter * 1 identity 1 inc n))


(sum 3 5)
(product 3 5)

(factorial 0)
(factorial 1)
(factorial 2)
(factorial 3)
