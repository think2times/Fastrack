#lang racket
(require racket/trace)

(define (double a)
  (* a 2))

(define (halve a)
  (/ a 2))

(define (even? n)
  (= (remainder n 2) 0))

(define (multiply-recur a b)
  (cond ((= b 0) 0)
        ((even? b) (multiply-recur (double a) (halve b)))
        (else (+ a (multiply-recur a (- b 1))))))

(trace multiply-recur)
(multiply-recur 97 99)
