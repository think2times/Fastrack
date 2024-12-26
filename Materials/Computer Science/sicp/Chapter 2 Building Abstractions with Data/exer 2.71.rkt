#lang racket


; Representing Huffman trees
(define (make-leaf symbol weight) (list 'leaf symbol weight))

(define (leaf? object) (eq? (car object) 'leaf))

(define (symbol-leaf x) (cadr x))

(define (weight-leaf x) (caddr x))

(define (make-code-tree left right)
  (list left
        right
        (append (symbols left) (symbols right))
        (+ (weight left) (weight right))))

(define (left-branch tree) (car tree))

(define (right-branch tree) (cadr tree))

(define (symbols tree)
  (if (leaf? tree)
      (list (symbol-leaf tree))
      (caddr tree)))

(define (weight tree)
  (if (leaf? tree)
      (weight-leaf tree)
      (cadddr tree)))

; Sets of weighted elements
(define (adjoin-set x set)
  (cond ((null? set) (list x))
        ((< (weight x) (weight (car set))) (cons x set))
        (else (cons (car set)
                    (adjoin-set x (cdr set))))))

(define (make-leaf-set pairs)
  (if (null? pairs)
      '()
      (let ((pair (car pairs)))
        (adjoin-set (make-leaf (car pair)      ; symbol
                               (cadr pair))    ; frequency
                    (make-leaf-set (cdr pairs))))))


(define (generate-huffman-tree pairs)
  (successive-merge (make-leaf-set pairs)))

(define (successive-merge leaf-set)
  (if (null? leaf-set)
      '()
      (let ((first (car leaf-set))
            (last (cdr leaf-set)))
        (if (null? last)
            first
            (successive-merge (adjoin-set (make-code-tree first (car last))
                                          (cdr last)))))))

(define (encode message tree)
  (if (null? message)
      '()
      (append (encode-symbol (car message) tree)
              (encode (cdr message) tree))))

(define (element-of-set? x set)
  (cond ((null? set) false)
        ((equal? x (car set)) true)
        (else (element-of-set? x (cdr set)))))

(define (encode-symbol symbol tree)
  (if (leaf? tree)
      (if (eq? symbol (symbol-leaf tree))
          '()
          (error "bad symbol: The symbol is not in the tree at all!" symbol))
      (let ((left (left-branch tree)))
        (if (element-of-set? symbol (symbols left))
            (cons 0 (encode-symbol symbol left))
            (cons 1 (encode-symbol symbol (right-branch tree)))))))


(define pairs1 '((A 1) (B 2) (C 4) (D 8) (E 16)))
(define pairs2 '((A 1) (B 2) (C 4) (D 8) (E 16) (F 32) (G 64) (H 128) (I 256) (J 512)))

(generate-huffman-tree pairs1)
(generate-huffman-tree pairs2)
