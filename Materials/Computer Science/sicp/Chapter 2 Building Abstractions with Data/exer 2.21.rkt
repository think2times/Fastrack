#lang racket

(require "../Modules/base.rkt")


(define (square-list items)
  (if (null? items)
      nil
      (cons (square (car items))
            (square-list (cdr items)))))

(define (square-list-by-map items)
  (map square items))


(square-list (list 1 2 3 4))
(square-list-by-map (list 1 2 3 4))
   