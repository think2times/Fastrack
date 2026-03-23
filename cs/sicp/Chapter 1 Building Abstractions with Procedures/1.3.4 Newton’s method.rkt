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

(define (fixed-point-of-transform g transform guess)
  (fixed-point (transform g) guess))

(define (average-damp f)
  (lambda (x) (average x (f x))))

(define (sqrt1 x)
  (fixed-point-of-transform (lambda (y) (/ x y))
                            average-damp
                            1.0))

(define (sqrt2 x)
  (fixed-point-of-transform (lambda (y) (- (square y) x))
                            newton-transform
                            1.0))
                            

((deriv cube) 5)

(sqrt2 5)
