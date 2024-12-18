#lang racket

(provide nil)
(provide pi)
(provide runtime)
(provide square)
(provide cube)
(provide expt)
(provide even?)
(provide double)
(provide halve)
(provide inc)
(provide average)
(provide positive?)
(provide negative?)
(provide sqrt)
(provide put)
(provide get)
(provide put-coercion)
(provide get-coercion)


(define *operation-table* (make-hash))

(define (put op-type op-name procedure)
  (hash-set! *operation-table* (list op-type op-name) procedure))

(define (get op-type op-name)
  (hash-ref *operation-table* (list op-type op-name) #f))

; A function to add a coercion entry to the table
(define (put-coercion type1 type2 fn)
  (hash-set! *operation-table* (list type1 type2) fn))

; A function to get a coercion function from type1 to type2
(define (get-coercion type1 type2)
  (hash-ref *operation-table* (list type1 type2) #f))

(define nil '())

(define pi 3.141592653589793)

; returns a guaranteed-to-increase floating point number which represent the current millisecond count from the system
(define (runtime)
  (current-inexact-milliseconds))

(define (square x)
  (* x x))

(define (cube x)
  (* x x x))

(define (expt b n) 
  (cond ((= n 0) 1) 
        ((even? n) (square (expt b (/ n 2)))) 
        (else (* b (expt b (- n 1)))))) 

(define (even? n)
  (= (remainder n 2) 0))

(define (double a)
  (* a 2))

(define (halve a)
  (/ a 2))

(define (inc a)
  (+ a 1))

(define (average a b)
  (/ (+ a b) 2))

(define (positive? x)
  (if (> x 0) true false))

(define (negative? x)
  (if (< x 0) true false))

(define tolerance 0.00001)

(define (good-enough? guess target tolerance)
  (< (abs (- guess target)) tolerance))

; 注意:这个函数的两个参数以及返回值都是函数,所以调用的语句外还要传一个参数作为 first-guess
(define (iterative-improve good-enough? improve-guess)
  (lambda (first-guess)
    (define (iter guess)
      (if (good-enough? guess)
          guess
          (iter (improve-guess guess))))
    (iter first-guess)))

; Rewrite Version
; 1.1.7 Square Roots by Newton's Method
(define (sqrt x)
  ((iterative-improve (lambda (guess) (good-enough? (square guess) x tolerance))
                      (lambda (guess) (average guess (/ x guess))))
   1.0))
