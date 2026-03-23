#lang racket


(define (element-of-set? x set)
  (cond ((null? set) false)
        ((equal? x (car set)) true)
        (else (element-of-set? x (cdr set)))))

(define (adjoin-set x set)
  (cons x set))

(define (intersection-set set1 set2)
  (cond ((or (null? set1) (null? set2)) '())
        ((element-of-set? (car set1) set2)
         (cons (car set1) (intersection-set (cdr set1) set2)))
        (else (intersection-set (cdr set1) set2))))

(define (union-set set1 set2)
  (append set1 set2))


(define set1 (list 1 3 5 'a 'b 'c))
(define set2 (list 2 4 6 'a 'd 'c))

(adjoin-set 'a set1)
(union-set set1 set2)
(intersection-set set1 set2)
