#lang racket

(require "../Modules/base.rkt")


(define (count-leaves x)
  (cond ((null? x) 0)
        ((not (pair? x)) 1)
        (else (+ (count-leaves (car x))
                 (count-leaves (cdr x))))))


(define x (cons (list 1 2) (list 3 4)))
(count-leaves x)
(count-leaves (list x x))


; Mapping over trees
(define (scale-tree tree factor)
  (cond ((null? tree) nil)
        ((not (pair? tree)) (* tree factor))
        (else (cons (scale-tree (car tree) factor)
                    (scale-tree (cdr tree) factor)))))

(define (scale-tree-by-map tree factor)
  (map (lambda (sub-tree)
         (if (pair? sub-tree)
             (scale-tree-by-map sub-tree factor)
             (* sub-tree factor)))
       tree))


(define test (list 1 (list 2 (list 3 4) 5) (list 6 7)))
(scale-tree test 10)
(scale-tree-by-map test 10)
