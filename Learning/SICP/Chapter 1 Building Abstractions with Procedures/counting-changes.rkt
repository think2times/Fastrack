#lang racket
(define (count-change amount kinds-of-coins)
  (cond ((= amount 0) 1)
        ((< amount 0) 0)
        ((= kinds-of-coins 0) 0)
        (else (+ (count-change amount (- kinds-of-coins 1))
                 (count-change (- amount
                                 (first-denomination kinds-of-coins))
                              kinds-of-coins)))))

(define (first-denomination kinds-of-coins)
  (cond ((= kinds-of-coins 1) 1)
        ((= kinds-of-coins 2) 5)
        ((= kinds-of-coins 3) 10)
        ((= kinds-of-coins 4) 25)
        ((= kinds-of-coins 5) 50)))

(count-change 100 5)
