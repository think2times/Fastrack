#lang racket

(require "../Modules/base.rkt")


(define (fringe tree)
  (define (iter tree result)
    (cond ((null? tree) result)
          ((not (pair? tree)) (cons tree result))
          (else (append (iter (car tree) nil)
                        (iter (cdr tree) result)))))

  (iter tree nil))


(define x (list (list 1 2) (list 3 4)))

(fringe x)
(fringe (list x x))
