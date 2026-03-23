#lang racket

(require "../modules/base.rkt")


; The Fermat Test
; calculate the remainder of base^exp modulo m
(define (expmod base exp m) 
  (cond ((= exp 0) 1) 
        ((even? exp) 
          (remainder 
            (square (expmod base (/ exp 2) m)) ; (1) 
            m)) 
        (else 
          (remainder 
            (* base (expmod base (- exp 1) m)) 
            m))))

; The modified procedures 
(define (modified-expmod base exp m) 
  (remainder (fast-expt base exp) m))

; Helper procedures 
(define (fast-expt b n) 
  (cond ((= n 0) 1) 
        ((even? n) (square (fast-expt b (/ n 2)))) 
        (else (* b (fast-expt b (- n 1)))))) 

; calculate run time of a procedure
(define (report-elapsed-time start-time) 
  (display " *** ") 
  (display (- (runtime) start-time)))


; Test the speed 
(define start-time1 (runtime)) 
(expmod 999999 1000000 1000000) 
(report-elapsed-time start-time1)
(newline)

(define start-time2 (runtime)) 
(modified-expmod 999999 1000000 1000000) 
(report-elapsed-time start-time2)
