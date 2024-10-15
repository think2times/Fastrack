(define (make-vect x y)
  (cons x y))

(define (xcor-vect vector)
  (car vector))

(define (ycor-vect vector)
  (cdr vector))

(define (add-vect v1 v2)
  (make-vect (+ (xcor-vect v1)
                (xcor-vect v2))
             (+ (ycor-vect v1)
                (ycor-vect v2))))

(define (sub-vect v1 v2)
  (make-vect (- (xcor-vect v1)
                (xcor-vect v2))
             (- (ycor-vect v1)
                (ycor-vect v2))))

(define (scale-vect s v)
  (make-vect (* s (xcor-vect v))
             (* s (ycor-vect v))))

(define (make-frame origin edge1 edge2)
  (list origin edge1 edge2))

(define (origin-frame frame)
  (car frame))

(define (edge1-frame frame)
  (cadr frame))

(define (edge2-frame frame)
  (caddr frame))

(define (frame-coord-map frame)
  (lambda (v)
    (add-vect
     (origin-frame frame)
     (add-vect (scale-vect (xcor-vect v) (edge1-frame frame))
               (scale-vect (ycor-vect v) (edge2-frame frame))))))

(define (draw-line v1 v2)
  (cons v1 v2))

(define (start-segment segment)
  (car segment))

(define (end-segment segment)
  (cdr segment))

(define (segments->painter segment-list)
  (lambda (frame)
    (for-each
     (lambda (segment)
       (draw-line
        ((frame-coord-map frame)
         (start-segment segment))
        ((frame-coord-map frame)
         (end-segment segment))))
     segment-list)))

; 获取 frame 的四个顶点的坐标
(define (bl frame) (origin-frame frame))    ; 左下
(define (bt frame) (add-vect (bl frame) (edge1-frame frame)))   ; 左上
(define (rt frame) (add-vect (bt frame) (edge2-frame frame)))   ; 右上
(define (rl frame) (add-vect (bl frame) (edge2-frame frame)))   ; 右下

(define (outline-of-frame frame)
  (let ((below (draw-line (bl frame) (rl frame)))         ; 下面那条边
        (right (draw-line (rl frame) (rt frame)))         ; 右面那条边
        (top (draw-line (rt frame) (bt frame)))           ; 上面那条边
        (left (draw-line (bt frame) (bl frame))))         ; 左面那条边
    (segments->painter (list below right top left))))

       
(define origin (make-vect 0 0))
(define v1 (make-vect 3 4))
(define v2 (make-vect -4 3))

(define a-frame (make-frame origin v1 v2))
(paint (outline-of-frame a-frame))
