(define (make-vect x y)
  (cons x y))

(define (xcor-vect vector)
  (car vector))

(define (ycor-vect vector)
  (cdr vector))

(define (add-vect v1 v2)
  (make-vect (+ (xcor-vect v1)
                (xcor-vect v2))
             (+ (ycor-vect v1)
                (ycor-vect v2))))

(define (sub-vect v1 v2)
  (make-vect (- (xcor-vect v1)
                (xcor-vect v2))
             (- (ycor-vect v1)
                (ycor-vect v2))))

(define (scale-vect s v)
  (make-vect (* s (xcor-vect v))
             (* s (ycor-vect v))))


(define (make-frame-by-list origin edge1 edge2)
  (list origin edge1 edge2))

(define (origin-frame-by-list frame)
  (car frame))

(define (edge1-frame-by-list frame)
  (cadr frame))

(define (edge2-frame-by-list frame)
  (caddr frame))

(define (make-frame-by-cons origin edge1 edge2)
  (cons origin (cons edge1 edge2)))

(define (origin-frame-by-cons frame)
  (car frame))

(define (edge1-frame-by-cons frame)
  (cadr frame))

(define (edge2-frame-by-cons frame)
  (cddr frame))


(define origin (make-vect 1 1))
(define v1 (make-vect 3 4))
(define v2 (make-vect -4 3))

(define frame1 (make-frame-by-list origin v1 v2))
(origin-frame-by-list frame1)
(edge1-frame-by-list frame1)
(edge2-frame-by-list frame1)

(define frame2 (make-frame-by-cons origin v1 v2))
(origin-frame-by-cons frame2)
(edge1-frame-by-cons frame2)
(edge2-frame-by-cons frame2)
