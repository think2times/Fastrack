#lang racket 
  
;;; 
;;; put-coersion & get-coersion 
;;; from https://gist.github.com/kinoshita-lab/b76a55759a0d0968cd97 
;;; 
  
(define coercion-list '()) 
  
(define (clear-coercion-list) 
  (set! coercion-list '())) 
  
(define (put-coercion type1 type2 item) 
  (if (get-coercion type1 type2) coercion-list 
      (set! coercion-list 
            (cons (list type1 type2 item) 
                  coercion-list)))) 
  
(define (get-coercion type1 type2) 
  (define (get-type1 listItem) 
    (car listItem)) 
  (define (get-type2 listItem) 
    (cadr listItem)) 
  (define (get-item listItem) 
    (caddr listItem)) 
  (define (get-coercion-iter list type1 type2) 
    (if (null? list) #f 
        (let ((top (car list))) 
          (if (and (equal? type1 (get-type1 top)) 
                   (equal? type2 (get-type2 top))) 
              (get-item top) 
              (get-coercion-iter (cdr list) type1 type2))))) 
  (get-coercion-iter coercion-list type1 type2)) 
  
;;; 
;;; Put & Get, from https://stackoverflow.com/a/19114031 
;;; 
  
(define *op-table* (make-hash)) 
(define (put op type proc) 
  (hash-set! *op-table* (list op type) proc)) 
(define (get op type) 
  (hash-ref *op-table* (list op type) #f)) 
  
;;; 
;;; Tags from 2.4.2 
;;; 
  
(define (attach-tag type-tag z) 
  (cons type-tag z)) 
  
(define (type-tag datum) 
  (if (pair? datum) 
      (car datum) 
      (error "Not a pair: TYPE-TAG" datum))) 
(define (contents datum) 
  (if (pair? datum) 
      (cdr datum) 
      (error "Not a pair: CONTENT" datum))) 
  
;;; 
;;; 2.4.3 Data-Directed Programming and Additivity 
;;; 
  
(define (install-rectangular-package) 
  ;; internal procedures 
  (define (real-part z) (car z)) 
  (define (imag-part z) (cdr z)) 
  (define (make-from-real-imag x y) 
    (cons x y)) 
  
  ;; change sqrt, +, square, atan, *, cos, sin to generic procedures 
  (define (magnitude z) 
    (sqrt-generic (add (square-generic (real-part z)) 
                       (square-generic (imag-part z))))) 
  (define (angle z) 
    (atan-generic (imag-part z) (real-part z))) 
  (define (make-from-mag-ang r a) 
    (cons (mul r (cosine a)) (mul r (sine a)))) 
  
  ;; interface to the rest of the system 
  (define (tag x) 
    (attach-tag 'rectangular x)) 
  (put 'real-part '(rectangular) real-part) 
  (put 'imag-part '(rectangular) imag-part) 
  (put 'magnitude '(rectangular) magnitude) 
  (put 'angle '(rectangular) angle) 
  (put 'make-from-real-imag 'rectangular 
       (lambda (x y) 
         (tag (make-from-real-imag x y)))) 
  (put 'make-from-mag-ang 'rectangular 
       (lambda (r a) 
         (tag (make-from-mag-ang r a)))) 
  'done) 
  
(define (install-polar-package) 
  ;; internal procedures 
  (define (magnitude z) (car z)) 
  (define (angle z) (cdr z)) 
  (define (make-from-mag-ang r a) (cons r a)) 
  
  ;; change *, cos, sin, sqrt, +, square, atan to generic procedures 
  (define (real-part z) 
    (mul (magnitude z) (cosine (angle z)))) 
  (define (imag-part z) 
    (mul (magnitude z) (sine (angle z)))) 
  (define (make-from-real-imag x y) 
    (cons (sqrt-generic (add (square-generic x) (square-generic y))) 
          (atan-generic y x))) 
  
  ;; interface to the rest of the system 
  (define (tag x) (attach-tag 'polar x)) 
  (put 'real-part '(polar) real-part) 
  (put 'imag-part '(polar) imag-part) 
  (put 'magnitude '(polar) magnitude) 
  (put 'angle '(polar) angle) 
  (put 'make-from-real-imag 'polar 
       (lambda (x y) 
         (tag (make-from-real-imag x y)))) 
  (put 'make-from-mag-ang 'polar 
       (lambda (r a) 
         (tag (make-from-mag-ang r a)))) 
  'done) 
  
  
(define (real-part z) 
  (apply-generic 'real-part z)) 
(define (imag-part z) 
  (apply-generic 'imag-part z)) 
(define (magnitude z) 
  (apply-generic 'magnitude z)) 
(define (angle z) 
  (apply-generic 'angle z)) 
  
;;; 
;;; APPLY-GENERIC 
;;; From 2.5.2 Combining Data of Different Types -> Coercion 
;;; 
  
(define (apply-generic op . args) 
  (let ((type-tags (map type-tag args))) 
    (let ((proc (get op type-tags))) 
      (if proc 
          (apply proc (map contents args)) 
          (if (= (length args) 2) 
              (let ((type1 (car type-tags)) 
                    (type2 (cadr type-tags)) 
                    (a1 (car args)) 
                    (a2 (cadr args))) 
                (let ((t1->t2 (get-coercion type1 type2)) 
                      (t2->t1 (get-coercion type2 type1))) 
                  (cond (t1->t2 
                         (apply-generic op (t1->t2 a1) a2)) 
                        (t2->t1 
                         (apply-generic op a1 (t2->t1 a2))) 
                        (else (error "No method for these types: 
                                       APPLY-GENERIC" 
                                     (list op type-tags)))))) 
              (error "No method for these types: APPLY-GENERIC" 
                     (list op type-tags))))))) 
  
;;; 
;;; Added 
;;; Coerce rational to scheme-number 
;;; 
  
(define (rational->scheme-number x) 
  (let ((numer (car (contents x))) 
        (denom (cdr (contents x)))) 
    (make-scheme-number (/ (* numer 1.0) denom)))) 
  
(put-coercion 'rational 'scheme-number rational->scheme-number) 
  
;;; 
;;; 2.5.1 Generic Arithmetic Operations 
;;; 
  
(define (add x y) (apply-generic 'add x y)) 
(define (sub x y) (apply-generic 'sub x y)) 
(define (mul x y) (apply-generic 'mul x y)) 
(define (div x y) (apply-generic 'div x y)) 
  
;; Add definitons of generic procedures 
(define (sine x) (apply-generic 'sine x)) 
(define (cosine x) (apply-generic 'cosine x)) 
(define (sqrt-generic x) (apply-generic 'sqrt-generic x)) 
(define (atan-generic y x) (apply-generic 'atan-generic y x)) 
(define (square-generic x) (mul x x)) 
  
(define (install-scheme-number-package) 
  (define (tag x) 
    (attach-tag 'scheme-number x)) 
  (put 'add '(scheme-number scheme-number) 
       (lambda (x y) (tag (+ x y)))) 
  (put 'sub '(scheme-number scheme-number) 
       (lambda (x y) (tag (- x y)))) 
  (put 'mul '(scheme-number scheme-number) 
       (lambda (x y) (tag (* x y)))) 
  (put 'div '(scheme-number scheme-number) 
       (lambda (x y) (tag (/ x y)))) 
  (put 'make 'scheme-number 
       (lambda (x) (tag x))) 
  
  ;; added 
  (put 'sine '(scheme-number) (lambda (x) (tag (sin x)))) 
  (put 'cosine '(scheme-number) (lambda (x) (tag (cos x)))) 
  (put 'sqrt-generic '(scheme-number) (lambda (x) (tag (sqrt x)))) 
  (put 'atan-generic '(scheme-number scheme-number) (lambda (y x) (tag (atan y x)))) 
  
  'done) 
  
(define (make-scheme-number n) 
  ((get 'make 'scheme-number) n)) 
  
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
  (put 'make 'rational 
       (lambda (n d) (tag (make-rat n d)))) 
  
  ;; added 
  (define (tag-schemenumber x) 
    (attach-tag 'scheme-number x)) 
  (put 'sine '(rational) 
       (lambda (x) 
         (tag-schemenumber (sin (/ (numer x) (denom x)))))) 
  (put 'cosine '(rational) 
       (lambda (x) 
         (tag-schemenumber (cos (/ (numer x) (denom x)))))) 
  (put 'sqrt-generic '(rational) 
       (lambda (x) 
         (tag-schemenumber (sqrt (/ (* 1.0 (numer x)) (denom x)))))) 
  (put 'atan-generic '(rational rational) 
       (lambda (y x) 
         (tag-schemenumber (atan (/ (numer y) (denom y)) 
                                 (/ (numer x) (denom x)))))) 
  
  'done) 
  
(define (make-rational n d) 
  ((get 'make 'rational) n d)) 
  
(define (install-complex-package) 
  ;; imported procedures from rectangular 
  ;; and polar packages 
  (define (make-from-real-imag x y) 
    ((get 'make-from-real-imag 
          'rectangular) 
     x y)) 
  (define (make-from-mag-ang r a) 
    ((get 'make-from-mag-ang 'polar) 
     r a)) 
  ;; internal procedures 
  
  ;; change +, -, *, / to generic procedures 
  (define (add-complex z1 z2) 
    (make-from-real-imag 
     (add (real-part z1) (real-part z2)) 
     (add (imag-part z1) (imag-part z2)))) 
  (define (sub-complex z1 z2) 
    (make-from-real-imag 
     (sub (real-part z1) (real-part z2)) 
     (sub (imag-part z1) (imag-part z2)))) 
  (define (mul-complex z1 z2) 
    (make-from-mag-ang 
     (mul (magnitude z1) (magnitude z2)) 
     (add (angle z1) (angle z2)))) 
  (define (div-complex z1 z2) 
    (make-from-mag-ang 
     (div (magnitude z1) (magnitude z2)) 
     (sub (angle z1) (angle z2)))) 
  
  ;; interface to rest of the system 
  (define (tag z) (attach-tag 'complex z)) 
  (put 'add '(complex complex) 
       (lambda (z1 z2) 
         (tag (add-complex z1 z2)))) 
  (put 'sub '(complex complex) 
       (lambda (z1 z2) 
         (tag (sub-complex z1 z2)))) 
  (put 'mul '(complex complex) 
       (lambda (z1 z2) 
         (tag (mul-complex z1 z2)))) 
  (put 'div '(complex complex) 
       (lambda (z1 z2) 
         (tag (div-complex z1 z2)))) 
  (put 'make-from-real-imag 'complex 
       (lambda (x y) 
         (tag (make-from-real-imag x y)))) 
  (put 'make-from-mag-ang 'complex 
       (lambda (r a) 
         (tag (make-from-mag-ang r a)))) 
  'done) 
  
(define (make-complex-from-real-imag x y) 
  ((get 'make-from-real-imag 'complex) x y)) 
(define (make-complex-from-mag-ang r a) 
  ((get 'make-from-mag-ang 'complex) r a)) 
  
  
;;; 
;;; Test 
;;; 
  
(install-scheme-number-package) 
(install-rational-package) 
(install-rectangular-package) 
(install-polar-package) 
(install-complex-package) 
  
(define x1 (make-scheme-number 1)) 
(define x2 (make-scheme-number 2)) 
  
(define y1 (make-rational 2 3)) 
(define y2 (make-rational 2 5)) 
  
(define z1 (make-complex-from-mag-ang x1 x2)) 
(define z2 (make-complex-from-mag-ang x1 y1)) 
(define z3 (make-complex-from-real-imag y1 y2)) 
  
(add z1 z2) 
(add z1 z3) 
(sub z1 z2) 
(sub z1 z3) 
(mul z1 z2) 
(mul z1 z3) 
(div z1 z2) 
(div z1 z3) 