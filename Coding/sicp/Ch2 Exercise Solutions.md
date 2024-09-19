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

### Exercise2.6
> In case representing pairs as procedures wasn’t mind-boggling enough, consider that, in a language that can manipulate procedures, we can get by without numbers (at least insofar as nonnegative integers are concerned) by implementing 0 and the operation of adding 1 as
```
(define zero (lambda (f) (lambda (x) x)))
(define (add-1 n)
  (lambda (f) (lambda (x) (f ((n f) x)))))
```
> This representation is known as $Church numerals$, after its inventor, Alonzo Church, the logician who invented the λ calculus.
> Define $one$ and $two$ directly (not in terms of $zero$ and $add-1$). (Hint: Use substitution to evaluate `(add-1 zero)`). Give a direct definition of the addition procedure + (not in terms  of repeated application of $add-1$).
---
> 这个题太难理解了，题目里的两个函数，zero 我搞明白了，也勉强能接受它跟 0 的作用相同，但是我始终理解不了为啥 $add-1$ 的作用是加一，明明是 `(f x)` 啊。
```
; 任何数加 0 都等于它本身。所以,表示 0 的函数，无论你给它传入什么函数 f 和参数 x，它都直接返回 x，相当于什么都不做。
; (lambda (f) ...) 定义了一个匿名函数，它接受一个函数 f 作为参数，并返回 (lambda (x) x)。
; (lambda (x) x) 定义了另一个匿名函数，它接受一个参数 x,并直接返回 x。
; 组合起来:zero 函数本质上就是一个恒等函数，无论你给它传入什么函数 f，它都会返回一个新的函数，这个新函数会直接返回它的输入 x。
; 这符合我们对 0 的理解————任何数加 0 等于它本身。
(define zero (lambda (f) (lambda (x) x)))

; 1. 把 (lambda (x) (square x)) 传给 zero 作为参数，返回新的函数 (lambda (x) x)
; 2. 再把 10 传给 (lambda (x) x)，得到原数 10
(display ((zero (lambda (x) (square x))) 10))    ; 输出是 10
(newline)

; n 必须是 Church Numeral，比如说上面定义的 zero
; 返回值是一个新的 Church Numeral，表示的值为 n + 1
(define (add-1 n)
  (lambda (f) (lambda (x) (f ((n f) x)))))


(display (((add-1 zero) square) 10))    ; 输出是 100
(newline)

; 1. 先用 f1 表示匿名函数 (lambda (x) (+ x 1))，则原式变为 ((zero f1) 0)
; 2. 把 zero 函数用它的定义替代，得到 (((lambda (f) (lambda (x) x)) f1) 0)
; 3. 把 f1 带入到 zero 的返回值函数，得到 ((lambda (x) x) 0)
; 4. (lambda (x) x) 函数会返回传入的参数，也就是0
((zero (lambda (x) (+ x 1))) 0)    ; 输出是 0

; 1. 把 zero 作为参数传入，得到 (lambda (f) (lambda (x) (f ((zero f) x))))
; 2. 先处理 (zero f)，根据上面我们对 zero 函数的分析，无论传入什么函数作为参数，它都返回 (lambda (x) x)
; 3. 则 ((zero f) x) 就是 x，(lambda (f) (lambda (x) (f x)))，也就是无论传入什么 f 和 x，都会返回 (f x)
(define one (add-1 zero))

; 根据上面的分析，下面的程序相当于执行 ((lambda (x) (+ x 1)) 0), 也就是 0 + 1
((one (lambda (x) (+ x 1))) 0)    ; 输出是 1

; 1. 把 one 作为参数传入，得到 (lambda (f) (lambda (x) (f ((one f) x))))
; 2. 根据上面的分析，((one f) x) 会返回 (f x)
; 3. 所以下面的函数无论传入什么 f 和 x，都会返回 (f (f x))
(define two (add-1 one))

; 根据上面的分析,下面的程序相当于执行 ((lambda (x) (+ x 1)) ((lambda (x) (+ x 1)) 0)), 也就是 ((0 + 1) + 1)
((two (lambda (x) (+ x 1))) 0)    ; 输出是 2

; 以此类推，可以用如下方式直接定义 one, two, three
(define new-one (lambda (f) (lambda (x) (f x)))) 
(define new-two (lambda (f) (lambda (x) (f (f x)))))
(define three (lambda (f) (lambda (x) (f (f (f x)))))) 

; 虽然不理解为啥 add-1 可以表示加一，但是按照上面的规律，加法可以按下面的函数来定义
(define (add a b) 
  (lambda (f) 
    (lambda (x) ((a f) ((b f) x)))))

; 下面的程序相当于 ((two square) (square 2))
; 进一步替代得到 (square (square (square 2)))
(((add two one) square) 2)      ; 输出是 256

; 执行结果
10
100
0
1
2
256
```

