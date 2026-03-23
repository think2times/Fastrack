#lang racket

(require "../modules/base.rkt")

(define (compose f g)
  (lambda (x) (f (g x))))

; f 表示函数,参数只有一个且为数值;n 表示要嵌套执行多少次 f 函数
(define (repeated f n)
  (if (= n 1)
      (lambda (x) (f x))
      (compose f (repeated f (- n 1)))))

(define dx 0.0001)
(define (smooth f)
  (lambda (x) (/ (+ (f (- x dx))
                    (f x)
                    (f (+ x dx)))
                 3)))

(define (n-fold-smooth f n)
  (repeated f n))


((smooth square) 5)
((smooth inc) 5)

((n-fold-smooth square 2) 5)
((n-fold-smooth inc 10) 5)
