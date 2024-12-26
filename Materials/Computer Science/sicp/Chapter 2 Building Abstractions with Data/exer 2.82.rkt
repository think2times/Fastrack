#lang racket

(require "../Modules/base.rkt")


(define (attach-tag type-tag contents)
  (cons type-tag contents))

(define (type-tag datum)
  (if (pair? datum)
      (car datum)
      (error "Bad tagged datum: TYPE-TAG" datum)))

(define (contents datum)
  (if (pair? datum)
      (cdr datum)
      (error "Bad tagged datum: CONTENTS" datum)))

(define (apply-generic op . args) 
  (define (no-method type-tags) 
    (error "No method for these types" 
           (list op type-tags)))
  
  (define (type-tags args) 
         (map type-tag args))

  ; 对每一个参数尝试进行强制类型转换
  (define (try-coerce-to target)
    (map (lambda (origin)
           (if (eq? (type-tag origin) (type-tag target))
               (lambda (x) x)   ; 如果类型一致，不进行转换
               (let ((coercor (get-coercion (type-tag origin) (type-tag target)))) 
                 (if coercor 
                     (coercor origin) 
                     origin)))) 
           args))
  
  (define (iterate next) 
    (if (null? next)
        (no-method (type-tags args)) 
        (let ((coerced (try-coerce-to (car next)))) 
          (let ((proc (get op (type-tags coerced)))) 
            (if proc 
                (apply proc (map contents coerced)) 
                (iterate (cdr next))))))) 
  
  (let ((proc (get op (type-tags args)))) 
    (if proc 
        (apply proc (map contents args)) 
        (iterate args))))
