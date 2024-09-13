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

; 把 w 改为百分比形式
(define (make-center-width c w)
  (let ((tolerance (* c w)))
    (make-interval (- c tolerance) (+ c tolerance))))

(define (center i)
  (average (lower-bound i) (upper-bound i)))

(define (width i)
  (* (/ (/ (- (upper-bound i) (lower-bound i)) 2)
        (center i))
     100))

(define (display-interval-tolerance i) 
  (newline)
  (display (center i))
  (display " ± ")
  (display (width i))
  (display "%"))

; 记 x 的下界为 x1，上界为 x2；记 y 的下界为 y1，上界为 y2
; 将他们按 x1 x2 y1 y2 从左到右排序，并按位置记为 1, 2, 3, 4
; 则按照 x 和 y 的区间端点数字的符号，可以分成以下9种情况：
; - - - -   min: 2*4, max: 1*3
; - - - +   min: 1*4, max: 1*3
; - - + +   min: 1*4, max: 2*3
; - + - -   min: 2*3, max: 1*3
; - + - +   min: min(1*4, 2*3), max: max(1*3, 2*4)
; - + + +   min: 1*4, max: 2*4
; + + - -   min: 2*3, max: 1*4
; + + - +   min: 2*3, max: 2*4
; + + + +   min: 1*3, max: 2*4
(define (mul-interval x y)
  (let ((x1 (lower-bound x))
        (x2 (upper-bound x))
        (y1 (lower-bound y))
        (y2 (upper-bound y))
        (p1 (* (lower-bound x) (lower-bound y)))    ; 即 1*3
        (p2 (* (lower-bound x) (upper-bound y)))    ; 即 1*4
        (p3 (* (upper-bound x) (lower-bound y)))    ; 即 2*3
        (p4 (* (upper-bound x) (upper-bound y))))   ; 即 2*4
    (cond ((and (negative? x2) (negative? y2)) (make-interval p4 p1))
          ((and (negative? x2) (negative? y1) (positive? y2)) (make-interval p2 p1))
          ((and (negative? x2) (positive? y1)) (make-interval p2 p3))
          ((and (negative? x1) (positive? x2) (negative? y2)) (make-interval p3 p1))
          ((and (negative? x1) (positive? x2) (negative? y1) (positive? y2)) (make-interval (min p2 p3) (max p1 p4)))
          ((and (negative? x1) (positive? x2) (positive? y1)) (make-interval p2 p4))
          ((and (positive? x1) (negative? y2)) (make-interval p3 p2))
          ((and (positive? x1) (negative? y1) (positive? y2)) (make-interval p3 p4))
          ((and (positive? x1) (positive? y1)) (make-interval p1 p4)))))


(define a (make-interval -6.12 7.48))
(define b (make-interval -4.465 4.935))
(display-interval (mul-interval a b))
(display-interval-tolerance (mul-interval a b))
