#lang racket


(define (union-set set1 set2)
  (cond ((null? set1) set2)
        ((null? set2) set1)
        ((let ((s1 (car set1))
               (s2 (car set2)))
           (if (<= s1 s2)
               (cons s1 (union-set (cdr set1) set2))
               (cons s2 (union-set set1 (cdr set2))))))))

(define set1 (list 1 3 5 7 9))
(define set2 (list 2 4 6 8 10))

(union-set set1 set2)
