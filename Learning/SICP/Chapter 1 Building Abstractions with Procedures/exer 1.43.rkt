#lang racket

(require "../modules/base.rkt")

(define (compose f g)
  (lambda (x) (f (g x))))

; f 表示函数，参数只有一个且为数值；n 表示要嵌套执行多少次 f 函数
(define (repeated f n)
  (if (= n 1)
      (lambda (x) (f x))
      (compose f (repeated f (- n 1)))))
      
      
((repeated square 2) 5)
((repeated inc 10) 5)
