#lang racket
(define (factorial n)
  ; 1. 直接递归调用自身
  (define (factorial-recursion n)
    (if (= n 0)
        1
        (* n (factorial-recursion (- n 1)))))

  ; 2. 存放上一步计算结果
  (define (factorial-iter counter product)
    (if (> counter n)
        product
        (factorial-iter (+ counter 1)
                        (* product counter))))

  ; 选择不同的算法计算阶乘
  ; 面对100000就无能为力了
  ;(factorial-recursion n))
  ; 计算100000的阶乘没啥压力
  (factorial-iter 1 1))

(factorial 6)