#lang racket

(require "../modules/base.rkt")

(define tolerance 0.001)

(define (close-enough? x y tolerance)
  (< (abs (- x y)) tolerance))

(define (fixed-point f first-guess)
  (define (close-enough? v1 v2 tolerance)
    (< (abs (- v1 v2))
       tolerance))
  (define (try guess count)
    (let ((next (f guess)))
      (display count)
      (display " *** ")
      (display guess)
      (newline)
      (if (close-enough? guess next tolerance)
          (and (display (+ count 1))
               (display " *** ")
               (display next))
          (try next (+ count 1)))))
  (try first-guess 1))


; with average damping
(newline)
(display "with average damping")
(newline)
(fixed-point (lambda (x) (average x (/ (log 1000) (log x))))
             1.1)
(newline)

; without average damping
(newline)
(display "without average damping")
(newline)
(fixed-point (lambda (x) (/ (log 1000) (log x)))
             1.1)
