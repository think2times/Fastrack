#lang racket

(require racket/trace)
(require "../Modules/base.rkt")

(define (expt-recur b n)
  (if (= n 0)
      1
      (* b (expt-recur b (- n 1)))))

(define (expt-iter b n)
  (define (iter now count)
    (if (= count 0)
        now
        (iter (* now b) (- count 1))))
  (iter 1 n))

(define (expt-recur-by-square b n)
  (cond ((= n 0) 1)
        ((even? n) (square (expt-recur-by-square b (/ n 2))))
        (else (* b (expt-recur-by-square b (- n 1))))))

(define (expt-iter-by-square b n)
  (define (iter b n a)
    (cond ((= n 0) a)
          ((even? n) (iter (square b)
                           (/ n 2)
                           a))
          (else (iter b
                      (- n 1)
                      (* a b)))))
  (iter b n 1))


(trace expt-recur)
(expt-recur 2 10)

(trace expt-iter)
(expt-iter 2 127)

(trace expt-recur-by-square)
(expt-recur-by-square 2 127)

(trace expt-iter-by-square)
(expt-iter-by-square 2 127)
