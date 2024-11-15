#lang racket

(require "../Modules/base.rkt")


(define (variable? x) (symbol? x))

(define (same-variable? v1 v2)
  (and (variable? v1) (variable? v2) (eq? v1 v2)))

(define (=number? exp num) (and (number? exp) (= exp num)))

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

(define (deriv exp var)
  (cond ((number? exp) 0)
        ((variable? exp) (if (same-variable? exp var) 1 0))
        (else ((get 'deriv (operator exp))
               (operands exp) var))))

(define (operator exp) (car exp))
(define (operands exp) (cdr exp))

(define (install-deriv-package)
  ;; internal procedures
  ;; sum
  (define (make-sum a1 a2)
    (cond ((=number? a1 0) a2)
          ((=number? a2 0) a1)
          ((and (number? a1) (number? a2)) (+ a1 a2))
          (else (list '+ a1 a2))))

  (define (sum? x) (and (pair? x) (eq? (car x) '+)))

  (define (addend s) (car s))

  (define (augend s) (cadr s))

  (define (sum-deriv expr var) 
    (make-sum (deriv (addend expr) var) 
              (deriv (augend expr) var))) 

  ;; product
  (define (make-product m1 m2)
    (cond ((or (=number? m1 0) (=number? m2 0)) 0)
          ((=number? m1 1) m2)
          ((=number? m2 1) m1)
          ((and (number? m1) (number? m2)) (* m1 m2))
          (else (list '* m1 m2))))

  (define (product? x) (and (pair? x) (eq? (car x) '*)))

  (define (multiplier p) (car p))

  (define (multiplicand p) (cadr p))

  (define (product-deriv expr var) 
    (make-sum (make-product (deriv (multiplier expr) var) 
                            (multiplicand expr))
              (make-product (multiplier expr)
                            (deriv (multiplicand expr) var))))

  ;; exponentiate
  (define (make-exponentiation base exponent)
    (cond ((=number? base 0) 0)
          ((=number? base 1) 1)
          ((and (number? base) (=number? exponent 0)) 1)
          ((and (number? base) (=number? exponent 1)) base)
          ((and (number? base) (number? exponent)) (* base (make-exponentiation base (- exponent 1))))
          (else (list '** base exponent))))

  (define (base e) (car e))

  (define (exponent e) (cadr e))

  (define (exponentation-deriv expr var) 
    (make-product (exponent expr) 
                  (make-product  
                   (make-exponentiation (base expr) 
                                        (make-sum (exponent expr) -1)) 
                   (deriv (base expr) var))))
<<<<<<< HEAD

=======
               
>>>>>>> b44974c026b167484c540725f26ef6d61807ee5e
  ;; interface to the rest of the system
  (put 'deriv '+ sum-deriv)
  (put 'deriv '* product-deriv)
  (put 'deriv '** exponentation-deriv)
  'done)


(install-deriv-package)


(deriv '(+ x x x) 'x) 
(deriv '(* x x x) 'x) 
(deriv '(+ x (* x  (+ x (+ y 2)))) 'x) 
(deriv '(+ x (* 3 (+ x (+ y 2)))) 'x)
(deriv '(** x 3) 'x) 
