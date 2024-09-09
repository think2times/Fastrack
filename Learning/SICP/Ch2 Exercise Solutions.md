[Building Abstractions with Data]()

# 2.1 Introduction to Data Abstraction

## 2.1.1 Example: Arithmetic Operations for Rational Numbers

### Exercise 2.1
> Exercise 2.1: Define a better version of $make-rat$ that handles both positive and negative arguments. $make-rat$ should normalize the sign so that if the rational number is positive, both the numerator and denominator are positive, and if the rational number is negative, only the numerator is negative.
---
> 第一章学完了，今天开始学习第二章，目前还没有遇到什么问题，这道题也比较简单，只要注意到“分子分母同时为正，或者分子为负，分母为正，不需要改变符号；分子分母同时为负,或者分子为正,分母为负,分子分母都需要改变符号”这一点，就可以很容易地实现题目要求。
```
; (make-rat ⟨n⟩ ⟨d ⟩) returns the rational number whose numerator is the integer ⟨n⟩ and whose denominator is the integer ⟨d ⟩.
(define (make-rat n d)
  (let ((n (/ n (gcd n d)))
        (d (/ d (gcd n d))))
    ; 分子分母同时为正，或者分子为负，分母为正，不需要改变符号
    ; 分子分母同时为负,或者分子为正,分母为负,分子分母都需要改变符号
    (if (or (and (positive? n) (positive? d))
            (and (negative? n) (positive? d)))
        (cons n d)
        (cons (- 0 n) (- 0 d)))))

; (numer ⟨x⟩) returns the numerator of the rational number ⟨x⟩.
(define (numer x) (car x))

; (denom ⟨x⟩) returns the denominator of the rational number ⟨x⟩.
(define (denom x) (cdr x))

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

(define (equal-rat? x y)
  (= (* (numer x) (denom y))
     (* (numer y) (denom x))))

(define (print-rat x)
  (newline)
  (display (numer x))
  (display "/")
  (display (denom x)))


(print-rat (make-rat -1 2))
(print-rat (make-rat 1 2))

(define neg-one-half (make-rat -1 2))
(define one-third (make-rat 1 3))

(print-rat (add-rat neg-one-half one-third))
(print-rat (add-rat neg-one-half neg-one-half))
(print-rat (sub-rat neg-one-half one-third))
(print-rat (mul-rat neg-one-half one-third))
(print-rat (div-rat neg-one-half one-third))

; 执行结果
-1/2
1/2
-1/6
-1/1
-5/6
-1/6
-3/2
```
> 可以看出这里还是有改进空间，-1/1 写成 -1 就行，利用 $gcd$ 就可以实现，不过我暂时不改了，也许后面有道题目会让做这个事情，到时候再说。

## 2.1.2 Abstraction Barriers

### Exercise 2.2
> Consider the problem of representing line segments in a plane. Each segment is represented as a pair of points: a starting point and an ending point. Define a constructor make-segment and selectors start-segment and end-segment that define the representation of segments in terms of points. Furthermore, a point can be represented as a pair of numbers: the x coordinate and the y coordinate. Accordingly, specify a constructor make-point and selectors x-point and y-point that define this representation. Finally, using your selectors and constructors, define a procedure midpoint-segment that takes a line segment as argument and returns its midpoint (the point whose coordinates are the average of the coordinates of the endpoints). To try your procedures, you’ll need a way to print points:
```
(define (print-point p)
  (newline)
  (display "(")
  (display (x-point p))
  (display ",")
  (display (y-point p))
  (display ")"))
```
---
> 这道题目很简单，主要是为了检查我们是否理解了嵌套使用抽象数据结构的概念，有点像 Python 里的列表，每个列表元素也可以是列表。
```
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

; 线段中点坐标就是起点和终点横纵坐标的平均值
(define (midpoint-segment segment)
  (let ((start (start-segment segment))
        (end (end-segment segment)))
    (make-point (average (x-point start) (x-point end))
                (average (y-point start) (y-point end)))))


; 设置线段起点为(3, 5)，终点为(7, 7)，中点应该为(5, 6)
(define start (make-point 3 5))
(define end (make-point 7 7))
(define line (make-segment start end))
(print-point (midpoint-segment line))

; 执行结果
(5, 6)
```

