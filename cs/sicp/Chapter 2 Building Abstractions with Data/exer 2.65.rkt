#lang racket


(define (entry tree) (car tree))

(define (left-branch tree) (cadr tree))

(define (right-branch tree) (caddr tree))

(define (make-tree entry left right)
  (list entry left right))

(define (tree->list-2 tree)
  (define (copy-to-list tree result-list)
    (if (null? tree)
        result-list
        (copy-to-list (left-branch tree)
                      (cons (entry tree)
                            (copy-to-list
                             (right-branch tree)
                             result-list)))))
  (copy-to-list tree '()))

(define (list->tree elements)
  (car (partial-tree elements (length elements))))

(define (partial-tree elts n)
  (if (= n 0)
      (cons '() elts)
      (let ((left-size (quotient (- n 1) 2)))
        (let ((left-result
               (partial-tree elts left-size)))
          (let ((left-tree (car left-result))
                (non-left-elts (cdr left-result))
                (right-size (- n (+ left-size 1))))
            (let ((this-entry (car non-left-elts))
                  (right-result
                   (partial-tree
                    (cdr non-left-elts)
                    right-size)))
              (let ((right-tree (car right-result))
                    (remaining-elts
                     (cdr right-result)))
                (cons (make-tree this-entry
                                 left-tree
                                 right-tree)
                      remaining-elts))))))))

(define (union-tree tree1 tree2) 
  (define (union-set set1 set2) 
    (cond ((null? set2) set1) 
          ((null? set1) set2)
          (else (let ((s1 (car set1))
                      (s2 (car set2)))
                  (cond ((= s1 s2) (cons s1 (union-set (cdr set1) (cdr set2))))
                        ((< s1 s2) (cons s1 (union-set (cdr set1) set2)))
                        (else (cons s2 (union-set set1 (cdr set2)))))))))
  (list->tree (union-set (tree->list-2 tree1) (tree->list-2 tree2))))
  
(define (intersection-tree tree1 tree2) 
  (define (intersection-set set1 set2) 
    (if (or (null? set1) (null? set2))
        '()
        (let ((s1 (car set1))
              (s2 (car set2)))
          (cond ((= s1 s2) (cons s1 (intersection-set (cdr set1) (cdr set2))))
                ((< s1 s2) (intersection-set (cdr set1) set2))
                (else (intersection-set set1 (cdr set2)))))))
  (list->tree (intersection-set (tree->list-2 tree1) (tree->list-2 tree2)))) 


(define tree1 (list->tree (list 1 3 5 7 9 11)))
(define tree2 (list->tree (list 2 4 6 7 8 9 10)))

(intersection-tree tree1 tree2)
(union-tree tree1 tree2)
