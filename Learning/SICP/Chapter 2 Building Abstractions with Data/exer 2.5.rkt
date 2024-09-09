#lang racket

(require "../modules/base.rkt")

; 计算 n 中最多包含几个 base 的积
(define (get-power n base)
  (define (iter k last)
    (if (= (remainder last base) 0)      ; 如果余数为0，说明能够被base整除，则次数 +1
        (iter (+ k 1) (/ last base))
        k))
  (iter 0 n))

(define (cons a b)
  (* (expt 2 a) (expt 3 b)))

(define (car z)
  (get-power z 2))

(define (cdr z)
  (get-power z 3))


(define p (cons 3 2))
(display p)
(newline)
(car p)
(cdr p)
