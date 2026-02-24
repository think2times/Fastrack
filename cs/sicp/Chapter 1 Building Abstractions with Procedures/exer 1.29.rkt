#lang racket

(require "../modules/base.rkt")

; template of "summation according to Simpson’s Rule".
(define (simpson-sum term a next b n)
  ; 由于n取得是偶数，所以得到的factor会是2, 4, 2, 4, ... , 1
  ; 与Simpson’s Rule相比，第一项加了2遍，最后需要把第一项减掉一次
  (define factor (cond ((= n 0) 1)
                       ((even? n) 2)
                       (else 4)))
  (if (> a b)
      0
      (+ (* factor (term a))
         (simpson-sum term (next a) next b (- n 1)))))


(define (integral f a b n)
  (define h (/ (- b a) n))
  (define (integral-next x)
    (+ x h))
  (* (/ h 3.0)
     ; 把第一项减掉一次
     (- (simpson-sum f a integral-next b n) (f a))))


(integral cube 0 1 100)
(integral cube 0 1 1000)
