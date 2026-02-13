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


; 获取不大于正整数n的1/3的最大整数
(define (one-third-factor n)
  (cond ((= (remainder n 3) 0) (/ n 3))
        ((= (remainder n 3) 1) (/ (- n 1) 3))
        (else (/ (- n 2) 3))))

(define (ordered-triple-sum n s)
  (if (or (< s 6) (> n (- s 3)))     ; 要找的是不同的3个正整数，所以s至少是6,且n至少比s小3
      nil
      (filter (lambda (seq) (= (accumulate + 0 seq) s))
              (flatmap (lambda (i)
                         (flatmap (lambda (j)
                                    (map (lambda (k) (list i j k))
                                         (enumerate-interval (+ j 1) n)))    ; 第三个数比第二个大
                                    (enumerate-interval (+ i 1) (- n 1))))   ; 第二个数比第一个大
                       (enumerate-interval 1 (one-third-factor n))))))       ; 需要的是有序3元组，所以第一个数最大也比n/3小


(ordered-triple-sum 15 20)