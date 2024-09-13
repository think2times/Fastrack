#lang racket

(require "../modules/base.rkt")

; template of "summation of a series".
(define (sum term a next b)
  (if (> a b)
      0
      (+ (term a)
         (sum term (next a) next b))))

; computes the sum of the cubes of the integers in the given range.
(define (sum-cubes a b)
  (sum cube a inc b))

; computes the sum of the integers in the given range.
(define (identity x) x)
(define (sum-int a b)
  (sum identity a inc b))

; computes the sum of a sequence of terms in the series
;  1/(1*3)+1/(5*7)+1/(9*11)+...,
(define (pi-sum a b)
  (define (pi-term a)
    (/ 1.0 (* a (+ a 2))))
  (define (pi-next a)
    (+ a 4))
  (sum pi-term a pi-next b))

; computes the definite integral of a function f between the limits a and b
(define (integral f a b dx)
  (define (add-dx x)
    (+ x dx))
  (* (sum f (+ a (/ dx 2.0)) add-dx b)
     dx))


(sum-cubes 3 5)
(sum-int 1 10)
(* 8 (pi-sum 1 1000))
(integral cube 0 1 0.01)
(integral cube 0 1 0.001)