## 2.1.4 Extended Exercise: Interval Arithmetic

### 2.7
> Alyssa’s program is incomplete because she has not specified the implementation of the interval abstraction. Here is a definition of the interval constructor:
` (define (make-interval a b) (cons a b))`
> Define selector $supper-bound$ and $lower-bound$ to complete the implementation.
---
> 这道题目难度不大，比起前面的选择函数，就是多了一个取最小值为下界，最大值为上界的步骤，直接利用现成的 $min, max$ 即可。
```
; x 表示某个区间
(define (lower-bound x) (min (car x) (cdr x)))

(define (upper-bound x) (max (car x) (cdr x)))

(define helper (make-interval 1.0 1.0))
(define r1 (make-interval 6.12 7.48))
(define r2 (make-interval 4.465 4.935))

; 计算并联电路的电阻，注意这里不能化简成 r1*r2/(r1+r2) 的形式
(define (parallel-resistance r1 r2)
  (div-interval helper (add-interval (div-interval helper r1)
                                     (div-interval helper r2))))
                                     
(display (parallel-resistance r1 r2))

; 执行结果
[2.581558809636278, 2.97332259363673]
```

### Exercise 2.8
＞ Using reasoning analogous to Alyssa’s, describe how the difference of two intervals may be computed. Define a corresponding subtraction procedure, called $sub-interval$.
---
> 这道题目也比较简单，只要注意到区间之差的下界是被减区间的下界减去另一个区间的上界，上界是被减区间的上界减去另一个区间的下界即可。
```
; 计算 x-y 的结果
(define (sub-interval x y)
  (make-interval (- (lower-bound x) (upper-bound y))
                 (- (upper-bound x) (lower-bound y))))

(define r1 (make-interval 6.12 7.48))
(define r2 (make-interval 4.465 4.935))

(display (sub-interval r1 r2))

; 执行结果
[1.1850000000000005, 3.0150000000000006]
```

### Exercise 2.9
> The $width$ of an interval is half of the difference between its upper and lower bounds. The width is a measure of the uncertainty of the number specified by the interval. For some arithmetic operations the width of the result of combining two intervals is a function only of the widths of the argument intervals, whereas for others the width of the combination is not a function of the widths of the argument intervals. Show that the width of the sum (or difference) of two intervals is a function only of the widths of the intervals being added (or subtracted). Give examples to show that this is not true for multiplication or division.
---
> 这道题目没有任何难度，只要把原来的区间宽度和经过加减之后的区间宽度表示出来，它们的关系也就一目了然了。
```
; 计算区间的宽度
(define (get-width x)
  (/ (- (upper-bound x) (lower-bound x)) 2))


(define r1 (make-interval 6.12 7.48))
(define r2 (make-interval 4.465 4.935))

(display (get-width r1))
(newline)
(display (get-width r2))
(newline)
(display (get-width (add-interval r1 r2)))
(newline)
(display (get-width (sub-interval r1 r2)))
(newline)

; 执行结果
0.6800000000000002
0.23499999999999988
0.9149999999999991
0.915
```
> 根据执行结果可以看出，加减之后的区间宽度等于原来两个区间宽度之和。

