(define wave einstein)

(define (right-split-1 painter n)
  (if (= n 0)
      painter
      (let ((smaller (right-split-1 painter (- n 1))))
        (beside painter (below smaller smaller)))))

(define (up-split-1 painter n)
  (if (= n 0)
      painter
      (let ((smaller (up-split-1 painter (- n 1))))
        (below painter (beside smaller smaller)))))

(define (split op1 op2)
  (define (iter painter n)
    (if (= n 0)
        painter
        (let ((smaller (iter painter (- n 1))))
          (op1 painter (op2 smaller smaller)))))
  iter)

(define right-split-2 (split beside below))
(define up-split-2 (split below beside))


(paint (right-split-1 wave 1))
(paint (right-split-2 wave 1))

(paint (up-split-1 wave 1))
(paint (up-split-2 wave 1))
