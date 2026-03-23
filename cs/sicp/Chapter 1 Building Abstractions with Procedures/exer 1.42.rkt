#lang racket

(require "../modules/base.rkt")

; f 和 g 表示两个函数，而且都只有一个参数
(define (compose f g)
  (lambda (x) (f (g x))))


((compose square inc) 6)
((compose inc square) 6)
