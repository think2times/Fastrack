#lang racket

(require "../Modules/base.rkt")


(define (fib n)
  ; 递归写法
  (define (fib-recur n)
    (cond ((= n 0) 0)
          ((= n 1) 1)
          (else (+ (fib-recur (- n 1))
                   (fib-recur (- n 2))))))

  ; 迭代写法
  (define (fib-iter n)
    (define a 0)
    (define b 1)
    (define (iter a b counter)
      (if (= counter 0)
          a
          (iter b
                (+ a b)
                (- counter 1))))

    (iter a b n))

  (fib-iter n))

; takes a tree as argument and computes the sum of the squares of the leaves that are odd
(define (sum-odd-squares tree)
  (cond ((null? tree) 0)
        ((not (pair? tree))
         (if (odd? tree) (square tree) 0))
        (else (+ (sum-odd-squares (car tree))
                 (sum-odd-squares (cdr tree))))))

(define test (list 1
                   (list 2 (list 3 4) 5)
                   (list 6 7)))

(sum-odd-squares test)

; constructs a list of all the even Fibonacci numbers Fib(k),
; where k is less than or equal to a given integer n
(define (even-fibs n)
  (define (next k)
    (if (> k n)
        nil
        (let ((f (fib k)))
          (if (even? f)
              (cons f (next (+ k 1)))
              (next (+ k 1))))))
  (next 0))

(even-fibs 10)


; Sequence Operations
(define (filter predicate sequence)
  (cond ((null? sequence) nil)
        ((predicate (car sequence))
         (cons (car sequence)
               (filter predicate (cdr sequence))))
        (else (filter predicate (cdr sequence)))))

(filter odd? (list 1 2 3 4 5))

(define (accumulate op initial sequence)
  (if (null? sequence)
      initial
      (op (car sequence)
          (accumulate op initial (cdr sequence)))))

(accumulate + 0 (list 1 2 3 4 5))
(accumulate * 1 (list 1 2 3 4 5))
(accumulate cons nil (list 1 2 3 4 5))

(define (enumerate-interval low high)
  (if (> low high)
      nil
      (cons low (enumerate-interval (+ low 1) high))))

(enumerate-interval 2 7)

(define (enumerate-tree tree)
  (cond ((null? tree) nil)
        ((not (pair? tree)) (list tree))
        (else (append (enumerate-tree (car tree))
                      (enumerate-tree (cdr tree))))))

(enumerate-tree (list 1 (list 2 (list 3 4)) 5))

(define (sum-odd-squares-by-seq tree)
  (accumulate
   + 0 (map square (filter odd? (enumerate-tree tree)))))

(sum-odd-squares-by-seq test)

(define (even-fibs-by-seq n)
  (accumulate
   cons
   nil
   (filter even? (map fib (enumerate-interval 0 n)))))

(even-fibs-by-seq 10)

; constructs a list of the squares of the first n + 1 Fibonacci numbers
(define (list-fib-squares n)
  (accumulate
   cons
   nil
   (map square (map fib (enumerate-interval 0 n)))))

(list-fib-squares 10)

; compute the product of the squares of the odd integers in a sequence
(define (product-of-squares-of-odd-elements sequence)
  (accumulate * 1 (map square (filter odd? (enumerate-tree sequence)))))

(product-of-squares-of-odd-elements (list 1 2 3 4 5))


; Nested Mappings
; Find the smallest integral divisor (greater than 1)
(define (smallest-divisor n) (find-divisor n 2))

(define (find-divisor n test-divisor)
  (cond ((> (square test-divisor) n) n)
        ((divides? test-divisor n) test-divisor)
        (else (find-divisor n (+ test-divisor 1)))))

(define (divides? a b) (= (remainder b a) 0))

(define (prime? n)
  (= n (smallest-divisor n)))

(define (flatmap proc seq)
  (accumulate append nil (map proc seq)))


(define (prime-sum? pair)
  (prime? (+ (car pair) (cadr pair))))      ; cadr 表示取第二个元素

(define (make-pair-sum pair)
  (list (car pair) (cadr pair) (+ (car pair) (cadr pair))))

(define (prime-sum-pairs n)
  (map make-pair-sum
       (filter prime-sum? (flatmap
                           (lambda (i)
                             (map (lambda (j) (list i j))
                                  (enumerate-interval 1 (- i 1))))
                           (enumerate-interval 1 n)))))

(prime-sum-pairs 10)

(define (permutations s)
  (if (null? s) ; empty set?
      (list nil) ; sequence containing empty set
      (flatmap (lambda (x)
                 (map (lambda (p) (cons x p))
                      (permutations (remove x s))))
               s)))

(define (remove item sequence)
  (filter (lambda (x) (not (= x item)))
          sequence))


(permutations (list 1 2 3 6))
