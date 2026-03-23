#lang racket


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

; 计算 x-y 的结果
(define (sub-interval x y)
  (make-interval (- (lower-bound x) (upper-bound y))
                 (- (upper-bound x) (lower-bound y))))


(define r1 (make-interval 6.12 7.48))
(define r2 (make-interval 4.465 4.935))

(display-interval (sub-interval r1 r2))
