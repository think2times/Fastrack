#lang racket

(require "../modules/base.rkt")


(define (print-point p)
  (newline)
  (display "(")
  (display (x-point p))
  (display ", ")
  (display (y-point p))
  (display ")"))

(define (make-point x y)
  (cons x y))

(define (x-point p) (car p))

(define (y-point p) (cdr p))

(define (make-segment start end)
  (cons start end))

(define (start-segment segment)
  (car segment))

(define (end-segment segment)
  (cdr segment))

; 线段中点坐标就是起点和终点横纵坐标的平均值
(define (midpoint-segment segment)
  (let ((start (start-segment segment))
        (end (end-segment segment)))
    (make-point (average (x-point start) (x-point end))
                (average (y-point start) (y-point end)))))


; 设置线段起点为(3, 5)，终点为(7, 7)，中点应该为(5, 6)
(define start (make-point 3 5))
(define end (make-point 7 7))
(define line (make-segment start end))
(print-point (midpoint-segment line))
