#lang racket

(require "../modules/base.rkt")

(define (timed-prime-test n)
  (newline)
  (display n)
  (start-prime-test n (runtime)))

(define (start-prime-test n start-time)
  (cond ((prime? n)
         (report-prime (- (runtime) start-time)))))

(define (report-prime elapsed-time)
  (display " *** ")
  (display elapsed-time))

; Find the smallest integral divisor (greater than 1)
(define (smallest-divisor n) (find-divisor n 2))

(define (find-divisor n test-divisor)
  (cond ((> (square test-divisor) n) n)
        ((divides? test-divisor n) test-divisor)
        (else (find-divisor n (next test-divisor)))))

(define (divides? a b) (= (remainder b a) 0))

; 跳过除了2以外的偶数
(define (next n)
  (if (= n 2) 3 (+ n 2)))

(define (prime? n)
  (= n (smallest-divisor n)))

; checks the primality of consecutive odd integers in a specified range
; n represent the smallest number we check, count represent the the number of odd integers we need
(define (search-for-primes n count)
  (cond ((and (< count 3) (prime? n)) (and (timed-prime-test n) (search-for-primes (+ n 1) (+ count 1))))
        ((< count 3) (search-for-primes (+ n 1) count))))
      

(search-for-primes 1000000000000000 0)
