(define (make-vect x y)
  (cons x y))

(define (xcor-vect vector)
  (car vector))

(define (ycor-vect vector)
  (cdr vector))


(define (make-segment v1 v2)
  (cons v1 v2))

(define (start-segment segment)
  (car segment))

(define (end-segment segment)
  (cdr segment))


(define v1 (make-vect 3 4))
(define v2 (make-vect -4 3))
  
(define a-segment (make-segment v1 v2))
a-segment
(start-segment a-segment)
(end-segment a-segment)

