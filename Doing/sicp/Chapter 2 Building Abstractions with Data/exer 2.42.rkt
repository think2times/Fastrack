#lang racket

(require "../Modules/base.rkt")


; board-size 指的是正方形棋盘的长
(define (queens board-size)
  (define (queen-cols k)
    (if (= k 0)
        (list empty-board)
        (filter
         (lambda (positions) (safe? k positions))
         (flatmap
          (lambda (rest-of-queens)         ; 已经被放置在安全位置的 k-1 个王后
            (map (lambda (new-row)
                   (adjoin-position
                    new-row k rest-of-queens))
                 (enumerate-interval 1 board-size)))
          (queen-cols (- k 1))))))
  (queen-cols board-size))

(define empty-board nil)

; 只保留第 k 行和 第 k 列跟前 k-1 个王后不冲突的位置
; 同行比较好判断，只要新王后位置的行跟前 k-1 个王后的行都不同就行，同列同理
; 对角线比较复杂，分为从左上到右下和从左下到右上两类
; 从左上到右下也比较简单，在同一条对角线上的坐标，行与列坐标之差相同
; 从左下到右上的对角线上的坐标，他们的行坐标之和与列坐标之和相同(或所有位置的行与列坐标之差的和为0)
(define (safe? k positions)
  (= k positions))

; 在已有前 k-1 个王后的位置组合的基础上，把第 k 行和第 k 列加进来
(define (adjoin-position new-row k rest-of-queens)
  

(queens 8)
