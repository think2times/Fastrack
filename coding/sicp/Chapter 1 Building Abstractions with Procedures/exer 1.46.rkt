#lang racket

(require "../modules/base.rkt")


(define tolerance 0.00001)

(define (good-enough? guess target tolerance)
  (< (abs (- guess target)) tolerance))

; 注意：这个函数的两个参数以及返回值都是函数，所以调用的语句外还要传一个参数作为 first-guess
(define (iterative-improve good-enough? improve-guess)
  (lambda (first-guess)
    (define (iter guess)
      (if (good-enough? guess)
          guess
          (iter (improve-guess guess))))
    (iter first-guess)))

; Rewrite Version
; 1.1.7 Square Roots by Newton's Method
(define (sqrt x)
  ((iterative-improve (lambda (guess) (good-enough? (square guess) x tolerance))
                      (lambda (guess) (average guess (/ x guess))))
   1.0))

; 1.3.3 Procedures as General Methods
(define (fixed-point f first-guess)
  ((iterative-improve (lambda (guess) (good-enough? guess (f guess) tolerance))
                      f)
   first-guess))


(sqrt 2)
(sqrt 10)

(fixed-point cos 1.0)
(fixed-point (lambda (x) (+ (sin x) (cos x))) 1.0)