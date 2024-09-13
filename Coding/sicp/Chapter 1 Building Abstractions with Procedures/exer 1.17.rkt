#lang racket

(require racket/trace)
(require "../Modules/base.rkt")


(define (multiply-recur a b)
  (cond ((= b 0) 0)
        ((even? b) (multiply-recur (double a) (halve b)))        ; 当b为偶数时，利用ab=2b*b/2
        (else (+ a (multiply-recur a (- b 1))))))                ; 当b为奇数时,利用乘法分配律，ab=a(1+b-1)=a+a(b-1)


(trace multiply-recur)
(multiply-recur 97 99)
