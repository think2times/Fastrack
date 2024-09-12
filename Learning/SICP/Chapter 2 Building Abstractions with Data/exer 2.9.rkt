#lang racket

(require "../Modules/base.rkt")


(define (make-interval a b) (cons a b))

; x 表示某个区间
(define (lower-bound x) (min (car x) (cdr x)))

(define (upper-bound x) (max (car x) (cdr x)))

(define (display-interval i) 
  (newline) 
  (display "[") 
  (display (lower-bound i)) 
  (display ", ") 
  (display (upper-bound i)) 
  (display "]"))

(define (add-interval x y)
  (make-interval (+ (lower-bound x) (lower-bound y))
                 (+ (upper-bound x) (upper-bound y))))

; 计算 x-y 的结果
(define (sub-interval x y)
  (make-interval (- (lower-bound x) (upper-bound y))
                 (- (upper-bound x) (lower-bound y))))

; 计算区间的宽度
(define (get-width x)
  (/ (- (upper-bound x) (lower-bound x)) 2))


(define r1 (make-interval 6.12 7.48))
(define r2 (make-interval 4.465 4.935))

(display (get-width r1))
(newline)
(display (get-width r2))
(newline)
(display (get-width (add-interval r1 r2)))
(newline)
(display (get-width (sub-interval r1 r2)))
(newline)
