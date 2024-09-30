#lang racket

(require "../Modules/base.rkt")


(define (accumulate op initial sequence)
  (if (null? sequence)
      initial
      (op (car sequence)
          (accumulate op initial (cdr sequence)))))

(define (accumulate-n op init seqs)
  (if (null? (car seqs))
      nil
      (cons (accumulate op init (map car seqs))
            (accumulate-n op init (map cdr seqs)))))

; v 和 w 表示的都是向量，且它们的元素的个数相等
(define (dot-product v w)
  (accumulate + 0 (map * v w)))

; m 表示矩阵，v 表示向量，m 的行数必须等于 v 中元素的个数
; 矩阵乘向量，相当于用矩阵的每一行跟向量做点乘
(define (matrix-*-vector m v)
  (map (lambda (x) (dot-product x v)) m))

; mat 表示矩阵
(define (transpose mat)
  (accumulate-n cons nil mat))

; m, n 都表示矩阵，m 的列数必须等于 n 的行数
; 最后的结果矩阵行数等于 m 的行数，列数等于 n 的列数
(define (matrix-*-matrix m n)
  (let ((cols (transpose n)))
    (map (lambda (mat) (matrix-*-vector cols mat)) m)))


(define mat (list (list 1 2 3 4) (list 4 5 6 6) (list 6 7 8 9)))
(define mat2 (list (list 1 2 3 4) (list 4 5 6 6) (list 6 7 8 9) (list 1 2 3 4)))
(define v (list 1 3 3 1))

(dot-product v (list 2 3 5 7))
(matrix-*-vector mat v)
(transpose mat)
(matrix-*-matrix mat mat2)
