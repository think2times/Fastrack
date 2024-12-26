#lang racket

(require "../Modules/base.rkt")


(define (fold-right op initial sequence)
  (if (null? sequence)
      initial
      (op (car sequence)
          (fold-right op initial (cdr sequence)))))

(define (fold-left op initial sequence)
  (define (iter result rest)
    (if (null? rest)
        result
        (iter (op result (car rest))
              (cdr rest))))
  (iter initial sequence))

(define (reverse-by-right sequence)
  (fold-right (lambda (x y) (append y (list x))) nil sequence))

(define (reverse-by-left sequence)
  (fold-left (lambda (x y) (cons y x)) nil sequence))

(define odds (list 1 3 5 7 9))
(reverse-by-right odds)
(reverse-by-left odds)
