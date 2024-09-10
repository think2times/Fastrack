#lang racket

(require "../Modules/base.rkt")


; 任何数加 0 都等于它本身。所以,表示 0 的函数，无论你给它传入什么函数 f 和参数 x，它都直接返回 x，相当于什么都不做。
; (lambda (f) ...) 定义了一个匿名函数，它接受一个函数 f 作为参数，并返回 (lambda (x) x)。
; (lambda (x) x) 定义了另一个匿名函数，它接受一个参数 x,并直接返回 x。
; 组合起来:zero 函数本质上就是一个恒等函数，无论你给它传入什么函数 f，它都会返回一个新的函数，这个新函数会直接返回它的输入 x。
; 这符合我们对 0 的理解————任何数加 0 等于它本身。
(define zero (lambda (f) (lambda (x) x)))

; 1. 把 (lambda (x) (square x)) 传给 zero 作为参数，返回新的函数 (lambda (x) x)
; 2. 再把 10 传给 (lambda (x) x)，得到原数 10
(display ((zero (lambda (x) (square x))) 10))
(newline)

; n 必须是 Church Numeral，比如说上面定义的 zero
; 返回值是一个新的 Church Numeral，表示的值为 n + 1
(define (add-1 n)
  (lambda (f) (lambda (x) (f ((n f) x)))))


(display (((add-1 zero) square) 10))
(newline)

; 1. 先用 f1 表示匿名函数 (lambda (x) (+ x 1))，则原式变为 ((zero f1) 0)
; 2. 把 zero 函数用它的定义替代，得到 (((lambda (f) (lambda (x) x)) f1) 0)
; 3. 把 f1 带入到 zero 的返回值函数，得到 ((lambda (x) x) 0)
; 4. (lambda (x) x) 函数会返回传入的参数，也就是0
((zero (lambda (x) (+ x 1))) 0)

; 1. 把 zero 作为参数传入，得到 (lambda (f) (lambda (x) (f ((zero f) x)))))
; 2. 先处理 (zero f)，根据上面我们对 zero 函数的分析，无论传入什么函数作为参数，它都返回 (lambda (x) x)
; 3. 则 ((zero f) x) 就是 x，(lambda (f) (lambda (x) (f x)))，也就是无论传入什么 f 和 x，都会返回 (f x)
(define one (add-1 zero))

; 根据上面的分析，下面的程序相当于执行 ((lambda (x) (+ x 1)) 0), 也就是 0 + 1
((one (lambda (x) (+ x 1))) 0)

; 1. 把 one 作为参数传入，得到 (lambda (f) (lambda (x) (f ((one f) x)))))
; 2. 根据上面的分析，((one f) x) 会返回 (f x)
; 3. 所以下面的函数无论传入什么 f 和 x，都会返回 (f (f x))
(define two (add-1 one))

; 根据上面的分析,下面的程序相当于执行 ((lambda (x) (+ x 1)) ((lambda (x) (+ x 1)) 0)), 也就是 ((0 + 1) + 1)
((two (lambda (x) (+ x 1))) 0)

; 以此类推，可以用如下方式直接定义 one, two, three
(define one (lambda (f) (lambda (x) (f x)))) 
(define two (lambda (f) (lambda (x) (f (f x)))))
(define three (lambda (f) (lambda (x) (f (f (f x)))))) 


(define (add a b) 
  (lambda (f) 
    (lambda (x) ((a f) ((b f) x)))))
