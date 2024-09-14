#lang racket

(require "../Modules/base.rkt")


(define (make-interval a b) (cons a b))

; x 表示某个区间
(define (lower-bound x) (min (car x) (cdr x)))

(define (upper-bound x) (max (car x) (cdr x)))

; 把 w 改为百分比形式
(define (make-center-width c w)
  (let ((tolerance (* c w)))
    (make-interval (- c tolerance) (+ c tolerance))))

(define (center i)
  (average (lower-bound i) (upper-bound i)))

(define (percent i)
  (* (/ (/ (- (upper-bound i) (lower-bound i)) 2)
        (center i))
     100))

(define (add-interval x y)
  (make-interval (+ (lower-bound x) (lower-bound y))
                 (+ (upper-bound x) (upper-bound y))))

; 计算 x-y 的结果
(define (sub-interval x y)
  (make-interval (- (lower-bound x) (upper-bound y))
                 (- (upper-bound x) (lower-bound y))))

(define (mul-interval x y)
  (let ((cx (center x))
        (cy (center y))
        (px (/ (percent x) 100))
        (py (/ (percent y) 100)))
    (make-interval (* (- cx (* cx px)) (- cy (* cy py)))
                   (* (+ cx (* cx px)) (+ cy (* cy py))))))

(define (div-interval x y)
  (if (and (<= (lower-bound y) 0) (>= (upper-bound y) 0))
      (error "被除区间包含0!")
      (mul-interval
       x
       (make-interval (/ 1.0 (upper-bound y))
                      (/ 1.0 (lower-bound y))))))

(define (display-interval-tolerance i) 
  (newline)
  (display (center i))
  (display " ± ")
  (display (percent i))
  (display "%"))

(define (par1 r1 r2)
  (div-interval (mul-interval r1 r2)
                (add-interval r1 r2)))

(define (par2 r1 r2)
  (let ((one (make-interval 1 1)))
    (div-interval one (add-interval (div-interval one r1)
                                    (div-interval one r2)))))


(define r1 (make-interval 6.12 7.48))
(define r2 (make-interval 4.465 4.935))

(display-interval-tolerance (par1 r1 r2))
(display-interval-tolerance (par2 r1 r2))
