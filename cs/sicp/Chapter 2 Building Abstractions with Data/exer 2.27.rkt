#lang racket

(require "../Modules/base.rkt")


(define (deep-reverse-by-reverse items) 
  (define (iter items result) 
    (if (null? items) 
        result 
        (if (pair? (car items)) 
            (let ((x (iter (car items) nil))) 
              (iter (cdr items) (cons x result))) 
            (iter (cdr items) (cons (car items) result))))) 
  (iter items nil))

(define (deep-reverse items)
  (if (pair? items)
      (append (deep-reverse (cdr items))
              (list (deep-reverse (car items))))
      items))


(define x (list (list 1 2) (list 3 4)))

x
(reverse x)
(deep-reverse x)

(deep-reverse '(1 2 (3 4) 5 (6 (7 8) 9) 10)) 
