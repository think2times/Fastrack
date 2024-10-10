#lang racket

(require "../Modules/base.rkt")


(define (accumulate op initial sequence)
  (if (null? sequence)
      initial
      (op (car sequence)
          (accumulate op initial (cdr sequence)))))

(define (enumerate-interval low high)
  (if (> low high)
      nil
      (cons low (enumerate-interval (+ low 1) high))))

(define (flatmap proc seq)
  (accumulate append nil (map proc seq)))

(define (unique-pairs n)
  (flatmap (lambda (i) (map (lambda (j) (cond ((> i j) (list i j))))
                            (enumerate-interval 1 (- i 1))))
           (enumerate-interval 1 n)))

; 获取不大于正整数n的1/3的最大整数
(define (one-third-factor n)
  (cond ((= (remainder n 3) 0) (/ n 3))
        ((= (remainder n 3) 1) (/ (- n 1) 3))
        (else (/ (- n 2) 3))))

(define (triple-sum n s)
  (if (or (< s 6) (> n (- s 3)))     ; 要找的是不同的3个正整数，所以s至少是6,且n至少比s小3
      nil
      (flatmap (lambda (i) (+ i 1))
               (enumerate-interval 1 (one-third-factor n)))))     ; 需要的是有序3元组，所以第一个数最大也比n/3小
        
