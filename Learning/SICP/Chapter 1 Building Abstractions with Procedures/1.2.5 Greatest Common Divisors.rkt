#lang racket

(require racket/trace)

(define (gcd a b)
  (if (= b 0)
      a
      (gcd b (remainder a b))))


(trace gcd)
(gcd 40 206)