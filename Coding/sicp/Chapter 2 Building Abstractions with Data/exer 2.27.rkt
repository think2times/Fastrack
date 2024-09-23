#lang racket

(require "../Modules/base.rkt")


(define (append list1 list2)
  (if (null? list1)
      list2
      (cons (car list1)
            (append (cdr list1) list2))))

(define (reverse items) 
  (define (iter items result) 
    (if (null? items) 
        result 
        (iter (cdr items) (cons (car items) result)))) 
  
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
  