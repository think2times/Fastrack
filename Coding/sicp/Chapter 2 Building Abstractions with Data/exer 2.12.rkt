#lang racket

(require "../Modules/base.rkt")


(define (make-interval a b) (cons a b))

; x 表示某个区间
(define (lower-bound x) (min (car x) (cdr x)))

(define (upper-bound x) (max (car x) (cdr x)))

; 把 w 改为百分比形式
(define (make-center-width center percent)
  (let ((tolerance (* center (/ percent 100))))
    (make-interval (- center tolerance) (+ center tolerance))))

(define (center i)
  (average (lower-bound i) (upper-bound i)))

(define (percent i)
  (* (/ (/ (- (upper-bound i) (lower-bound i)) 2)
        (center i))
     100))

(define (display-interval-tolerance i) 
  (newline)
  (display (center i))
  (display " ± ")
  (display (percent i))
  (display "%"))

(define a (make-interval 6.12 7.48))
(define b (make-interval 4.465 4.935))


(display-interval-tolerance a)
(display-interval-tolerance b)
