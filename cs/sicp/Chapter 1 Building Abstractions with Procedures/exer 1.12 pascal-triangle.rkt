#lang racket

(define (pascal row col)
  (cond ((or (< row 1) (< col 1) (< row col)) 0)     ; 排除非法参数
        ((or (= col 1) (= row col)) 1)               ; 当该位置在两边时,值都为1
        (else (+ (pascal (- row 1) (- col 1))        ; 其他位置的数都等于上一行“肩膀”2数之和
                 (pascal (- row 1) col)))))


(pascal 5 1)
(pascal 5 2)
(pascal 5 3)
(pascal 5 4)
(pascal 5 5)
