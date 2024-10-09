#lang racket

(require "../modules/base.rkt")


(define (print-point p)
  (newline)
  (display "(")
  (display (x-point p))
  (display ", ")
  (display (y-point p))
  (display ")"))

(define (make-point x y)
  (cons x y))

(define (x-point p) (car p))

(define (y-point p) (cdr p))

(define (make-segment start end)
  (cons start end))

(define (start-segment segment)
  (car segment))

(define (end-segment segment)
  (cdr segment))

; 用左下的顶点和经过该顶点的两条邻边来确定一个矩形，为简单起见，左下的顶点坐标设为(0, 0)
; length, width 分别表示矩形的长和宽
(define (make-rect length width)
  (let ((left-bottom (make-point 0 0)))
    (cons (make-segment left-bottom (make-point (car left-bottom) (+ (cdr left-bottom) width)))    ; 竖直的那条边
          (make-segment left-bottom (make-point (+ (car left-bottom) length) (cdr left-bottom))))))    ; 水平的那条边

; 用矩形的对角线交点和左边的边来确定一个矩形,为简单起见,对角线交点坐标设为(0, 0)
; left-line 表示左边的边
(define (make-rect-by-meeting-point left-line)
  (cons left-line (make-segment (start-segment left-line) (make-point (- 0 (x-point (start-segment left-line)))
                                                                      (y-point (start-segment left-line))))))

; 用两点间距离公式 d = sqrt(x^2 + y^2) 计算线段的长度
(define (get-line-length segment)
  (sqrt (+ (square (- (x-point (end-segment segment))
                      (x-point (start-segment segment))))
           (square (- (y-point (end-segment segment))
                      (y-point (start-segment segment)))))))

; 计算矩形的周长
(define (get-perimeter rect)
  (* 2 (+ (get-line-length (car rect))
          (get-line-length (cdr rect)))))

; 计算矩形的面积
(define (get-area rect)
  (* (get-line-length (car rect))
     (get-line-length (cdr rect))))


; 设置一个长为7宽为5的矩形
(define test-rect1 (make-rect 7 5))

(display "矩形test-rect1周长为：")
(display (get-perimeter test-rect1))
(newline)
(display "矩形test-rect1面积为:")
(display (get-area test-rect1))
(newline)

; 设置一个长为7宽为5的矩形
(define A (make-point -3.5 -2.5))
(define B (make-point -3.5 2.5))
(define left-line (make-segment A B))
(define test-rect2 (make-rect-by-meeting-point left-line))
(display "矩形test-rect2周长为:")
(display (get-perimeter test-rect2))
(newline)
(display "矩形test-rect2面积为:")
(display (get-area test-rect2))
(newline)