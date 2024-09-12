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

(define (mul-interval x y)
  (let ((p1 (* (lower-bound x) (lower-bound y)))
        (p2 (* (lower-bound x) (upper-bound y)))
        (p3 (* (upper-bound x) (lower-bound y)))
        (p4 (* (upper-bound x) (upper-bound y))))
    (make-interval (min p1 p2 p3 p4)
                   (max p1 p2 p3 p4))))

(define (div-interval x y)
  (if (and (<= (lower-bound y) 0) (>= (upper-bound x) 0))
      (error "被除区间包含0！")
      (mul-interval
       x
       (make-interval (/ 1.0 (upper-bound y))
                      (/ 1.0 (lower-bound y))))))


(define r1 (make-interval 6.12 7.48))
(define r2 (make-interval 4.465 4.935))
(display-interval (div-interval r1 r2))
(newline)

(define a (make-interval 6.12 7.48))
(define b (make-interval -4.465 4.935))
(display-interval (div-interval a b))
