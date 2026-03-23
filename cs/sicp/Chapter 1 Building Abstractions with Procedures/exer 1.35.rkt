#lang racket

(require "../modules/base.rkt")

(define tolerance 0.001)

(define (close-enough? x y tolerance)
  (< (abs (- x y)) tolerance))

(define (fixed-point f first-guess)
  (define (close-enough? v1 v2 tolerance)
    (< (abs (- v1 v2))
       tolerance))
  (define (try guess)
    (let ((next (f guess)))
      (if (close-enough? guess next tolerance)
          next
          (try next))))
  (try first-guess))

; calculate the golden ratio φ by solve the equation: x = 1 + 1/x
(fixed-point (lambda (x) (+ 1 (/ 1 x)))
             1.0)
