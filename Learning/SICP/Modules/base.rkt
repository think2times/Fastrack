#lang racket

(provide pi)
(provide runtime)
(provide square)
(provide cube)
(provide expt)
(provide even?)
(provide double)
(provide halve)
(provide inc)
(provide average)
(provide positive?)
(provide negative?)


(define pi 3.141592653589793)

; returns a guaranteed-to-increase floating point number which represent the current millisecond count from the system
(define (runtime)
  (current-inexact-milliseconds))

(define (square x)
  (* x x))

(define (cube x)
  (* x x x))

(define (expt b n) 
  (cond ((= n 0) 1) 
        ((even? n) (square (expt b (/ n 2)))) 
        (else (* b (expt b (- n 1)))))) 

(define (even? n)
  (= (remainder n 2) 0))

(define (double a)
  (* a 2))

(define (halve a)
  (/ a 2))

(define (inc a)
  (+ a 1))

(define (average a b)
  (/ (+ a b) 2))

(define (positive? x)
  (if (> x 0) true false))

(define (negative? x)
  (if (< x 0) true false))
