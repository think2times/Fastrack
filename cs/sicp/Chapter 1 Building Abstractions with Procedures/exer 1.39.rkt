#lang racket

(require "../modules/base.rkt")


; 注意 n 和 d 都是 procedure 而不是数字,k 表示要计算的项数
(define (cont-frac n d radians k)
  ; iterative implementation
  (define (frac-iter i pre)
    (if (= i 1)
        pre
        ; 这里要注意计算的是 (d (- i 1))，而不是 (d i)，否则会漏掉 1-... 这一项
        (frac-iter (- i 1) (/ (n i) (- (d (- i 1)) pre)))))      

  ; recurative implementation
  (define (frac-recur i)
    (if (= i k)
        (/ (n i) (d i))
        (/ (n i) (- (d i) (frac-recur (+ i 1))))))

  (frac-iter k (square radians)))         ; 注意初始值是 x^2
  ;(frac-recur 1))

; 注意到原式最上面的分子其实可以写成 x^2 / x，这样它的结构就可以保持一致，只要在最后把结果除以 x 即可
(define (tan-cf x k)
  (let ((radians (/ (* pi x) 180)))
    (/ (cont-frac (lambda (i) (square radians))
                  (lambda (i) (- (* 2 i) 1))
                  radians
                  k)
       radians)))


; tan 30° ≈ 0.577，tan 45° = 1，tan 60° ≈ 1.732
(tan-cf 30 10)
(tan-cf 45 10)
(tan-cf 60 10)
