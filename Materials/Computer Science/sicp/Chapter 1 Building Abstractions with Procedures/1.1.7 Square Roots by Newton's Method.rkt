#lang racket

(require "../Modules/base.rkt")

; 牛顿法求一个数的算术平方根
(define (sqrt x)
  (define (sqrt-iter guess)
    (if (good-enough? guess)
        guess
        (sqrt-iter (improve guess))))

  ; 把x除以这个猜测值的结果与猜测值的平均值作为新的猜测值
  (define (improve guess)
    (/ (+ guess (/ x guess))
       2))

  ; 把猜测值的平方与所求值之差的绝对值与设定的误差允许范围进行比较
  (define (good-enough? guess)
    (< (abs (- (square guess) x))
       0.0001))

  ; 把1.0作为猜测值，注意如果设为1的话，算出的结果为分数
  (sqrt-iter 1.0))


(sqrt 0.01)
(sqrt 9000000000)
(sqrt 137)
(sqrt (+ (sqrt 2) (sqrt 3)))
(square (sqrt 1000))
