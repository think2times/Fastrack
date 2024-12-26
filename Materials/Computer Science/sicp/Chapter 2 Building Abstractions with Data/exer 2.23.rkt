#lang racket

(require "../Modules/base.rkt")


(define (for-each f items)
  (cond ((not (null? items))
         (f (car items))
         (for-each f (cdr items)))))


(define test (list 57 321 88))
(for-each (lambda(x) (newline) (display x))
          test)

(newline)

(for-each (lambda(x) (newline) (display (square x)))
          test)
