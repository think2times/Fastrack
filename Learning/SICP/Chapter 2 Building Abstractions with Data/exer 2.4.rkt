#lang racket


; 返回值是一个单参数的函数，它会把 cons 函数的两个数传给返回值函数
(define (cons x y)
  (lambda (m) (m x y)))

; 如果 z 是由 cons 函数创建的数据对，则 z 会把 (lambda (p q) p)) 作为参数
(define (car z)
  (z (lambda (p q) p)))

(define (cdr z)
  (z (lambda (p q) q)))


(define z (cons 3 4)) 
(car z) 
(cdr z) 

; applicative-order
; (car (cons x y)) 
; (car (lambda (m) (m x y))) 
; ((lambda (m) (m x y)) (lambda (p q) p)) 
; ((lambda (p q) p) x y) 
; x 
