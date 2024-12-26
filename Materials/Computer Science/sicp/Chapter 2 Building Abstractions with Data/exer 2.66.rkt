#lang racket

(define (make-tree entry left right)
  (list entry left right))

(define (entry tree) (car tree))

(define (left-branch tree) (cadr tree))

(define (right-branch tree) (caddr tree))

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

(define (lookup given-key set-of-records)
  (if (null? set-of-records)
      false
      (let ((root (entry set-of-records)))
        (cond ((= given-key root) true)
              ((< given-key root) (lookup given-key (left-branch set-of-records)))
              (else (lookup given-key (right-branch set-of-records)))))))


(define test (list->tree (list 1 2 3 4 5 6 7 8 9)))
(lookup 7 test)
(lookup 10 test)
