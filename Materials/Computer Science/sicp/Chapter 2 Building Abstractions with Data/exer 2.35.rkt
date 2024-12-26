#lang racket

(require "../Modules/base.rkt")


(define (accumulate op initial sequence)
  (if (null? sequence)
      initial
      (op (car sequence)
          (accumulate op initial (cdr sequence)))))

(define (enumerate-tree tree)
  (cond ((null? tree) nil)
        ((not (pair? tree)) (list tree))
        (else (append (enumerate-tree (car tree))
                      (enumerate-tree (cdr tree))))))

(define (count-leaves t)
  (accumulate
   +
   0
   (map (lambda (x) (if (null? x) 0 1)) 
        (enumerate-tree t))))


(define x (cons (list 1 2) (list 1 3 0 (list 2 4 6) 0 1)))
(count-leaves x)
(count-leaves (list x x))
