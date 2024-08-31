#lang racket

(provide pi)
(provide runtime)
(provide square)
(provide cube)
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
