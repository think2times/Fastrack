#lang racket

(require "../Modules/base.rkt")


(define (square-list items)
  (define (iter things answer)
    (if (null? things)
        answer
        (iter (cdr things)
              (cons answer
                    (square (car things))))))
  (iter items nil))


(define odds (list 1 3 5 7 9))
(square-list odds)