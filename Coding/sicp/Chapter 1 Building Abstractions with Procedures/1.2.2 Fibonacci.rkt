#lang racket
(define (fibonacci n)
  ; 递归写法
  (define (fib-recur n)
    (cond ((= n 0) 0)
          ((= n 1) 1)
          (else (+ (fib-recur (- n 1))
                   (fib-recur (- n 2))))))

  ; 迭代写法
  (define (fib-iter n)
    (define a 0)
    (define b 1)
    (define (iter a b counter)
      (if (= counter 0)
          a
          (iter b
                (+ a b)
                (- counter 1))))

    (iter a b n))

  (fib-iter n))

(fibonacci 40)