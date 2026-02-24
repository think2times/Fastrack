(#%require sicp-pict)


; a 
(define outline 
  (segments->painter 
   (list 
    (segment (vect 0.0 0.0) (vect 0.0 1.0)) 
    (segment (vect 0.0 0.0) (vect 1.0 0.0)) 
    (segment (vect 0.0 1.0) (vect 1.0 1.0)) 
    (segment (vect 1.0 0.0) (vect 1.0 1.0)))))

; b 
(define x-painter 
  (segments->painter 
   (list 
    (segment (vect 0.0 0.0) (vect 1.0 1.0)) 
    (segment (vect 0.0 1.0) (vect 1.0 0.0))))) 

; c
(define diamond 
  (segments->painter 
   (list 
    (segment (vect 0.0 0.5) (vect 0.5 1.0)) 
    (segment (vect 0.5 1.0) (vect 1.0 0.5)) 
    (segment (vect 1.0 0.5) (vect 0.5 0.0)) 
    (segment (vect 0.5 0.0) (vect 0.0 0.5))))) 

; d
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


(paint outline)
(paint x-painter)
(paint diamond)
(paint wave)
