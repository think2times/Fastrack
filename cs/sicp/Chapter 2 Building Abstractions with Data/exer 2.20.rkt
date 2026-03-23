#lang racket

(require "../Modules/base.rkt")


(define (reverse items) 
  (define (iter items result) 
    (if (null? items) 
        result 
        (iter (cdr items) (cons (car items) result)))) 
  
  (iter items nil)) 

(define (same-parity x . y)
  (define (iter items r result)
    (cond ((null? items) result)
          ((= r (remainder (car items) 2)) (iter (cdr items) r (cons (car items) result)))
          (else (iter (cdr items) r result))))
  (let ((r (remainder x 2)))
    (reverse (iter y r (cons x nil)))))


(same-parity 1 2 3 4 5 6 7)

(same-parity 2 3 4 5 6 7)

(same-parity 2)
