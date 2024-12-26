#lang racket

(require "../modules/base.rkt")

(define tolerance 0.00001)

(define (close-enough? x y tolerance)
  (< (abs (- x y)) tolerance))

; Anumberx iscalled a fixed point of a function f if x satisfies the equation f (x) = x.
; For some functions f we can locate a fixed point by beginning with an initial guess and applying f repeatedly,
;  f (x), f (f (x)), f (f (f (x))), . . . , until the value does not change very much.
(define (fixed-point f first-guess)
  (define (close-enough? v1 v2 tolerance)
    (< (abs (- v1 v2))
       tolerance))
  (define (try guess)
    (let ((next (f guess)))
      (if (close-enough? guess next tolerance)
          next
          (try next))))
  (try first-guess))

(define (compose f g)
  (lambda (x) (f (g x))))

; f 表示函数,参数只有一个且为数值;n 表示要嵌套执行多少次 f 函数
(define (repeated f n)
  (if (= n 1)
      f
      (compose f (repeated f (- n 1)))))

; 求 x 和 f(x) 的平均值
(define (average-damp f)
  (lambda (x) (average x (f x))))

; 对于任意正整数 n，求使得 2^k < n 的最大 k 值
(define (max-expt n)
  (define (iter k pre)
    (if (< n pre)
        (- k 1)
        (iter (+ k 1) (* 2 pre))))
  (iter 1 2))

(define (nth-root x n)
  (fixed-point ((repeated average-damp (max-expt n))
                (lambda (y) (/ x (expt y (- n 1)))))
               1.0))


(display (nth-root 2 2))
(newline)
(display (nth-root 32 5))
(newline)
