#lang racket

(require "../Modules/base.rkt")


(define (enumerate-interval low high)
  (if (> low high)
      nil
      (cons low (enumerate-interval (+ low 1) high))))

(define (accumulate op initial sequence)
  (if (null? sequence)
      initial
      (op (car sequence)
          (accumulate op initial (cdr sequence)))))

(define (flatmap proc seq)
  (accumulate append nil (map proc seq)))

; board-size 指的是正方形棋盘的长
(define (queens board-size)
  (define (queen-cols k)
    (if (= k 0)
        (list empty-board)
        (filter
         (lambda (positions) (safe? k positions))     ; 每组位置不冲突的皇后的位置构成一个位置的集合
         (flatmap
          (lambda (rest-of-queens)         ; rest-of-queens 表示已经被放置在安全位置的 k-1 个王后的位置的组合
            (map (lambda (new-row)
                   (adjoin-position new-row k rest-of-queens))
                 (enumerate-interval 1 board-size)))             ; 把第 k 列的新位置加进之前的王后的位置组合
          (queen-cols (- k 1))))))
  (queen-cols board-size))

(define empty-board nil)

; 检查2个位置坐标是否冲突
; 同行比较好判断,只要新王后位置的行跟前 k-1 个王后的行都不同就行,同列同理
; 对角线比较复杂,分为从左上到右下和从左下到右上两类
; 从左上到右下,在同一条对角线上的坐标,行与列坐标之差相同
; 从左下到右上,在同一条对角线上的坐标,行与列坐标之和相同
(define (check pos1 pos2)
  (let ((x1 (car pos1))
        (y1 (cadr pos1))
        (x2 (car pos2))
        (y2 (cadr pos2)))
    (and (not (= x1 x2))
         (not (= y1 y2))
         (not (= (- x1 x2) (- y1 y2)))
         (not (= (+ x1 x2) (+ y1 y2))))))

; 检查新加入的王后的位置与其他王后的位置是否冲突
; k 其实没有任何作用
(define (safe? k positions)
  (let ((new-queen (car positions))
        (rest-of-queens (cdr positions)))
    (accumulate (lambda (pos result)
                  (and (check pos new-queen)
                       result))
                true
                rest-of-queens)))
         
; 在已有前 k-1 个王后的位置组合的基础上，把某个位置坐标(row col)加到第一个位置
(define (adjoin-position row col rest-of-queens)
  (cons (list row col) rest-of-queens))
 

(queens 1)
(queens 2)
(queens 3)
(queens 4)
(queens 8)
