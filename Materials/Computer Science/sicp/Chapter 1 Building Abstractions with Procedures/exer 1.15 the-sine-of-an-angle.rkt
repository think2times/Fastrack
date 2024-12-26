#lang racket

(require racket/trace)
(require "../Modules/base.rkt")


(define (p x) (- (* 3 x) (* 4 (cube x))))

(define (sine angle)
    (if (not (> (abs angle) 0.1))
        angle
        (p (sine (/ angle 3.0)))))


(trace sine)
(trace p)
(sine 12.15)