### Exercise 2.3
> Implement a representation for rectangles in a plane. (Hint: You may want to make use of Exercise 2.2.) In terms of your constructors and selectors, create procedures that compute the perimeter and the area of a given rectangle. Now implement a different representation for rectangles. Can you design your system with suitable abstraction barriers, so that the same perimeter and area procedures will work using either representation?
---
> 首先借用 Exercise 2.2 的函数来表示矩形，我们已经有了线段的表示方法，那矩形就是2组平行且相等的线段，且邻边垂直。为了简单起见，把矩形左下角的顶点坐标设为(0, 0)，且一条边落在 x 轴上。然后采用矩形左边的那条边和对角线交点坐标来确定一个矩形，同样为了简便起见，把交点坐标设为(0, 0)。可以看出 $make-point, x-point, y-point$; $make-segment, start-segment, end-segment$; $make-rect, make-rect-by-meeting-point$; $get-line-length, get-perimeter, get-area$ 是四层不同的函数，某一层的函数实现逻辑的改变，不会影响到其他层的调用。
```
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

; 执行结果
矩形test-rect1周长为：24.000000282646763
矩形test-rect1面积为:35.00000070672435
矩形test-rect2周长为:24.000000282646763
矩形test-rect2面积为:35.00000070672435
```

## 2.1.3 What Is Meant by Data?

### Exercise 2.4
> Here is an alternative procedural representation of pairs. Forthisrepresentation, verify that $(car\ (cons\ x\ y))$ yields $x$ for any objects $x$ and $y$.
 ```
 (define (cons x y)
  (lambda (m) (m x y)))
 (define (car z)
  (z (lambda (p q) p)))
```
> Whatisthe corresponding definition of $cdr$? (Hint: To verify that this works, make use of the substitution model of Section 1.1.5.)
---
> 这道题很简单，只需要把 $car$ 改一个字母就行。
```
; 返回值是一个单参数的函数，它会把 cons 函数的两个数传给返回值函数
(define (cons x y)
  (lambda (m) (m x y)))

; 如果 z 是由 cons 函数创建的数据对，则 z 会把 (lambda (p q) p)) 作为参数
(define (car z)
  (z (lambda (p q) p)))

(define (cdr z)
  (z (lambda (p q) q)))


(define z (cons 3 4)) 
(car z) 
(cdr z) 

; 执行结果
3
4

; applicative-order
; (car (cons x y)) 
; (car (lambda (m) (m x y))) 
; ((lambda (m) (m x y)) (lambda (p q) p)) 
; ((lambda (p q) p) x y) 
; x 
```

### Exercise 2.5
> Show that we can represent pairs of nonnegative integers using only numbers and arithmetic operations if we represent the pair a and b as the integer that is the product 2a3b. Give the corresponding definitions of the procedures cons, car, and cdr.
---
> 这道题目难度也不大，只要实现一个辅助函数来计算结果中包含了几个 $base$ 的乘积即可。
```
; 计算 n 中最多包含几个 base 的积
(define (get-power n base)
  (define (iter k last)
    (if (= (remainder last base) 0)      ; 如果余数为0，说明能够被base整除，则次数 +1
        (iter (+ k 1) (/ last base))
        k))
  (iter 0 n))

(define (cons a b)
  (* (expt 2 a) (expt 3 b)))

(define (car z)
  (get-power z 2))

(define (cdr z)
  (get-power z 3))


(define p (cons 3 2))
(display p)
(newline)
(car p)
(cdr p)

; 执行结果
72
3
2
```

