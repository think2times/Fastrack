#lang racket

(require "../modules/base.rkt")

(define tolerance 0.001)

; The half-interval method for finding roots of an equation f (x) = 0, where f is a continuous function.
; if we are given points a and b such that f (a) < 0 < f (b),
; then f must have at least one zero between a and b.
(define (search f neg-point pos-point)
 (let ((midpoint (average neg-point pos-point)))
   (if (close-enough? neg-point pos-point tolerance)
       midpoint
       (let ((test-value (f midpoint)))
         (cond ((positive? test-value)
                (search f neg-point midpoint))
               ((negative? test-value)
                (search f midpoint pos-point))
               (else midpoint))))))

(define (close-enough? x y tolerance)
  (< (abs (- x y)) tolerance))

; checks to see which of the endpoints has a negative function value and which has a positive value,
; and calls the search procedure accordingly.
; If the function has the same sign on the two given points,
; the half-interval method cannot be used, in which case the procedure signals an error.
(define (half-interval-method f a b)
  (let ((a-value (f a))
        (b-value (f b)))
    (cond ((and (negative? a-value) (positive? b-value))
           (search f a b))
          ((and (negative? b-value) (positive? a-value))
           (search f b a))
          (else
           (error "Values are not of opposite sign" a b)))))

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

(define (sqrt x)
  (fixed-point (lambda (y) (average y (/ x y)))
               1.0))


(half-interval-method sin 2.0 4.0)
(half-interval-method (lambda (x) (- (* x x x) (* 2 x) 3))
                      1.0
                      2.0)

(fixed-point cos 1.0)
(fixed-point (lambda (x) (+ (sin x) (cos x))) 1.0)

(sqrt 10)
