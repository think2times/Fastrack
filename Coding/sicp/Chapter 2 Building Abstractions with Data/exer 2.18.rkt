#lang racket


(require "../Modules/base.rkt")

; List operations
(define (list-ref items n)
  (let ((len (length items)))
    (cond ((>= n len) (error "查找的下标超出了列表中元素的个数!"))
          ((= n 0) (car items))
          (else (list-ref (cdr items) (- n 1))))))

(define (length items)
  (define (iter items count)
    (if (null? items)
        count
        (iter (cdr items) (+ 1 count))))
  (iter items 0))

(define (reverse items) 
  (define (iter items result) 
    (if (null? items) 
        result 
        (iter (cdr items) (cons (car items) result)))) 
  
  (iter items nil)) 
  
  
(reverse (list 1 4 9 16 25))
