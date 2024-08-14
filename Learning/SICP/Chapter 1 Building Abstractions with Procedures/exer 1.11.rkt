#lang racket
(define (f-recur n)
  (if (< n 3)
      n
      (+ (f-recur (- n 1))
         (* 2 (f-recur (- n 2)))
         (* 3 (f-recur (- n 3))))))

(define (f-iter n)
  (define a 2)
  (define b 1)
  (define c 0)
  (define (iter a b c counter)
    (if (< counter 3)
        a
        (iter (+ a
                 (* 2 b)
                 (* 3 c))
              a
              b
              (- counter 1))))
  (if (< n 3)
      n
      (iter a b c n)))

(f-iter 32)
;(f-recur 32)
