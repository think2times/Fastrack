#lang racket


(define (adjoin-set x set)
  (let ((first (car set)))
    (cond ((null? set) (list x))
          ((<= x first) (cons x set))
          (else (cons first (adjoin-set x (cdr set)))))))
      

(define set1 (list 1 3 5 7 9))
(adjoin-set 6 set1)
