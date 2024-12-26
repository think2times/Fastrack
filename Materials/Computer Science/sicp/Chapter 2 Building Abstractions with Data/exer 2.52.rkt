(#%require sicp-pict)


(define wave 
  (segments->painter (list 
                      (segment (vect .25 0) (vect .35 .5)) 
                      (segment (vect .35 .5) (vect .3 .6)) 
                      (segment (vect .3 .6) (vect .15 .4)) 
                      (segment (vect .15 .4) (vect 0 .65)) 
                      (segment (vect 0 .65) (vect 0 .85)) 
                      (segment (vect 0 .85) (vect .15 .6)) 
                      (segment (vect .15 .6) (vect .3 .65)) 
                      (segment (vect .3 .65) (vect .4 .65)) 
                      (segment (vect .4 .65) (vect .35 .85)) 
                      (segment (vect .35 .85) (vect .4 1)) 
                      (segment (vect .4 1) (vect .6 1)) 
                      (segment (vect .6 1) (vect .65 .85)) 
                      (segment (vect .65 .85) (vect .6 .65)) 
                      (segment (vect .6 .65) (vect .75 .65)) 
                      (segment (vect .75 .65) (vect 1 .35)) 
                      (segment (vect 1 .35) (vect 1 .15)) 
                      (segment (vect 1 .15) (vect .6 .45)) 
                      (segment (vect .6 .45) (vect .75 0)) 
                      (segment (vect .75 0) (vect .6 0)) 
                      (segment (vect .6 0) (vect .5 .3)) 
                      (segment (vect .5 .3) (vect .4 0)) 
                      (segment (vect .4 0) (vect .25 0)) 
                      )))

(define (right-split painter n)
  (if (= n 0)
      painter
      (let ((smaller (right-split painter (- n 1))))
        (beside painter (below smaller smaller)))))

(define (up-split painter n)
  (if (= n 0)
      painter
      (let ((smaller (up-split painter (- n 1))))
        (beside painter (below smaller smaller)))))

; a
(define wave-with-smile
  (segments->painter (list 
                      (segment (vect .25 0) (vect .35 .5)) 
                      (segment (vect .35 .5) (vect .3 .6)) 
                      (segment (vect .3 .6) (vect .15 .4)) 
                      (segment (vect .15 .4) (vect 0 .65)) 
                      (segment (vect 0 .65) (vect 0 .85)) 
                      (segment (vect 0 .85) (vect .15 .6)) 
                      (segment (vect .15 .6) (vect .3 .65)) 
                      (segment (vect .3 .65) (vect .4 .65)) 
                      (segment (vect .4 .65) (vect .35 .85))
                      (segment (vect .35 .85) (vect .4 1))
                      (segment (vect .4 1) (vect .6 1)) 
                      (segment (vect .6 1) (vect .65 .85))
                      (segment (vect .65 .85) (vect .6 .65)) 
                      (segment (vect .6 .65) (vect .75 .65)) 
                      (segment (vect .75 .65) (vect 1 .35)) 
                      (segment (vect 1 .35) (vect 1 .15)) 
                      (segment (vect 1 .15) (vect .6 .45)) 
                      (segment (vect .6 .45) (vect .75 0)) 
                      (segment (vect .75 0) (vect .6 0)) 
                      (segment (vect .6 0) (vect .5 .3)) 
                      (segment (vect .5 .3) (vect .4 0)) 
                      (segment (vect .4 0) (vect .25 0))
                      (segment (vect .45 .76) (vect .5 0.72))
                      (segment (vect .5 0.72) (vect .55 .76))
                      )))

(paint wave-with-smile)


(define (corner-split painter n)
  (if (= n 0)
      painter
      (let ((up (up-split painter (- n 1)))
            (right (right-split painter (- n 1))))
        (let ((top-left up)
              (bottom-right (below right right))
              (corner (corner-split painter (- n 1))))
          (beside (below painter top-left)
                  (below bottom-right corner))))))

(paint (corner-split wave-with-smile 1))

(define (square-of-four tl tr bl br)
  (lambda (painter)
    (let ((top (beside (tl painter) (tr painter)))
          (bottom (beside (bl painter) (br painter))))
      (below bottom top))))

(define (square-limit painter n)
  (let ((combine4 (square-of-four flip-vert rotate180
                                  identity flip-horiz)))
    (combine4 (corner-split painter n))))

(paint (square-limit wave-with-smile 1))
