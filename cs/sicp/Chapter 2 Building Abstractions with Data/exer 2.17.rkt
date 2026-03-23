#lang racket


(define (last-pair list1)
  (let ((last (car list1)))
    (if (null? (cdr list1))
        last
        (last-pair (cdr list1)))))


(last-pair (list 23 72 149 34))