### Exercise 2.10
> Ben Bitdiddle, an expert systems programmer, looks over Alyssa’s shoulder and comments that it is not clear what it means to divide by an interval that spans zero. Modify Alyssa’s code to check for this condition and to signal an error if it occurs.
---
> 这道题目也很简单，只要加一个区间内是否包含0的判断就行了
```
(define (div-interval x y)
  (if (and (<= (lower-bound y) 0) (>= (upper-bound x) 0))
      (error "被除区间包含0！")
      (mul-interval
       x
       (make-interval (/ 1.0 (upper-bound y))
                      (/ 1.0 (lower-bound y))))))


(define r1 (make-interval 6.12 7.48))
(define r2 (make-interval 4.465 4.935))
(display-interval (div-interval r1 r2))
(newline)

(define a (make-interval 6.12 7.48))
(define b (make-interval -4.465 4.935))
(display-interval (div-interval a b))
```
> 执行结果
![Alt text](<images/exer 2.10.png>)

### Exercise 2.11
> In passing, Ben also cryptically comments: “By testing the signs of the endpoints of the intervals, it is possible to break $mul-interval$ into nine cases, only one of which requires more than two multiplications.” Rewrite this procedure using Ben’s suggestion.
> After debugging her program, Alyssa shows it to a potential user, who complains that her program solves the wrong problem. He wants a program that can deal with numbers represented as a center value and an additive tolerance; for example, he wants to work with intervals such as 3.5±0.15 rather than [3.35, 3.65]. Alyssa returns to her desk and fixes this problem by supplying an alternate constructor and alternate selectors:
```
(define (make-center-width c w)
  (make-interval (- c w) (+ c w)))
(define (center i)
  (/ (+ (lower-bound i) (upper-bound i)) 2))
(define (width i)
  (/ (- (upper-bound i) (lower-bound i)) 2))
```
> Unfortunately, most of Alyssa’s users are engineers. Real engineering situations usually involve measurements with only a small uncertainty, measured as the ratio of the width of the interval to the midpoint of the interval. Engineers usually specify percentage tolerances on the parameters of devices, as in the resistor specifications given earlier.
---
> 这道题目难度并不大，就是有点麻烦，要把每一种情况的上界和下界都分析出来。至于区间采用置信区间的表示方法，只要用宽度的一半除以中间值就行了。
```
; 把 w 改为百分比形式
(define (make-center-width center percent)
  (let ((tolerance (* center (/ percent 100))))
    (make-interval (- center tolerance) (+ center tolerance))))

(define (center i)
  (average (lower-bound i) (upper-bound i)))

(define (percent i)
  (* (/ (/ (- (upper-bound i) (lower-bound i)) 2)
        (center i))
     100))

(define (display-interval-tolerance i) 
  (newline)
  (display (center i))
  (display " ± ")
  (display (percent i))
  (display "%"))

; 记 x 的下界为 x1，上界为 x2；记 y 的下界为 y1，上界为 y2
; 将他们按 x1 x2 y1 y2 从左到右排序，并按位置记为 1, 2, 3, 4
; 则按照 x 和 y 的区间端点数字的符号，可以分成以下9种情况：
; - - - -   min: 2*4, max: 1*3
; - - - +   min: 1*4, max: 1*3
; - - + +   min: 1*4, max: 2*3
; - + - -   min: 2*3, max: 1*3
; - + - +   min: min(1*4, 2*3), max: max(1*3, 2*4)
; - + + +   min: 1*4, max: 2*4
; + + - -   min: 2*3, max: 1*4
; + + - +   min: 2*3, max: 2*4
; + + + +   min: 1*3, max: 2*4
(define (mul-interval x y)
  (let ((x1 (lower-bound x))
        (x2 (upper-bound x))
        (y1 (lower-bound y))
        (y2 (upper-bound y))
        (p1 (* (lower-bound x) (lower-bound y)))    ; 即 1*3
        (p2 (* (lower-bound x) (upper-bound y)))    ; 即 1*4
        (p3 (* (upper-bound x) (lower-bound y)))    ; 即 2*3
        (p4 (* (upper-bound x) (upper-bound y))))   ; 即 2*4
    (cond ((and (negative? x2) (negative? y2)) (make-interval p4 p1))
          ((and (negative? x2) (negative? y1) (positive? y2)) (make-interval p2 p1))
          ((and (negative? x2) (positive? y1)) (make-interval p2 p3))
          ((and (negative? x1) (positive? x2) (negative? y2)) (make-interval p3 p1))
          ((and (negative? x1) (positive? x2) (negative? y1) (positive? y2)) (make-interval (min p2 p3) (max p1 p4)))
          ((and (negative? x1) (positive? x2) (positive? y1)) (make-interval p2 p4))
          ((and (positive? x1) (negative? y2)) (make-interval p3 p2))
          ((and (positive? x1) (negative? y1) (positive? y2)) (make-interval p3 p4))
          ((and (positive? x1) (positive? y1)) (make-interval p1 p4)))))


(define a (make-interval -6.12 7.48))
(define b (make-interval -4.465 4.935))
(display-interval (mul-interval a b))
(display-interval-tolerance (mul-interval a b))

; 执行结果
[-33.3982, 36.9138]
1.7577999999999996 ± 2000.0000000000007%
```

