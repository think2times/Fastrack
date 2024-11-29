#lang racket

(require "../Modules/base.rkt")


(define (attach-tag type-tag contents)
  (cons type-tag contents))

(define (type-tag datum)
  (if (pair? datum)
      (car datum)
      (error "Bad tagged datum: TYPE-TAG" datum)))

(define (contents datum)
  (if (pair? datum)
      (cdr datum)
      (error "Bad tagged datum: CONTENTS" datum)))

; 将当前的类型升级为上一级,如果不存在对应的转换函数,返回 false
(define (tower-raise origin target)
  (let ((o-type (type-tag origin))
        (t-type (type-tag target)))
    (cond ((eq? o-type t-type)    
           origin)
          ((get 'raise (list o-type))
           (tower-raise ((get 'raise (list o-type)) (contents origin)) target))
          (else false))))

(define (raise origin)
  (let ((raise-proc (get 'raise (list (type-tag origin)))))
    (if raise-proc
        (raise-proc (contents origin))
        false)))

(define (project origin)
  (let ((project-proc (get 'project (list (type-tag origin)))))
    (if project-proc
        (project-proc (contents origin))
        false)))

;; 在不失精度地前提下,把一个数的类型降到最底层
(define (drop origin)
  (if (pair? origin)    ; 过滤 false 等没有 type-tag 的参数
      (let ((project-number (project origin)))
        (if (and project-number
                 (equ? origin (raise project-number)))
            (drop project-number)
            origin))
      origin))

(define (apply-generic op . args) 
  (define (no-method type-tags) 
    (error "No method for these types" 
           (list op type-tags)))

  (let ((type-tags (map type-tag args)))
    (let ((proc (get op type-tags))) 
      (if proc 
          (drop (apply proc (map contents args)))
          (if (and (= (length args) 2)
                   (not (equal? (car type-tags) (cadr type-tags))))    ; 如果参数类型相同,不需要转换
              ;; 假设类型以简单的 tower 形式排序,从低到高
              (let ((a1 (car args))
                    (a2 (cadr args)))
                (cond ((tower-raise a1 a2)
                       (apply-generic op (tower-raise a1 a2) a2))
                      ((tower-raise a2 a1)
                       (apply-generic op a1 (tower-raise a2 a1)))
                      (else (no-method type-tags))))
              (no-method type-tags))))))


(define (add x y) (apply-generic 'add x y))
(define (sub x y) (apply-generic 'sub x y))
(define (mul x y) (apply-generic 'mul x y))
(define (div x y) (apply-generic 'div x y))
(define (equ? x y) (apply-generic 'equ? x y))
(define (=zero? x) (apply-generic '=zero? x))
(define (exp x y) (apply-generic 'exp x y))
(define (sine x) (apply-generic 'sine x))
(define (cosine x) (apply-generic 'cosine x))

;; 整数运算包
(define (install-integer-package)
  (define (tag x) (attach-tag 'integer x))
  (put 'add '(integer integer)
       (lambda (x y) (tag (+ x y))))
  (put 'sub '(integer integer)
       (lambda (x y) (tag (- x y))))
  (put 'mul '(integer integer)
       (lambda (x y) (tag (* x y))))
  (put 'div '(integer integer)
       (lambda (x y) (tag (round (/ x y)))))     ; 四舍五入
  ; 由于 sin 和 cos 的结果不一定是整数或有理数
  ; 所以先把它的类型转为有理数，然后再转为实数
  (put 'sine '(integer)
       (lambda (x) (sine (raise (tag x)))))   ; 把整数形式升级为有理数
  (put 'cosine '(integer)
       (lambda (x) (cosine (raise (tag x))))) ; 把整数形式升级为有理数
  (put 'equ? '(integer integer) =)
  (put '=zero? '(integer) (lambda (x) (= x 0)))
  (put 'exp '(integer integer)
       ; using primitive expt
       (lambda (x y) (tag (expt x y))))
  (put 'raise '(integer)
       (lambda (x) (make-rational x 1)))
  (put 'make 'integer
       (lambda (x) (tag x))))

(define (make-integer n)
  ((get 'make 'integer) n))

;; 有理数
(define (install-rational-package)
  ;; internal procedures
  (define (numer x) (car x))
  (define (denom x) (cdr x))
  (define (make-rat n d)
    (let ((g (gcd n d)))
      (cons (/ n g) (/ d g))))
  (define (add-rat x y)
    (make-rat (+ (* (numer x) (denom y))
                 (* (numer y) (denom x)))
              (* (denom x) (denom y))))
  (define (sub-rat x y)
    (make-rat (- (* (numer x) (denom y))
                 (* (numer y) (denom x)))
              (* (denom x) (denom y))))
  (define (mul-rat x y)
    (make-rat (* (numer x) (numer y))
              (* (denom x) (denom y))))
  (define (div-rat x y)
    (make-rat (* (numer x) (denom y))
              (* (denom x) (numer y))))
  (define (equ? x y)
    ;; 先化简为最简有理数
    (let ((simple-x (make-rat (numer x) (denom x)))
          (simple-y (make-rat (numer y) (denom y))))
      (and (= (numer simple-x) (numer simple-y))
           (= (denom simple-x) (denom simple-y)))))

  ;; 用十字相乘更简单
  ;; (define (equ? x y) (= (* (numer x) (denom y)) (* (numer y) (denom x))))
  
  ;; interface to rest of the system
  (define (tag x) (attach-tag 'rational x))
  (put 'add '(rational rational)
       (lambda (x y) (tag (add-rat x y))))
  (put 'sub '(rational rational)
       (lambda (x y) (tag (sub-rat x y))))
  (put 'mul '(rational rational)
       (lambda (x y) (tag (mul-rat x y))))
  (put 'div '(rational rational)
       (lambda (x y) (tag (div-rat x y))))
  (put 'sine '(rational)
       (lambda (x) (sine (raise (tag x)))))   ; 把有理数形式升级为实数
  (put 'cosine '(rational)
       (lambda (x) (cosine (raise (tag x))))) ; 把有理数形式升级为实数
  (put 'equ? '(rational rational)
       (lambda (x y) (equ? x y)))
  (put '=zero? '(rational)
       (lambda (x) (= (numer x) 0)))
  (put 'raise '(rational)
       (lambda (x) (make-real (/ (numer x) (denom x)))))
  (put 'project '(rational)
       (lambda (x) (make-integer (round (/ (numer x) (denom x))))))
  (put 'make 'rational
       (lambda (n d) (tag (make-rat n d)))))

(define (make-rational n d)
  ((get 'make 'rational) n d))

(define (install-real-package)
  (define (tag x) (attach-tag 'real x))
  (put 'add '(real real)
       (lambda (x y) (tag (+ x y))))
  (put 'sub '(real real)
       (lambda (x y) (tag (- x y))))
  (put 'mul '(real real)
       (lambda (x y) (tag (* x y))))
  (put 'div '(real real)
       (lambda (x y) (tag (/ x y))))
  ; sin 和 cos 的结果一定是实数
  (put 'sine '(real) (lambda (x) (tag (sin x))))
  (put 'cosine '(real) (lambda (x) (tag (cos x))))
  (put 'equ? '(real real)
       (lambda (x y) (= x y)))
  (put '=zero? '(real)
       (lambda (x) (= x 0)))
  (put 'raise '(real)
       (lambda (x) (make-complex-from-real-imag x 0)))
  (put 'project '(real)
       ;; 实数转为有理数没啥简单的好办法
       ;; 我采用了对实数四舍五入然后转为分母为1的有理数的逻辑
       (lambda (x) (make-rational (round x) 1)))
  (put 'make 'real (lambda (x) (tag (* 1.0 x)))))

(define (make-real r)
  ((get 'make 'real) r))


;; 复数
(define (install-rectangular-package)
  ;; internal procedures
  (define (real-part z) (car z))
  (define (imag-part z) (cdr z))
  (define (make-from-real-imag x y) (cons x y))
  
  (define (magnitude z)
    (sqrt (+ (square (real-part z))
             (square (imag-part z)))))
  (define (angle z)
    (atan (imag-part z) (real-part z)))
  (define (make-from-mag-ang r a)
    (cons (* r (cos a)) (* r (sin a))))
  
  ;; interface to the rest of the system
  (define (tag x) (attach-tag 'rectangular x))
  (put 'real-part '(rectangular) real-part)
  (put 'imag-part '(rectangular) imag-part)
  (put 'magnitude '(rectangular) magnitude)
  (put 'angle '(rectangular) angle)
  (put 'make-from-real-imag 'rectangular
       (lambda (x y) (tag (make-from-real-imag x y))))
  (put 'make-from-mag-ang 'rectangular
       (lambda (r a) (tag (make-from-mag-ang r a)))))

(define (install-polar-package)
  ;; internal procedures
  (define (magnitude z) (car z))
  (define (angle z) (cdr z))
  (define (make-from-mag-ang r a) (cons r a))
  
  (define (real-part z) (* (magnitude z) -(cos (angle z))))
  (define (imag-part z) (* (magnitude z) (sin (angle z))))
  (define (make-from-real-imag x y)
    (cons (sqrt (+ (square x) (square y)))
          (atan y x)))
  
  ;; interface to the rest of the system
  (define (tag x) (attach-tag 'polar x))
  (put 'real-part '(polar) real-part)
  (put 'imag-part '(polar) imag-part)
  (put 'magnitude '(polar) magnitude)
  (put 'angle '(polar) angle)
  (put 'make-from-real-imag 'polar
       (lambda (x y) (tag (make-from-real-imag x y))))
  (put 'make-from-mag-ang 'polar
       (lambda (r a) (tag (make-from-mag-ang r a)))))

(define (install-complex-package)
  ;; imported procedures from rectangular and polar packages
  (define (make-from-real-imag x y)
    ((get 'make-from-real-imag 'rectangular) x y))
  (define (make-from-mag-ang r a)
    ((get 'make-from-mag-ang 'polar) r a))
  ;; internal procedures
  (define (add-complex z1 z2)
    (make-from-real-imag (add (real-part z1) (real-part z2))
                         (add (imag-part z1) (imag-part z2))))
  (define (sub-complex z1 z2)
    (make-from-real-imag (sub (real-part z1) (real-part z2))
                         (sub (imag-part z1) (imag-part z2))))
  (define (mul-complex z1 z2)
    (make-from-mag-ang (mul (magnitude z1) (magnitude z2))
                       (add (angle z1) (angle z2))))
  (define (div-complex z1 z2)
    (make-from-mag-ang (div (magnitude z1) (magnitude z2))
                       (sub (angle z1) (angle z2))))
  (define (equ? z1 z2)
    (and (= (real-part z1) (real-part z2))
         (= (imag-part z1) (imag-part z2))))
  ;; interface to rest of the system
  (define (tag z) (attach-tag 'complex z))
  (put 'add '(complex complex)
       (lambda (z1 z2) (tag (add-complex z1 z2))))
  (put 'sub '(complex complex)
       (lambda (z1 z2) (tag (sub-complex z1 z2))))
  (put 'mul '(complex complex)
       (lambda (z1 z2) (tag (mul-complex z1 z2))))
  (put 'div '(complex complex)
       (lambda (z1 z2) (tag (div-complex z1 z2))))
  (put 'equ? '(complex complex)
       (lambda (z1 z2) (equ? z1 z2)))
  (put '=zero? '(complex)
       (lambda (z) (= (real-part z) (imag-part z) 0)))
  (put 'project '(complex)
       (lambda (z) (make-real (real-part z))))
  (put 'make-from-real-imag 'complex
       (lambda (x y) (tag (make-from-real-imag x y))))
  (put 'make-from-mag-ang 'complex
       (lambda (r a) (tag (make-from-mag-ang r a))))
  (put 'real-part '(complex) real-part)
  (put 'imag-part '(complex) imag-part)
  (put 'magnitude '(complex) magnitude)
  (put 'angle '(complex) angle))

(define (make-complex-from-real-imag x y)
  ((get 'make-from-real-imag 'complex) x y))
(define (make-complex-from-mag-ang r a)
  ((get 'make-from-mag-ang 'complex) r a))

(define (real-part z) (apply-generic 'real-part z)) 
(define (imag-part z) (apply-generic 'imag-part z)) 
(define (magnitude z) (apply-generic 'magnitude z)) 
(define (angle z) (apply-generic 'angle z))


(install-integer-package) 
(install-rational-package)
(install-real-package)
(install-rectangular-package) 
(install-polar-package) 
(install-complex-package) 
  
(define n1 (make-integer 1)) 
(define n2 (make-integer 2)) 
  
(define rat1 (make-rational 2 3)) 
(define rat2 (make-rational 2 5)) 

(define r1 (make-real 5))
(define r2 (make-real 3.2))

(define c1 (make-complex-from-real-imag rat1 rat2))
(define c2 (make-complex-from-mag-ang r2 n2))

(newline)
(display "测试样例")
(newline)
(add c1 c2)
(div c2 c1)
(sine n1)
(cosine n2)
(sine rat1)
(cosine rat2)
(sine r1)
(cosine r2)

; 检查是否影响到了前面的其他过程
(newline)
(display "检查是否影响到了前面的其他过程")
(newline)

(add n1 n2)
(sub n1 n2)
(mul n1 n2)
(div n1 n2)
(add rat1 (raise n1))
(sub (raise n2) rat2)
(mul rat1 (raise n2))
(div (raise n1) rat2)
(add r1 (raise rat1))
(sub (raise rat1) r2)
(mul r1 (raise rat2))
(div (raise rat2) r2)
(add c1 (raise r1))
(sub (raise r1) c2)
(mul c1 (raise r2))
(div (raise r2) c2)
(exp n2 n2)

(add n1 rat1)
(add rat1 n1)
(add r2 rat1)
(add c2 rat2)
(sub n1 r1)
(sub r2 n2)

(newline)
(display "因为复数乘法都是用 magnitude 和 angle 表示的,所以类型都是 polar")
(newline)
(mul n1 c1)
(mul c1 n1)
(div n1 c2)
(div c2 n2)

(display "测试 project")
(newline)
(project rat1)
(project rat2)
(project r1)
(project r2)
(project c1)
(project c2)

(newline)
(display "测试 drop")
(newline)
(drop rat1)
(drop rat2)
(drop r1)
(drop r2)
(drop c1)
(drop c2)
