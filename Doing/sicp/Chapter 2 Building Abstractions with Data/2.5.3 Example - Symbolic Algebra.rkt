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
 
;; 判断两个变量是否相同
(define (variable? x) (symbol? x))
(define (same-variable? v1 v2)
  (and (variable? v1) (variable? v2) (eq? v1 v2)))

;; term 及 termlist 相关的过程
(define (make-term order coeff) (list order coeff))
(define (order term) (car term))
(define (coeff term) (cadr term))

(define (the-empty-termlist) '())
(define (empty-termlist? term-list) (null? term-list))
(define (adjoin-term term term-list)
  (if (=zero? (coeff term))
      term-list
      (cons term term-list)))
(define (first-term term-list) (car term-list))
(define (rest-terms term-list) (cdr term-list))


(define (install-polynomial-package)
  ;; 内部过程
  ;; 根据变量和系数构造多项式
  (define (make-poly var terms)
    (cons var terms))
  (define (variable p) (car p))
  (define (term-list p) (cdr p))
  
  ;; 合并同类项
  (define (add-terms tl1 tl2)
    (cond ((empty-termlist? tl1) tl2)
          ((empty-termlist? tl2) tl1)
          (else
           (let ((t1 (first-term tl1))
                 (t2 (first-term tl2)))
             ;; 比较
             (cond ((> (order t1) (order t2))
                    (adjoin-term t1
                                 (add-terms (rest-term tl1) tl2)))
                   ((< (order t1) (order t2))
                    (adjoin-term t1
                                 (add-terms tl1 (rest-term tl2))))
                   (else
                    (adjoin-term (make-term (order t1)
                                            (add (coeff t1) (coeff t2)))
                                 (add-terms (rest-terms tl1)
                                            (rest-terms tl2)))))))))

  ;; 先用乘法分配律计算，然后合并同类项
  (define (mul-terms tl1 tl2)
    (if (empty-termlist? tl1)
        (the-empty-termlist)
        (add-terms (mul-term-by-all-terms (first-term tl1) tl2)
                   (mul-terms (rest-terms tl1) tl2))))

  (define (mul-term-by-all-terms term term-list)
    (if (empty-termlist? term-list)
        (the-empty-termlist)
        (let ((t1 (first-term term-list)))
          (adjoin-term (make-term (+ (order term) (order t1))
                                  (mul (coeff term) (coeff t1)))
                       (mul-term-by-all-terms term (rest-terms term-list))))))
  
  ;; 两个单变量多项式相加
  (define (add-poly p1 p2)
    (if (same-variable? (variable p1) (variable p2))
        (make-poly (variable p1)
                   (add-terms (term-list p1) (term-list p2)))
        (error "Polys not in same var: ADD-POLY" (list p1 p2))))

  ;; 两个单变量多项式相乘
  (define (mul-poly p1 p2)
    (if (same-variable? (variable p1) (variable p2))
        (make-poly (variable p1)
                   (mul-terms (term-list p1) (term-list p2)))
        (error "Polys not in same var: MUL-POLY" (list p1 p2))))
  
  ;; 与系统其他部分交互
  (define (tag p) (attach-tag 'polynomial p))
  (put 'add '(polynomial polynomial)
       (lambda (p1 p2) (tag (add-poly p1 p2))))
  (put 'mul '(polynomial polynomial)
       (lambda (p1 p2) (tag (mul-poly p1 p2))))
  (put 'make 'polynomial
       (lambda (var terms) (tag (make-poly var terms))))
  'polynomial_install_done)

(define (make-polynomial var terms)
  ((get 'make 'polynomial) var terms))

install-polynomial-package
