#lang racket

(require "../Modules/base.rkt")

(define epsilon (expt 2 -52))

(define (sqrt x)
  (define (sqrt-iter guess)
    (if (good-enough-3? guess)
        guess
        (sqrt-iter (improve guess))))
  (define (improve guess)
    (/ (+ guess (/ x guess)) 2))
  #|
  1. The initial strategy is to stop the improvement of the guess when the absolute error of the guess is less than a constant tolerance.
     For small radicands, the result is not accurate because the tolerance is not scaled down to the small radicands.
     For large radicands, the procedure sqrt-iter enters an infinite recursion because the tolerance is not scaled up to the large radicands
     and floating-point numbers are represented with limited precision so the absolute error at that scale is always greater than the tolerance.
     The problem observed for large radicands can also be observed for small radicands, providing that the tolerance is chosen
     so that the absolute error at that scale is always greater than the tolerance.
  |#
  (define (good-enough-1? guess)
    (define tolerance 1.0)
    (< (abs (- (square guess) x)) tolerance))
  #|
  2. An alternative strategy is to stop the improvement of the guess when the absolute error of the guess is less than a variable tolerance scaled to the radicand,
     in other words when the relative error of the guess is less than a constant tolerance.
  |#
  (define (good-enough-2? guess)
    (define min-float (expt 2 -1022))
    (define tolerance (* (/ 3 2) epsilon))
    (< (abs (- (square guess) x)) (if (= x 0) min-float (* tolerance x))))
  #|
  3. Another alternative strategy is to stop the improvement of the guess when the absolute change of the guess is less than a variable tolerance scaled to the guess,
     in other words when the relative change of the guess is less than a constant tolerance.
  |#
  (define (good-enough-3? guess)
    (define tolerance (* (/ 9 4) epsilon))
    (or (= guess 0) (< (abs (- (improve guess) guess)) (* tolerance guess))))

  (define initial-guess 1.0)
  (sqrt-iter initial-guess))


(sqrt 0.0000000000001)
(sqrt 900000000000000)
