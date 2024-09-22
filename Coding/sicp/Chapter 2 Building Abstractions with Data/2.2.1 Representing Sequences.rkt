#lang racket

(require "../Modules/base.rkt")


(define one-through-four (list 1 2 3 4))

one-through-four
(car one-through-four)
(cdr one-through-four)

(cons 10 one-through-four)


; List operations
(define (list-ref items n)
  (let ((len (length items)))
    (cond ((>= n len) (error "查找的下标超出了列表中元素的个数！"))
          ((= n 0) (car items))
          (else (list-ref (cdr items) (- n 1))))))

(define (length-recur items)
  (if (null? items)
      0
      (+ 1 (length-recur (cdr items)))))

(define (length-iter items)
  (define (iter items count)
    (if (null? items)
        count
        (iter (cdr items) (+ 1 count))))
  (iter items 0))

(define (append list1 list2)
  (if (null? list1)
      list2
      (cons (car list1)
            (append (cdr list1) list2))))

(define squares (list 1 4 9 16 25))
(define odds (list 1 3 5 7 9 11))

(list-ref squares 0)
(list-ref squares 3)
(list-ref squares 4)

(length-iter squares)

(length-recur odds)

(append odds squares)
(append squares odds)


; Mapping over lists
(define (scale-list items factor)
  (if (null? items)
      nil
      (cons (* (car items) factor)
            (scale-list (cdr items)
                        factor))))

(define (map proc items)
  (if (null? items)
      nil
      (cons (proc (car items))
            (map proc (cdr items)))))
            
(define (scale-list-by-map items factor)
  (map (lambda (x) (* x factor))
       items))


(scale-list (list 1 2 3 4 5) 10)
(scale-list-by-map (list 1 2 3 4 5) 10)
