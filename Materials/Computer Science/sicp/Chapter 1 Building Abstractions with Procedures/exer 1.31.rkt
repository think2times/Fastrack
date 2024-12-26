#lang racket

(require "../modules/base.rkt")

; template of "production of a series".
; use recursive
(define (product-recur term a next b)
  (if (> a b)
      1
      (* (term a)
         (product-recur term (next a) next b))))

; use iter
(define (product-iter term a next b)
  (define (iter a result)
    (if (> a b)
        result
        (iter (next a) (* (term a) result))))
  (iter a 1))

; computes the factorial of the integers in the given number.
(define (factorial n)
  (define (identity x) x)
  (product-recur identity 1 inc n))


(factorial 0)
(factorial 1)
(factorial 2)
(factorial 3)
