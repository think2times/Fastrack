#lang racket

(require "../modules/base.rkt")


; 注意 n 和 d 都是 procedure 而不是数字,k 表示要计算的项数
(define (cont-frac n d k)
  ; iterative implementation
  (define (frac-iter k pre)
    (if (= k 0)
        pre
        (frac-iter (- k 1) (/ (n k) (+ (d k) pre)))))

  ; recurative implementation
  (define (frac-recur i)
    (if (= i k)
        (/ (n i) (d i))
        (/ (n i) (+ (d i) (frac-recur (+ i 1))))))

  (frac-iter k 0))
  ;(frac-recur 1))

(define (e-euler k)
   (+ 2.0 (cont-frac (lambda (i) 1)
                     ; 观察 Di 序列,发现每 3 个一组,
                     ; 从 1 开始计数的话,在每一组的 3 个数中,只有除以 3 余数为 2 的那个不是 1
                     (lambda (i) 
                       (if (= (remainder i 3) 2) 
                           (/ (+ i 1) 1.5)          ; 先除3向下取整再加1最后乘2,等同于先加1再除1.5
                           1)) 
                     k))) 


; e 的近似值为 2.71828
(e-euler 100)