### Exercise 2.12 Defineaconstructor $make-center-percent$ that takes a center and a percentage tolerance and produces the desired interval. You must also define a selector $percent$ that produces the percentage tolerance for a given interval. The $center$ selector is the same as the one shown above.
---
> 我以为这是上道题的要求，已经实现了。。
```
; 把 w 改为百分比形式
(define (make-center-width c w)
  (let ((tolerance (* c w)))
    (make-interval (- c tolerance) (+ c tolerance))))

(define (center i)
  (average (lower-bound i) (upper-bound i)))

(define (percent i)
  (* (/ (/ (- (upper-bound i) (lower-bound i)) 2)
        (center i))
     100))

(define (display-interval-tolerance i) 
  (newline)
  (display (center i))
  (display " ± ")
  (display (percent i))
  (display "%"))

(define a (make-interval 6.12 7.48))
(define b (make-interval 4.465 4.935))


(display-interval-tolerance a)
(display-interval-tolerance b)

; 执行结果
6.800000000000001 ± 10.000000000000002%
4.699999999999999 ± 4.999999999999998%
```

### Exercise 2.13
> Show that under the assumption of small percentage tolerances there is a simple formula for the approximate percentage tolerance of the product of two intervals in terms of the tolerances of the factors. You may simplify the problem by assumingthat all numbers are positive.
> After considerable work, Alyssa P. Hacker delivers her finished system. Several years later, after she has forgotten all about it, she gets a frenzied call from an irate user, Lem E.  Tweakit. It seems that Lem has noticed that the formula for parallel resistors can be written in two algebraically equivalent ways:
$\frac{R_1 R_2}{R_1+R_2}$ and $\frac{1}{\frac{1}{R_1}+\frac{1}{R_2}}$
> He has written the following two programs, each of which computes the parallel-resistors formula differently:
```
(define (par1 r1 r2)
  (div-interval (mul-interval r1 r2)
                (add-interval r1 r2)))

(define (par2 r1 r2)
  (let ((one (make-interval 1 1)))
    (div-interval
     one (add-interval (div-interval one r1)
                       (div-interval one r2)))))
```
> Lem complains that Alyssa’s program gives different answers for the two ways of computing. This is a serious complaint.
---
> 这道题一是要修改乘法函数，二是要演示两种计算并联电阻的方法计算的结果不一致。
```
(define (mul-interval x y)
  (let ((cx (center x))
        (cy (center y))
        (px (/ (percent x) 100))
        (py (/ (percent y) 100)))
    (make-interval (* (- cx (* cx px)) (- cy (* cy py)))
                   (* (+ cx (* cx px)) (+ cy (* cy py))))))

(define r1 (make-interval 6.12 7.48))
(define r2 (make-interval 4.465 4.935))

(display-interval-tolerance (par1 r1 r2))
(display-interval-tolerance (par2 r1 r2))

; 执行结果
2.844199964577264 ± 22.613352145193332%
2.777440701636504 ± 7.05260392723452%
```

