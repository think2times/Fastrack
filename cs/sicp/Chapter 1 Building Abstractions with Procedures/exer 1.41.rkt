#lang racket

(define (double f)
  (lambda (x) (f (f x))))

(define (inc a)
  (+ a 1))

(define (halve a)
  (/ a 2))


(((double (double double)) inc) 5)

(((double double) halve) 1024)
