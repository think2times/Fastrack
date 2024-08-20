#lang racket

(require "../modules/base.rkt")

(define (timed-prime-test n)
  (newline)
  (display n)
  (start-prime-test n (runtime)))

(define (start-prime-test n start-time)
  (cond ((fast-prime? n 10)
         (report-prime (- (runtime) start-time)))))

(define (report-prime elapsed-time)
  (display " *** ")
  (display elapsed-time))

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

; checking whether the remainder modulo n of the nth power of a is equal to a
(define (fermat-test n)
  (define (try-it a)
    (= (expmod a n n) a))
  (try-it (+ 1 (random (- n 1)))))           ; random returns a nonnegative integer less than its integer input.

; runs the test a given number of times, as specified by a parameter
(define (fast-prime? n times)
  (cond ((= times 0) true)
        ((fermat-test n) (fast-prime? n (- times 1)))
        (else false)))

; checks the primality of consecutive odd integers in a specified range
; n represent the smallest number we check, count represent the the number of odd integers we need
(define (search-for-primes n count)
  (cond ((and (< count 3) (fast-prime? n 10)) (and (timed-prime-test n) (search-for-primes (+ n 1) (+ count 1))))
        ((< count 3) (search-for-primes (+ n 1) count))))
      

(newline)
(search-for-primes 1000 0)
(newline)
(search-for-primes 10000 0)
(newline)
(search-for-primes 100000 0)
(newline)
(search-for-primes 1000000 0)
(newline)