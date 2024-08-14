#lang racket
(require racket/trace)

(define (square x) (* x x))
(define (even? n)
  (= (remainder n 2) 0))

(define (expt-iter-by-square b n)
  (define (iter b n a)
    (cond ((= n 0) a)
          ((even? n) (iter (square b)
                           (/ n 2)
                           a))
          (else (iter b
                      (- n 1)
                      (* a b)))))
  (iter b n 1))

(trace expt-iter-by-square)
(expt-iter-by-square 2 127)
