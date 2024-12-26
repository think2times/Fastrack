#lang racket


(define (make-mobile left right)
  (list left right))

(define (make-branch length structure)
  (list length structure))

(define (left-branch mobile)
  (car mobile))

(define (right-branch mobile)
  (car (cdr mobile)))

(define (branch-length branch)
  (car branch))

(define (branch-structure branch)
  (car (cdr branch)))

(define (total-weight mobile)
  (cond ((null? mobile) 0)
        ((not (pair? mobile)) mobile)
        (else (+ (total-weight (branch-structure (left-branch mobile)))
                 (total-weight (branch-structure (right-branch mobile)))))))

(define (torque branch)
  (* (branch-length branch)
     (total-weight (branch-structure branch))))

(define (balanced? mobile)
  (if (not (pair? mobile))
      true
      (= (torque (left-branch mobile))
         (torque (right-branch mobile)))))


(newline)
(define a (make-mobile (make-branch 2 3) (make-branch 3 2)))
(total-weight a)
(balanced? a)

(newline)
(define b (make-mobile (make-branch 2 a) (make-branch 4 a)))
(total-weight b)
(balanced? b)

(newline)
(define c (make-mobile (make-branch 2 b) (make-branch 3 a)))
(total-weight c)
(balanced? c)
