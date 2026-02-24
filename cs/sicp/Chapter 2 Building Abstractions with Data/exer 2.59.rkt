#lang racket


(define (element-of-set? x set)
  (cond ((null? set) false)
        ((equal? x (car set)) true)
        (else (element-of-set? x (cdr set)))))

(define (union-set set1 set2)
  (cond ((null? set1) set2)
        ((element-of-set? (car set1) set2)
         (union-set (cdr set1) set2))
        (else (cons (car set1) (union-set (cdr set1) set2)))))


(define set1 (list 1 3 5 'a 'b 'c))
(define set2 (list 2 4 6 'a 'd 'c))

(union-set set1 set2)
