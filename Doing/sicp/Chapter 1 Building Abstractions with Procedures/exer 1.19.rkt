#lang racket

(require racket/trace)
(require "../Modules/base.rkt")


(define (fib n)
  (fib-iter 1 0 0 1 n))
(define (fib-iter a b p q count)
  (cond ((= count 0) b)
        ((even? count)
         ; count为偶数且不为0时，可以连续进行两次转换
         ; 通过简单的代数计算和化简，可以得到经过两次转换后
         ; a = b(q^2+2pq) + a(q^2+2pq) + a(p^2+q^2)
         ; b = b(p^2+q^2) + a(q^2+2pq)
         ; 所以 q' = (q^2+2pq), p' = (p^2+q^2)
         (fib-iter a
                   b
                   (+ (square p) (square q))
                   (+ (square q) (* 2 p q))
                   (/ count 2)))
         (else (fib-iter (+ (* b q) (* a q) (* a p))
                         (+ (* b p) (* a q))
                         p
                         q
                         (- count 1)))))


(trace fib-iter)
(fib 10)

(trace fib-iter)
(fib 20)

(trace fib-iter)
(fib 40)

(trace fib-iter)
(fib 80)

(trace fib-iter)
(fib 160)
