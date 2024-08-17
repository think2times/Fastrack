#lang racket

(provide square)
(provide cube)
(provide even?)
(provide double)
(provide halve)

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