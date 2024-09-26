#lang racket

(require "../Modules/base.rkt")


(define (square-tree tree)
  (cond ((null? tree) nil)
        ((not (pair? tree)) (square tree))
        (else (cons (square-tree (car tree))
                    (square-tree (cdr tree))))))

(define (square-tree-by-map tree)
  (map (lambda (sub-tree)
         (if (pair? sub-tree)
             (square-tree-by-map sub-tree)
             (square sub-tree)))
       tree))


(define test (list 1
                   (list 2 (list 3 4) 5)
                   (list 6 7)))

(square-tree test)
(square-tree-by-map test)