### Exercise 2.14
> Demonstrate that Lem is right. Investigate the behavior of the system on a variety of arithmetic expressions. Make some intervals A and B, and use them in computing the expressions A/A and A/B. You will get the most insight by using intervals whose width is a small percentage of the center value. Examine the results of the computation in center-percent form (see Exercise 2.12).
---
```
(define r1 (make-interval 6.12 7.48))
(define r2 (make-interval 4.465 4.935))

(display-interval (div-interval r1 r1))
(display-interval (div-interval r1 r2))
(newline)
(display-interval-tolerance (div-interval r1 r1))
(display-interval-tolerance (div-interval r1 r2))

; 执行结果
[0.8181818181818182, 1.222222222222222]
[1.2401215805471126, 1.6752519596864504]

1.02020202020202 ± 19.801980198019795%
1.4576867701167815 ± 14.925373134328357%
```
> 根据执行结果来看，Lem显然是对的，对于 A/A，答案显然应该是 1 才对，但是程序计算出来的却是一个相对很大的范围，这是因为计算区间除法时，我们并没有定义“相等”这个概念，所以计算 A/A 时，它也按照通用的方法去计算了。

### Exercise 2.15
> Eva Lu Ator, another user, has also noticed the different intervals computed by different but algebraically equivalent expressions. She says that a formula to compute with intervals using Alyssa’s system will produce tighter error bounds if it can be written in such a form that no variable that represents an uncertain number is repeated. Thus, she says, par2 is a “better” program for parallel resistances than par1. Is she right? Why?
---
> Eva 说的是对的，对于练习 2.13 计算出的两个答案，par2 更准确，跟书上给出的答案是一致的，至于原因我觉得应该是区间之间的运算每次都会增加不确定性，par2 其实只有相加那一步是两个区间进行运算，其他的都可以看作确定数字与区间的运算，没有增加额外的不确定性；而 par1 进行了3次区间之间的运算————乘法、加法和除法，乘法和除法都会使结果变得不确定。

### Exercise 2.16
> Explain, in general, why equivalent algebraic expressions may lead to different answers. Can you devise an interval-arithmetic package that does not have this shortcoming, or is this task impossible? (Warning: This problem is very difficult.)
---
```
(define a (make-interval 2 4))
 
(define b (make-interval -2 0))
 
(define c (make-interval 3 8))
 
(define x (mul-interval a (add-interval b c)))
 
(define y (add-interval (mul-interval a b)
                        (mul-interval a c)))


(display-interval x)
(display-interval y)

; 执行结果
[2, 32]
[-2, 32]
```
> 根据上面的结果可以看到，区间运算连乘法分配律都无法保证。至于有没有无缺陷的区间运算规则，我大概想了一下，没有什么头绪，就没继续想了。。

# 2.2 Hierarchical Data and the Closure Property

## 2.2.1 Representing Sequences

### Exercise 2.17
> Define a procedure last-pair that returns the list that contains only the last element of a given (nonempty) list:
```
(last-pair (list 23 72 149 34))
(34)
```
---
> 这道题难度不大，而且借用之前的 length 和 list-ref 可以很轻松的完成这道题目的要求，不过我还是选择不用这两个函数，通过判断 list 最后一个元素是否为空来做。
```
(define (last-pair list1)
  (let ((last (car list1)))
    (if (null? (cdr list1))
        last
        (last-pair (cdr list1)))))


(last-pair (list 23 72 149 34))

; 执行结果
34
```

### Exercise 2.18
> Define a procedure reverse that takes a list as argument and returns a list of the same elements in reverse order:
```
(reverse (list 1 4 9 16 25))
(25 16 9 4 1)
```
---
> 可能是因为前两天发高烧脑子不好使，看到这道题我才忽然反应过来，这一节不就是在实现“链表”这个数据结构吗？乍一看，这道题利用 length 和 list-ref 很容易实现，但是我想了半天也没有做出来。最后想到了每次读取列表中的第一个元素，构造一个新的列表，不过也没有实现出来，还是上网查了资料，才明白怎么做。
```
(define (reverse items) 
  (define (iter items result) 
    (if (null? items) 
        result 
        (iter (cdr items) (cons (car items) result)))) 
  
  (iter items nil)) 
  
  
(reverse (list 1 4 9 16 25))

; 执行结果
'(25 16 9 4 1)

; 如果 nil 没有定义的话，可以用下面的语句自己定义
(define nil '())
```