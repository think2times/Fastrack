#lang racket
(define (pascal row col)
  (cond ((> col row) 0)
        ((or (= col 1) (= row col)) 1)
        (else (+ (pascal (- row 1) (- col 1))
                 (pascal (- row 1) col)))))

(pascal 5 1)
(pascal 5 3)
(pascal 5 5)
      