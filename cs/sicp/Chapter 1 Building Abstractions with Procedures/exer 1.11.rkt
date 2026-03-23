#lang racket

; 递归写法
(define (f-recur n)
  (if (< n 3)
      n
      (+ (f-recur (- n 1))
         (* 2 (f-recur (- n 2)))
         (* 3 (f-recur (- n 3))))))

; 迭代写法
(define (f-iter n)
  ; a相当于f(n-1), b相当于f(n-2), c相当于f(n-3), n相当于计数器
  ; 虽然题目给的公式是倒着算，但是实现的算法是正着算，依次把f(3), f(4)...算出来
  ; 当作为计数器的n恰好等于3时，a此时正好为f(n-1)，所以需要再算一次才能得到f(n)
  (define (iter a b c n)
    (if (< n 3)
        a
        (iter (+ a
                 (* 2 b)
                 (* 3 c))
              a
              b
              (- n 1))))

  (iter 2 1 0 n))


(f-iter 32)
(f-recur 32)
