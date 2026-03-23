#lang racket

(require "../modules/base.rkt")

(define (close-enough? x y tolerance)
  (< (abs (- x y)) tolerance))

; 黄金分割比例是 φ = (1+√5)/2,倒数 1/φ ≈ 0.61803398875
; 保留4位有效数字就是 0.6180,所以结果需要在 0.6175 ~ 0.6184 之间
; 取 0.6175 和 0.6184 的中间值 0.61795,只要与其差值不大于 0.00045 即可
(define tolerance 0.00045)
(define midterm 0.61795)

; 注意 n 和 d 都是 procedure 而不是数字，k 表示要计算的项数
; 他们都是常数函数，接受一个参数 i，但是无论 i 是多少，都返回 1.0
(define (cont-frac n d k)
  ; iterative implementation
  (define (frac-iter k pre)
    (if (= k 1)
        pre
        (frac-iter (- k 1) (/ (n k) (+ (d k) pre)))))

  ; recurative implementation
  (define (frac-recur k)
    (if (= k 1)
        (/ (n k) (d k))
        (/ (n k) (+ (d k) (frac-recur (- k 1))))))

  ; 找到满足要求的最小k值
  (define (find k)
    ;(let ((temp (frac-iter k 1.0)))
    (let ((temp (frac-recur k)))
      (if (close-enough? temp midterm tolerance)
          (and (display k)
               (display " *** ")
               (display temp))
          (find (+ k 1)))))

  (find 1))


(cont-frac (lambda (i) 1.0)
           (lambda (i) 1.0)
           10)
