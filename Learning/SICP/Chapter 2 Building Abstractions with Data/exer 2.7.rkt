#lang racket


(define (add-interval x y)
  (make-interval (+ (lower-bound x) (lower-bound y))
                 (+ (upper-bound x) (upper-bound y))))

(define (mul-interval x y)
  (let ((p1 (* (lower-bound x) (lower-bound y)))
        (p2 (* (lower-bound x) (upper-bound y)))
        (p3 (* (upper-bound x) (lower-bound y)))
        (p4 (* (upper-bound x) (upper-bound y))))
    (make-interval (min p1 p2 p3 p4)
                   (max p1 p2 p3 p4))))

(define (div-interval x y)
  (mul-interval
   x
   (make-interval (/ 1.0 (upper-bound y))
                  (/ 1.0 (lower-bound y)))))

(define (make-interval a b) (cons a b))

; x 表示某个区间
(define (lower-bound x) (min (car x) (cdr x)))

(define (upper-bound x) (max (car x) (cdr x)))

(define helper (make-interval 1.0 1.0))
(define r1 (make-interval 6.12 7.48))
(define r2 (make-interval 4.465 4.935))

; 计算并联电路的电阻，注意这里不能化简成 r1*r2/(r1+r2) 的形式
(define (parallel-resistance r1 r2)
  (div-interval helper (add-interval (div-interval helper r1)
                                     (div-interval helper r2))))

(define (display-interval i) 
  (newline) 
  (display "[") 
  (display (lower-bound i)) 
  (display ", ") 
  (display (upper-bound i)) 
  (display "]"))

(display-interval (parallel-resistance r1 r2))
