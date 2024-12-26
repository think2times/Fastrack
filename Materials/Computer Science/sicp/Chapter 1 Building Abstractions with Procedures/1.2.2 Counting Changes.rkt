#lang racket
(define (count-change amount kinds-of-coins)
  (cond ((= amount 0) 1)
        ((or (< amount 0)
             (= kinds-of-coins 0) 0))
        (else (+ (count-change amount (- kinds-of-coins 1))     ; 用除了第一种面额以外的其他硬币进行兑换
                 (count-change (- amount                        ; 用所有类型的硬币兑换剩下的钱（amount-第一种硬币的面额）
                                 (first-denomination kinds-of-coins))
                              kinds-of-coins)))))

; 设定可用来兑换的硬币的面额
(define (first-denomination kinds-of-coins)
  (cond ((= kinds-of-coins 1) 1)
        ((= kinds-of-coins 2) 5)
        ((= kinds-of-coins 3) 10)
        ((= kinds-of-coins 4) 25)
        ((= kinds-of-coins 5) 50)))

(count-change 100 5)
