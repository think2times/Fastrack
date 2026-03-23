#lang racket

(require "../modules/base.rkt")

; The Fermat Test
; calculate the remainder of base^exp modulo m
(define (expmod base exp m)
  (cond ((= exp 0) 1)
        ((even? exp)
         (remainder
          (square (expmod base (/ exp 2) m))
          m))
        (else
         (remainder
          (* base (expmod base (- exp 1) m))
          m))))


; runs the test for every a that satisfy 2 <= a < n, as specified by a parameter
(define (fast-prime? n a)
  (cond ((= a n) true)
        ((= (expmod a n n) a) (fast-prime? n (+ a 1)))
        (else false)))

(fast-prime? 561 2)      ; 能被3整除
(fast-prime? 1105 2)     ; 能被5整除
(fast-prime? 1729 2)     ; 能被7整除
(fast-prime? 2465 2)     ; 能被5整除
(fast-prime? 2821 2)     ; 能被7整除
(fast-prime? 6601 2)     ; 能被7整除
