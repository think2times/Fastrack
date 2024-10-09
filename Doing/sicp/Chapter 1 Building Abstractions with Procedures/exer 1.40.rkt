#lang racket

(require "../modules/base.rkt")

(define tolerance 0.001)

(define (deriv g)
  (lambda (x) (/ (- (g (+ x dx)) (g x)) dx)))

(define dx 0.00001)

(define (newton-transform g)
  (lambda (x) (- x (/ (g x) ((deriv g) x)))))

(define (newtons-method g guess)
  (fixed-point (newton-transform g) guess))

(define (close-enough? x y tolerance)
  (< (abs (- x y)) tolerance))

; Anumberx iscalled a fixed point of a function f if x satisfies the equation f (x) = x.
; For some functions f we can locate a fixed point by beginning with an initial guess and applying f repeatedly,
;  f (x), f (f (x)), f (f (f (x))), . . . , until the value does not change very much.
(define (fixed-point f first-guess)
  (define (close-enough? v1 v2 tolerance)
    (< (abs (- v1 v2))
       tolerance))
  (define (try guess)
    (let ((next (f guess)))
      (if (close-enough? guess next tolerance)
          next
          (try next))))
  (try first-guess))

; 求 x^3 + ax^2 + bx + c = 0 的解
(define (cubic a b c)
  (lambda (x) (+ (cube x)
                 (* a (square x))
                 (* b x)
                 c)))

(newtons-method (cubic 1 1 1)
                1)
