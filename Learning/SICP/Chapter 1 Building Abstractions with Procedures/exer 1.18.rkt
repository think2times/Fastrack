#lang racket
(require racket/trace)

(define (double a)
  (* a 2))

(define (halve a)
  (/ a 2))

(define (even? n)
  (= (remainder n 2) 0))

(define (multiply-iter a b)
  (define (iter a b answer)
    (cond ((= b 0) answer)
          ((even? b) (iter (double a) (halve b) answer))
          (else (iter a (- b 1) (+ answer a)))))
  (iter a b 0))

(trace multiply-iter)
(multiply-iter 99 97)
