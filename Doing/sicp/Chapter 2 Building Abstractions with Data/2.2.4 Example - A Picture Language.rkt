#lang racket


(define wave2 (beside wave (flip-vert wave)))
(define wave4 (below wave2 wave2))
