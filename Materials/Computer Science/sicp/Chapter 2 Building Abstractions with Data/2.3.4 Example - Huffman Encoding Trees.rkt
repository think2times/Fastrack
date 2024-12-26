#lang racket


; Generating Huffman trees
; The idea is to arrange the tree so that the symbols with the lowest frequency
; appear farthest away from the root. Begin with the set of leaf nodes,
; containing symbols and their frequencies, as determined by the initial
; data fromwhichthecodeistobeconstructed.Nowfindtwoleaveswith
; the lowest weights and merge them to produce a node that has these
; two nodes as its left and right branches. The weight of the new node is
; the sum of the two weights. Remove the two leaves from the original
; set and replace them by this new node. Now continue this process. At
; each step, merge two nodes with the smallest weights, removing them
; from the set and replacing them with a node that has these two as its
; left and right branches. The process stops when there is only one node
; left, which is the root of the entire tree.

; The algorithm does not always specify a unique tree, because there may
; not be unique smallest-weight nodes at each step. Also, the choice of the
; order in which the two nodes are merged is arbitrary.


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

; The decoding procedure
(define (decode bits tree)
  (define (decode-1 bits current-branch)
    (if (null? bits)
        '()
        (let ((next-branch
               (choose-branch (car bits) current-branch)))
          (if (leaf? next-branch)
              (cons (symbol-leaf next-branch)
                    (decode-1 (cdr bits) tree))
              (decode-1 (cdr bits) next-branch)))))
  (decode-1 bits tree))

(define (choose-branch bit branch)
  (cond ((= bit 0) (left-branch branch))
        ((= bit 1) (right-branch branch))
        (else (error "bad bit: CHOOSE-BRANCH" bit))))

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
