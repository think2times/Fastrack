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

### Exercise 2.19
> Consider the change-counting program of Section 1.2.2. It would be nice to be able to easily change the currency used by the program, so that we could compute the number of ways to change a British pound, for example. As the program is written, the knowledge of the currency is distributed partly into the procedure $first-denomination$ and partly into the procedure $count-change$ (which knows that there are five kinds of U.S. coins). It would be nicer to be able to supply a list of coins to be used for making change.
> We want to rewrite the procedure $cc$ so that its second argument is a list of the values of the coins to use rather than an integer specifying which coins to use. We could then have lists that defined each kind of currency:
```
(define us-coins (list 50 25 10 5 1))
(define uk-coins (list 100 50 20 10 5 2 1 0.5))
```
> We could then call $cc$ as follows:
```
(cc 100 us-coins)
292
```
> To do this will require changing the program $cc$ somewhat. It will still have the same form, but it will access its second argument differently, as follows:
```
(define (cc amount coin-values)
  (cond ((= amount 0) 1)
        ((or (< amount 0) (no-more? coin-values)) 0)
        (else
         (+ (cc amount
                (except-first-denomination
                 coin-values))
            (cc (- amount
                   (first-denomination
                    coin-values))
                coin-values)))))
```
> Define the procedures $first-denomination$, $except-firstdenomination$, and $no-more?$ in terms of primitive operations on list structures. Does the order of the list $coin-values$ affect the answer produced by $cc$? Why or why not?
---
> 这道题题目很长，看着挺唬人的，但实际上非常简单，只要把 coin-values 当作列表来处理就行了。
```
(define (no-more? items)
  (null? items))

(define (except-first-denomination items)
  (cdr items))

(define (first-denomination items)
  (car items))

(define us-coins (list 50 25 10 5 1))
(define uk-coins (list 100 50 20 10 5 2 1 0.5))

(cc 100 us-coins)
(cc 100 uk-coins)

; 借用上道题的列表翻转函数
(cc 100 (reverse us-coins))
(cc 100 (reverse uk-coins))

; 执行结果
292
104561
292
104561
```
> 从执行结果来看，零钱币值的顺序是不影响兑换的方法数的，这是因为 cc 算法覆盖了所有可能的情况，无论从哪种币值先开始兑换，都不会影响总的结果。

### Exercise 2.20
> The procedures +, *, and list take arbitrary numbers of arguments. One way to define such procedures is to use $define$ with $dotted-tail notation$. In a procedure definition, a parameter list that has a dot before the last parameter name indicates that, when the procedure is called, the initial parameters (if any) will have as values the initial arguments, as usual, but the final parameter’s value will be a list of any remaining arguments. For instance, given the definition
`(define (f x y . z) ⟨body⟩)`
> the procedure f can be called with two or more arguments. If we evaluate
`(f 1 2 3 4 5 6)`
> then in the body of f, x will be 1, y will be 2, and z will be the list (3 4 5 6). Given the definition
`(define (g . w) ⟨body⟩)`
> the procedure g can be called with zero or more arguments. If we evaluate
`(g 1 2 3 4 5 6)`
> then in the body of g, w will be the list (1 2 3 4 5 6).
> Use this notation to write a procedure $same-parity$ that takes one or more integers and returns a list of all the arguments that have the same even-odd parity as the first argument. For example,

```
(same-parity 1 2 3 4 5 6 7)
(1 3 5 7)
(same-parity 2 3 4 5 6 7)
(2 4 6)
```
---
> 这道题也是看着唬人，题干挺长，但是主要在介绍如何定义参数个数不定的函数，真正的题目就最后一段，就是要根据第一个参数的奇偶性，把后面参数中跟第一个参数奇偶性相同的找出来。
```
(define (same-parity x . y)
  (define (iter items r result)
    (cond ((null? items) result)
          ((= r (remainder (car items) 2)) (iter (cdr items) r (cons (car items) result)))
          (else (iter (cdr items) r result))))
  (let ((r (remainder x 2)))
    (reverse (iter y r (cons x nil)))))


(same-parity 1 2 3 4 5 6 7)
(same-parity 2 3 4 5 6 7)
(same-parity 2)

; 执行结果
'(1 3 5 7)
'(2 4 6)
'(2)
```

### Exercise 2.21 
> The procedure square-list takes a list of numbers as argument and returns a list of the squares of those numbers.
```
(square-list (list 1 2 3 4))
(1 4 9 16)
```
> Here are two different definitions of square-list. Complete both of them by filling in the missing expressions:
```
(define (square-list items)
  (if (null? items)
      nil
      (cons <??> <??>)))

(define (square-list-by-map items)
  (map <??> <??>))
```
---
> 这道题目很简单，只要把例子里的程序稍微修改就行，对比之下更显得 map 的强大。
```
(define (square-list items)
  (if (null? items)
      nil
      (cons (square (car items))
            (square-list (cdr items)))))

(define (square-list-by-map items)
  (map square items))


(square-list (list 1 2 3 4))
(square-list-by-map (list 1 2 3 4))

; 执行结果
'(1 4 9 16)
'(1 4 9 16)
```

### Exercise2.22
> Louis Reasoner tries to rewrite the first $square-list$ procedure of Exercise 2.21 so that it evolves an iterative process:
```
(define (square-list items)
  (define (iter things answer)
    (if (null? things)
        answer
        (iter (cdr things)
              (cons (square (car things))
                    answer))))
  (iter items nil))
```
> Unfortunately, defining $square-list$ this way produces the answer list in the reverse order of the one desired. Why?
> Louis then tries to fix his bug by interchanging the arguments to $cons$:
```
(define (square-list items)
  (define (iter things answer)
    (if (null? things)
        answer
        (iter (cdr things)
              (cons answer
                    (square (car things))))))
  (iter items nil))
```
> This doesn’t work either. Explain.
---
> 第一部分的代码得到的答案是倒序的，这个是因为程序里每次都把新加入的元素放到结果列表的开头；第二部分得到的答案是这样的：'(((((() . 1) . 9) . 25) . 49) . 81)，虽然顺序对了，这并不是我们想要的列表，其实只要在调用第一部分代码后再次调用之前练习里的 reverse 函数就可以得到顺序正确的列表了。

### Exercise2.23
> The procedure for-each is similar to map. It takes as arguments a procedure and a list of elements. How ever, rather than forming a list of the results, for-each just  applies the procedure to each of the elements in turn, from left to right. The values returned by applying the procedure to the elements are not used at all—$for-each$ is used with  procedures that perform an action, such as printing. For example,
```
(for-each(lambda(x)
           (newline)
           (display x))
         (list5732188))

57
321
88
```
> The value returned by the call to $for-each$ (not illustrated above) can be something arbitrary, such as true. Give an implementation of $for-each$.
---
> 这道题开始我不知道怎么连续执行 2 条程序，所以不知道怎么处理，后来上网查了一下，发现 $cond$ 可以直接把多条语句放到一起执行，然后这道题就没有什么难度了。
```
(define (for-each f items)
  (cond ((not (null? items))
         (f (car items))
         (for-each f (cdr items)))))


(define test (list 57 321 88))
(for-each (lambda(x) (newline) (display x))
          test)

(newline)

(for-each (lambda(x) (newline) (display (square x)))
          test)

; 执行结果
57
321
88

3249
103041
7744
```

## 2.2.2 Hierarchical Structures

### Exercise 2.24
> Suppose we evaluate the expression `(list 1 (list 2 (list 3 4)))`. Give the result printed by the interpreter, the corresponding box-and-pointer structure, and the interpretation of this as a tree (as in Figure 2.6).
---
> 解释器执行结果为：'(1 (2 (3 4)))
> 另外两种表示方法见下图：
![Alt text](<images/exer 2.24-tree.png>)

![Alt text](<images/exer 2.24-box-and-pointer.png>)

### Exercise 2.25
> Give combinations of cars and cdrs that will pick 7 from each of the following lists:
```
(1 3 (5 7) 9)
((7))
(1 (2 (3 (4 (5 (6 7))))))
```
---
> 纯看耐心。。
```
; 先创建这些要求的列表
(list 1 3 (list 5 7) 9)
(list (list 7))
(list 1 (list 2 (list 3 (list 4 (list 5 (list 6 7))))))

; 根据它们的结构依次定位到 7
(car (cdr (car (cdr (cdr (list 1 3 (list 5 7) 9))))))
(car (car (list (list 7))))
(car (cdr (car (cdr (car (cdr (car (cdr (car (cdr (car (cdr (list 1 (list 2 (list 3 (list 4 (list 5 (list 6 7))))))))))))))))))

; 执行结果
'(1 3 (5 7) 9)
'((7))
'(1 (2 (3 (4 (5 (6 7))))))
7
7
7
```

### Exercise 2.26
> Suppose we define x and y to be two lists:
```
(define x (list 1 2 3))
(define y (list 4 5 6))
```
> What result is printed by the interpreter in response to evaluating each of the following expressions:
```
(append x y)
(cons x y)
(list x y)
```
---
> 结果如下所示：
```
'(1 2 3 4 5 6)
'((1 2 3) 4 5 6)
'((1 2 3) (4 5 6))
```

### Exercise 2.27
> Modify your reverse procedure of Exercise 2.18 to produce a deep-reverse procedure that takes a list as argument and returns as its value the list with its elements reversed and with all sublists deep-reversed as well. For example,
```
(define x (list (list 1 2) (list 3 4)))
x
((1 2) (3 4))
(reverse x)
((3 4) (1 2))
(deep-reverse x)
((4 3) (2 1))
```
---
> 这道题难度还是挺大的，我开始想用 reverse 实现，比起原来的 reverse 函数，deep-reverse 需要在 items 不为空的情况下，额外判断 `(car items)` 是否为 pair，虽然也能做，但是步骤有点麻烦，最后在网上发现一个使用 append 的版本，程序非常简单，而且逻辑也很清楚。
```
(define (deep-reverse-by-reverse items) 
  (define (iter items result) 
    (if (null? items) 
        result 
        (if (pair? (car items)) 
            (let ((x (iter (car items) nil))) 
              (iter (cdr items) (cons x result))) 
            (iter (cdr items) (cons (car items) result))))) 
  (iter items nil))

(define (deep-reverse items)
  (if (pair? items)
      (append (deep-reverse (cdr items))
              (list (deep-reverse (car items))))
      items))


(define x (list (list 1 2) (list 3 4)))

x
(reverse x)
(deep-reverse x)
```

### Exercise2.28
> Write a procedure fringe that takes as argument a tree (represented as a list) and returns a list whose elements are all the leaves of the tree arranged in left-to-right order. For example,
```
(define x (list (list 1 2) (list 3 4)))
(fringe x)
(1 2 3 4)
(fringe (list x x))
 (1 2 3 4 1 2 3 4)
```
---
> 这道题我参考了 count-leaves 和 练习 2.27，其中比较难处理的可能是 tree 的第一部分，要注意这里的 result 应该是空的，其他地方逻辑跟 2.27 就没什么区别了。
```
(define (fringe tree)
  (define (iter tree result)
    (cond ((null? tree) result)
          ((not (pair? tree)) (cons tree result))
          (else (append (iter (car tree) nil)
                        (iter (cdr tree) result)))))

  (iter tree nil))


(define x (list (list 1 2) (list 3 4)))

(fringe x)
(fringe (list x x))

; 执行结果
'(1 2 3 4)
'(1 2 3 4 1 2 3 4)
```

###  Exercise 2.29
> A binary mobile consists of two branches, a left branch and a right branch. Each branch is a rod of a certain length, from which hangs either a weight or another binary mobile. We can represent a binary mobile using compound data by constructing it from two branches (for example, using $list$):
```
(define (make-mobile left right)
  (list left right))
```
> A branch is constructed from a $length$ (which must be a number) together with a $structure$, which may be either a number (representing a simple weight) or another mobile:
```
(define (make-branch length structure)
  (list length structure))
```
> a. Write the corresponding selectors $left-branch$ and $right-branch$, which return the branches of a mobile, and $branch-length$ and $branch-structure$, which return the components of a branch.
> b. Using your selectors, define a procedure $total-weight$ that returns the total weight of a mobile.
> c. A mobile is said to be $balanced$ if the torque applied by its top-left branch is equal to that applied by its top right branch (that is, if the length of the le rod multiplied by the weight hanging from that rod is equal to the corresponding product for the right side) and if each of the submobiles hanging offits branches is balanced. Design a predicate that tests whether a binary mobile is balanced.
> d. Suppose we change the representation of mobiles so that the constructors are 
```
(define (make-mobile left right) (cons left right))
(define (make-branch length structure) 
  (cons length structure))
```
> How much do you need to change your programs to convert to the new representation?
---
> 这道题主要是需要理解 mobile 是什么东西，我感觉它跟杠杆很像，然后就比较好处理了。
```
; a
(define (left-branch mobile)
  (car mobile))

(define (right-branch mobile)
  (car (cdr mobile)))

(define (branch-length branch)
  (car branch))

(define (branch-structure branch)
  (car (cdr branch)))

; b
(define (total-weight mobile)
  (cond ((null? mobile) 0)
        ((not (pair? mobile)) mobile)
        (else (+ (total-weight (branch-structure (left-branch mobile)))
                 (total-weight (branch-structure (right-branch mobile)))))))

; c
(define (torque branch)
  (* (branch-length branch)
     (total-weight (branch-structure branch))))

(define (balanced? mobile)
  (if (not (pair? mobile))
      true
      (= (torque (left-branch mobile))
         (torque (right-branch mobile)))))

(newline)
(define a (make-mobile (make-branch 2 3) (make-branch 3 2)))
(total-weight a)
(balanced? a)

(newline)
(define b (make-mobile (make-branch 2 a) (make-branch 4 a)))
(total-weight b)
(balanced? b)

(newline)
(define c (make-mobile (make-branch 2 b) (make-branch 3 a)))
(total-weight c)
(balanced? c)

; 执行结果
5
#t

10
#f

15
#f

; d
(define (right-branch mobile)
  (cdr mobile))

(define (branch-structure branch)
  (cdr branch))
```

### Exercise 2.30
> Define a procedure $square-tree$ analogous to the $square-list$ procedure of Exercise 2.21. That is, $square-tree$ should behave as follows:
```
(square-tree
 (list 1
       (list 2 (list 3 4) 5)
       (list 6 7)))
(1 (4 (9 16) 25) (36 49))
```
> Define $square-tree$ both directly (i.e., without using any higher-order procedures) and also by using map and recursion.
---
> 这个题目没啥难度，直接仿照 scale-tree 函数，修改一下函数名就行了。
```
(define (square-tree tree)
  (cond ((null? tree) nil)
        ((not (pair? tree)) (square tree))
        (else (cons (square-tree (car tree))
                    (square-tree (cdr tree))))))

(define (square-tree-by-map tree)
  (map (lambda (sub-tree)
         (if (pair? sub-tree)
             (square-tree-by-map sub-tree)
             (square sub-tree)))
       tree))


(define test (list 1
                   (list 2 (list 3 4) 5)
                   (list 6 7)))

(square-tree test)
(square-tree-by-map test)

; 执行结果
'(1 (4 (9 16) 25) (36 49))
'(1 (4 (9 16) 25) (36 49))
```

### Exercise 2.31
> Abstract your answer to Exercise 2.30 to produce a procedure $tree-map$ with the property that $square-tree$ could be defined as
```
(define (square-tree tree) (tree-map square tree))
```
---
> 这道题跟上面一道的 map 实现几乎一模一样，我还以为我理解错题目了，上网搜了一下，发现别人也是这么写的，那就这样吧。
```
(define (tree-map f tree)
  (map (lambda (sub-tree)
         (if (pair? sub-tree)
             (tree-map f sub-tree)
             (f sub-tree)))
       tree))

(define (square-tree tree) (tree-map square tree))


(square-tree
 (list 1
       (list 2 (list 3 4) 5)
       (list 6 7)))

; 执行结果
'(1 (4 (9 16) 25) (36 49))
```

### Exercise 2.32
> We can represent a set as a list of distinct elements, and we can represent the set of all subsets of the set as a list of lists. For example, if the set is (1 2 3), then the set of all subsets is (() (3) (2) (2 3) (1) (1 3) (1 2) (1 2 3)). Complete the following definition of a procedure that generates the set of subsets of a set and give a clear explanation of why it works:
```
(define (subsets s)
  (if (null? s)
      (list nil)
      (let ((rest (subsets (cdr s))))
        (append rest (map <??> rest)))))
```
---
> 这道题有一定难度，要注意到题目里面缺少对 `(car s)` 的处理，我们每次求 `(cdr s)` 的子集后要跟 `(car s)` 拼一下。
```
(define (subsets s)
  (if (null? s)
      (list nil)
      (let ((rest (subsets (cdr s))))
        (append rest (map (lambda (x) (cons (car s) x)) rest)))))


(subsets (list 1 2 3))

; 执行结果
'(() (3) (2) (2 3) (1) (1 3) (1 2) (1 2 3))
```

## 2.2.3 Sequences as Conventional Interfaces

### Exercise 2.33
> Fill in the missing expressions to complete the following definitions of some basic list-manipulation operations as accumulations:
```
; p 表示一个函数，sequence 表示一个列表
; 这个函数将对列表中每一个元素进行 p 操作
(define (map p sequence)
  (accumulate (lambda (x y) <??>) nil sequence))

(define (append seq1 seq2)
  (accumulate cons <??> <??>))

(define (length sequence)
  (accumulate <??> 0 sequence))
```
---
> 这道题还是有一定难度的，尤其是第一个 `(map p sequence)`，我开始没明白它的意思，不知道 lambda 两个参数要干嘛，所以先做的后面2个，做到第三个的时候才发现是 accumulate 函数中 op 函数需要2个参数，明白了这一点，剩下的就比较好处理了，x 就表示当前要处理的项，y 就是原函数中的递归项。
```
(define (map p sequence)
  (accumulate
   (lambda (x y) (if (null? x) y (cons (p x) y)))
   nil
   sequence))

(define (append seq1 seq2)
  (accumulate cons seq2 seq1))

(define (length sequence)
  (accumulate
   (lambda (x y) (if (null? x) y (+ y 1)))
   0
   sequence))


(define odds (list 1 3 5 7 9))
(define evens (list 2 4 6 8 10))

(map square odds)
(map sqrt evens)
(append odds evens)
(length odds)

; 执行结果
'(1 9 25 49 81)
'(1.4142156862745097 2.0000000929222947 2.4494897427875517 2.8284271250498643 3.162277665175675)
'(1 3 5 7 9 2 4 6 8 10)
5
```

### Exercise 2.34
> Evaluating a polynomial in x at a given value of x can be formulated as an accumulation. We evaluate the polynomial

$a_nx^n+a_{n-1}x^{n-1}+...+a_1x+a_0$
> using a well-known algorithm called $Horner’s\ rule$, which structures the computation as

$(...(a_nx+a_{n-1})x+...+a_1)x+a_0.$
> In other words, we start with $a_n$, multiply by x, add $a_{n−1}$, multiply by x, and so on, until we reach $a_0$.

> Fill in the following template to produce a procedure that evaluates a polynomial using Horner’s rule. Assume that the coefficients of the polynomial are arranged in a sequence, from $a_0$ through $a_n$.
```
(define (horner-eval x coefficient-sequence)
  (accumulate (lambda (this-coeff higher-terms) <??>)
              0
              coefficient-sequence))
```
> For example, to compute $1+3x+5x^3+x^5$ at $x = 2$ you would evaluate
```
(horner-eval 2 (list 1 3 0 5 0 1))
```
---
> 这道题挺简单的，主要是题目里给的参数名起的太好了，本来我还不知道咋写的，一看 this-coeff 和 higher-terms 这俩参数，瞬间就明白了。
```
(define (horner-eval x coefficient-sequence)
  (accumulate (lambda (this-coeff higher-terms) (+ (* higher-terms x) this-coeff))
              0
              coefficient-sequence))


(horner-eval 2 (list 1 3 0 5 0 1))

; 执行结果
79
```

### Exercise 2.35
> Redefine count-leaves from Section 2.2.2 as an accumulation:
```
(define (count-leaves t)
  (accumulate ⟨??⟩ ⟨??⟩ (map ⟨??⟩ ⟨??⟩)))
```
---
> 这道题难度不大，利用 enumerate-tree 和 accumulate 很容易就能实现。
```
(define (count-leaves t)
  (accumulate
   +
   0
   (map (lambda (x) (if (null? x) 0 1)) 
        (enumerate-tree t))))


(define x (cons (list 1 2) (list 1 3 0 5 0 1)))
(count-leaves x)
(count-leaves (list x x))

; 执行结果
10
20
```

### Exercise 2.36
> The procedure $accumulate-n$ is similar to $accumulate$ except that it takes as its third argument a sequence of sequences, which are all assumed to have the same number of elements. It applies the designated accumulation procedure to combine all the first elements of the sequences, all the second elements of the sequences, and so on, and returns a sequence of the results. For instance, if s is a sequence containing four sequences, ((1 2 3) (4 5 6) (7 8 9) (10 11 12)),then the value of `(accumulate-n + 0 s)` should be the sequence (22 26 30). Fill in the missing expressions in the following definition of $accumulate-n$:
```
(define (accumulate-n op init seqs)
  (if (null? (car seqs))
      nil
      (cons (accumulate op init ⟨??⟩)
            (accumulate-n op init ⟨??⟩))))
```
---
> 这道题我自己没做出来，搜了一下别人的答案才发现原来这么简单。。
```
(define (accumulate-n op init seqs)
  (if (null? (car seqs))
      nil
      (cons (accumulate op init (map car seqs))
            (accumulate-n op init (map cdr seqs)))))


(define test (list (list 1 2 3) (list 4 5 6) (list 7 8 9) (list 10 11 12)))
(accumulate-n + 0 test)

; 执行结果
'(22 26 30)
```

### Exercise 2.37
> Suppose we represent vectors $\boldsymbol v = (v_i)$ as sequences of numbers, and matrices $\boldsymbol m = (m_{ij})$ as sequences of vectors (the rows of the matrix). For example, the matrix
$\begin{pmatrix} 1 & 2 & 3 & 4 \\ 4 & 5 & 6 & 6 \\ 6 & 7 & 8 & 9 \end{pmatrix}$
> is represented as the sequence ((1 2 3 4) (4 5 6 6) (6 7 8 9)). With this representation, we can use sequence operations to concisely express the basic matrix and vector operations. These operations (which are described in any book on matrix algebra) are the following:
$(dot-product\ v\ w)\ returns\ the\ sum\ \Sigma_i v_i w_i;$
$(matrix-*-vector\ m\ v)\ returns\ the\ vector\ \boldsymbol t, where\ t_i= \Sigma_j m_{ij} v_j;$
$(matrix-*-matrix\ m\ n)\ returns\ the\ matrix\ \boldsymbol p, where\ p_{ij} = \Sigma_k m_{ik}n_{kj};$
$(transpose\ m)\ returns\ the\ matrix\ \boldsymbol n, where\ n_{ij} = m_{ji}.$
> We can define the do tproduct as
```
(define (dot-product v w)
  (accumulate + 0 (map * v w)))
```
> Fill in the missing expressions in the following procedures for computing the other matrix operations. (The procedure $accumulate-n$ is defined in Exercise 2.36.)
```
(define (matrix-*-vector mv)
  (map ⟨??⟩ m))

(define (transpose mat)
  (accumulate-n ⟨??⟩ ⟨??⟩ mat))

(define (matrix-*-matrix m n)
  (let ((cols (transpose n)))
    (map ⟨??⟩ m)))
```
---
> 这道题目还是挺难的，第一个矩阵乘向量比较简单，让向量依次跟矩阵的每一行点乘即可；第二个其实我不会做，我就是随便把 cons 和 nil 填到了空出的位置，没想到一执行恰好就是我要的结果，然后我回过头去看了一下 accumulate-n 的代码，发现它其实实现的就是转置的功能；第三个首先要理解它对 n 进行转置的目的，其实 m x n 就等价于用 m 的每一行跟 n 的每一列依次做点乘，现在对 n 做了转置之后，就相当于让 m 的每一行和 n 的每一行做点乘，明白了这一点这道题就可以很容易地实现了。
```
; m 表示矩阵，v 表示向量，m 的行数必须等于 v 中元素的个数
; 矩阵乘向量，相当于用矩阵的每一行跟向量做点乘
(define (matrix-*-vector m v)
  (map (lambda (x) (dot-product x v)) m))

; mat 表示矩阵
(define (transpose mat)
  (accumulate-n cons nil mat))

; m, n 都表示矩阵，m 的列数必须等于 n 的行数
; 最后的结果矩阵行数等于 m 的行数，列数等于 n 的列数
(define (matrix-*-matrix m n)
  (let ((cols (transpose n)))
    (map (lambda (mat) (matrix-*-vector cols mat)) m)))


(define mat (list (list 1 2 3 4) (list 4 5 6 6) (list 6 7 8 9)))
(define mat2 (list (list 1 2 3 4) (list 4 5 6 6) (list 6 7 8 9) (list 1 2 3 4)))
(define v (list 1 3 3 1))

(dot-product v (list 2 3 5 7))
(matrix-*-vector mat v)
(transpose mat)
(matrix-*-matrix mat mat2)

; 执行结果
33
'(20 43 60)
'((1 4 6) (2 5 7) (3 6 8) (4 6 9))
'((31 41 51 59) (66 87 108 124) (91 121 151 174))
```

### Exercise 2.38
> The $accumulate$ procedure is also known as $fold-right$, because it combines the first element of the sequence with the result of combining all the elements to the right. There is also a $fold-left$, which is similar to $fold-right$, except that it combines elements working in the opposite direction:
```
(define (fold-left op initial sequence)
  (define (iter result rest)
    (if (null? rest)
        result
        (iter (op result (car rest))
              (cdr rest))))
  (iter initial sequence))
```
> What are the values of
```
(fold-right / 1 (list 1 2 3))
(fold-left / 1 (list 1 2 3))
(fold-right list nil (list 1 2 3))
(fold-left list nil (list 1 2 3))
```
> Give a property that op should satisfy to guarantee that $fold-right$ and $fold-left$ will produce the same values for any sequence.
---
> 这道题还是挺简单的，题目给的2组例子都是结果不一样的，所以很容易就会想到跟顺序无关的操作，比如加法和乘法。
```
(fold-right / 1 (list 1 2 3))
(fold-left / 1 (list 1 2 3))

(fold-right list nil (list 1 2 3))
(fold-left list nil (list 1 2 3))


(fold-right + 1 (list 1 2 3))
(fold-left + 1 (list 1 2 3))

(fold-right * 1 (list 1 2 3))
(fold-left * 1 (list 1 2 3))

; 执行结果
1 1/2
1/6
'(1 (2 (3 ())))
'(((() 1) 2) 3)
7
7
6
6
```

### Exercise2.39
> Complete the following definitions of $reverse$ (Exercise 2.18) in terms of $fold-right$ and $fold-left$ from Exercise 2.38:
```
(define (reverse sequence)
  (fold-right (lambda (x y) ⟨??⟩) nil sequence))

(define (reverse sequence)
  (fold-left (lambda (x y) ⟨??⟩) nil sequence))
```
---
> 这道题还是有难度的，我只做出了用 $fold-left$ 实现的部分，用 $fold-right$ 实现的时候，开始用的 $cons$ 和 $list$，顺序虽然是对的，但是多了很多括号，最后我也想到了使用 $append$，但是一直报错，我试了一下没有找到解决办法，最后去搜了一下别人的答案。。
```
(define (reverse-by-right sequence)
  (fold-right (lambda (x y) (append y (list x))) nil sequence))

(define (reverse-by-left sequence)
  (fold-left (lambda (x y) (cons y x)) nil sequence))

(define odds (list 1 3 5 7 9))
(reverse-by-right odds)
(reverse-by-left odds)

; 执行结果
'(9 7 5 3 1)
'(9 7 5 3 1)
```

### Exercise2.40
> Define a procedure $unique-pairs$ that, given an integer n, generates the sequence of pairs $(i, j)$ with $1 < j < i < n$. Use $unique-pairs$ to simplify the definition of $prime-sum-pairs$ given above.
---
> 这道题还是挺简单的，最难的部分书上已经实现了，我们只要理解了书上这部分的代码，然后再加个大小的判断即可。
```
(define (unique-pairs n)
  (flatmap (lambda (i) (map (lambda (j) (cond ((> i j) (list i j))))
                            (enumerate-interval 1 (- i 1))))
           (enumerate-interval 1 n)))

(unique-pairs 5)

(define (prime-sum-pairs n)
  (map make-pair-sum
       (filter prime-sum? (unique-pairs n))))

(prime-sum-pairs 10)

; 执行结果
'((2 1) (3 1) (3 2) (4 1) (4 2) (4 3) (5 1) (5 2) (5 3) (5 4))
'((2 1 3) (3 2 5) (4 1 5) (4 3 7) (5 2 7) (6 1 7) (6 5 11) (7 4 11) (7 6 13) (8 3 11) (8 5 13) (9 2 11) (9 4 13) (9 8 17) (10 1 11) (10 3 13) (10 7 17) (10 9 19))
```

### Exercise 2.41
> Write a procedure to find all ordered triples of distinct positive integers i, j, and k less than or equal to a given integer n that sum to a given integer s.
---
> 这道题有一点难度，主要是要使用两次 flatmap 函数，仿照2元组的构造方式构造出3元组来，然后再筛选出和为s的。
```
; 获取不大于正整数n的1/3的最大整数
(define (one-third-factor n)
  (cond ((= (remainder n 3) 0) (/ n 3))
        ((= (remainder n 3) 1) (/ (- n 1) 3))
        (else (/ (- n 2) 3))))

(define (ordered-triple-sum n s)
  (if (or (< s 6) (> n (- s 3)))     ; n是不同的3个正整数之和，所以s至少是6,且n至少比s小3
      nil
      (filter (lambda (seq) (= (accumulate + 0 seq) s))
              (flatmap (lambda (i)
                         (flatmap (lambda (j)
                                    (map (lambda (k) (list i j k))
                                         (enumerate-interval (+ j 1) n)))    ; 第三个数比第二个大
                                    (enumerate-interval (+ i 1) (- n 1))))   ; 第二个数比第一个大
                       (enumerate-interval 1 (one-third-factor n))))))       ; 需要的是有序3元组，所以第一个数最大也比n/3小


(ordered-triple-sum 15 20)

; 执行结果
'((1 4 15) (1 5 14) (1 6 13) (1 7 12) (1 8 11) (1 9 10) (2 3 15) (2 4 14) (2 5 13) (2 6 12) (2 7 11) (2 8 10) (3 4 13) (3 5 12) (3 6 11) (3 7 10) (3 8 9) (4 5 11) (4 6 10) (4 7 9) (5 6 9) (5 7 8))
```

### Exercise 2.42
> The “eight-queens puzzle” asks how to place eight queens on a chessboard so that no queen is in check from any other (i.e., no two queens are in the same row, column, or diagonal). One possible solution is shown in Figure 2.8. One way to solve the puzzle is to work across the board, placing a queen in each column. Once we have placed $k-1$ queens, we must place the $k^{th}$ queen in a position where it does not check any of the queens already on the board. We can formulate this approach recursively: Assume that we have already generated the sequence of all possible ways to place $k-1$ queens in the first $k-1$ columns of the board. For each of these ways, generate an extended set of positions by placing a queen in each row of the $k^{th}$ column. Now filter these, keeping only the positions for which the queen in the $k^{th}$ column is safe with respect to the other queens. This produces the sequence of all ways to place k queens in the first k columns. By continuing this process, we will produce not only one solution, but all solutions to the puzzle.

![Alt text](<images/exer 2.42.png>)

>  We implement this solution as a procedure $queens$, which returns a sequence of all solutions to the problem of placing n queens on an $n × n$ chessboard. queens has an internal procedure $queen-cols$ that returns the sequence of all ways to place queens in the first k columns of the board.
```
(define (queens board-size)
  (define (queen-cols k)
    (if (= k 0)
        (list empty-board)
        (filter
         (lambda (positions) (safe? k positions))
         (flatmap
          (lambda (rest-of-queens)
            (map (lambda (new-row)
                   (adjoin-position new-row k rest-of-queens))
                 (enumerate-interval 1 board-size)))
          (queen-cols (- k 1))))))
  (queen-cols board-size))
```
> In this procedure $rest-of-queens$ is a way to place $k-1$ queens in the first $k-1$ columns, and $new-row$ is a proposed row in which to place the queen for the $k^{th}$ column. Complete the program by implementing the representation for sets of board positions, including the procedure $adjoin-position$, which adjoins a new row-column position to a set of positions, and $empty-board$, which represents an empty set of positions. You must also write the procedure $safe?$, which determines for a set of positions, whether the queen in the $k^{th}$ column is safe with respect to the others. (Note that we need only check whether the new queen is safe—the other queens are already guaranteed safe with respect to each other.)
---
> 这道题太难了，我自己只完成了 $empty-board$ 这一个定义，其他的函数即使看了别人的答案也研究了半天才搞明白。。
```
; board-size 指的是正方形棋盘的长
(define (queens board-size)
  (define (queen-cols k)
    (if (= k 0)
        (list empty-board)
        (filter
         (lambda (positions) (safe? k positions))     ; 每组位置不冲突的皇后的位置构成一个位置的集合
         (flatmap
          (lambda (rest-of-queens)         ; rest-of-queens 表示已经被放置在安全位置的 k-1 个王后的位置的组合
            (map (lambda (new-row)
                   (adjoin-position new-row k rest-of-queens))
                 (enumerate-interval 1 board-size)))             ; 把第 k 列的新位置加进之前的王后的位置组合
          (queen-cols (- k 1))))))
  (queen-cols board-size))

(define empty-board nil)

; 检查2个位置坐标是否冲突
; 同行比较好判断,只要新王后位置的行跟前 k-1 个王后的行都不同就行,同列同理
; 对角线比较复杂,分为从左上到右下和从左下到右上两类
; 从左上到右下,在同一条对角线上的坐标,行与列坐标之差相同
; 从左下到右上,在同一条对角线上的坐标,行与列坐标之和相同
(define (check pos1 pos2)
  (let ((x1 (car pos1))
        (y1 (cadr pos1))
        (x2 (car pos2))
        (y2 (cadr pos2)))
    (and (not (= x1 x2))
         (not (= y1 y2))
         (not (= (- x1 x2) (- y1 y2)))
         (not (= (+ x1 x2) (+ y1 y2))))))

; 检查新加入的王后的位置与其他王后的位置是否冲突
; k 其实没有任何作用
(define (safe? k positions)
  (let ((new-queen (car positions))
        (rest-of-queens (cdr positions)))
    (accumulate (lambda (pos result)
                  (and (check pos new-queen)
                       result))
                true
                rest-of-queens)))
         
; 在已有前 k-1 个王后的位置组合的基础上，把某个位置坐标(row col)加到第一个位置
(define (adjoin-position row col rest-of-queens)
  (cons (list row col) rest-of-queens))
 

(queens 1)
(queens 2)
(queens 3)
(queens 4)
(queens 8)


; 执行结果
'(((1 1)))
'()
'()
'(((1 4) (3 3) (4 2) (2 1)) ((1 4) (4 3) (2 2) (3 1)) ((2 4) (3 3) (1 2) (4 1)) ((3 4) (1 3) (2 2) (4 1)))
'(((1 8) (2 7) (6 6) (3 5) (5 4) (7 3) (8 2) (4 1))
  ((1 8) (2 7) (4 6) (6 5) (7 4) (3 3) (8 2) (5 1))
  ((1 8) (2 7) (6 6) (3 5) (7 4) (4 3) (8 2) (5 1))
  ((1 8) (2 7) (7 6) (3 5) (4 4) (6 3) (8 2) (5 1))
  ((1 8) (3 7) (4 6) (5 5) (7 4) (2 3) (8 2) (6 1))
  ((1 8) (4 7) (2 6) (7 5) (5 4) (3 3) (8 2) (6 1))
  ((1 8) (5 7) (2 6) (4 5) (7 4) (3 3) (8 2) (6 1))
  ((1 8) (3 7) (7 6) (2 5) (4 4) (5 3) (8 2) (6 1))
  ((1 8) (2 7) (4 6) (5 5) (8 4) (6 3) (3 2) (7 1))
  ((1 8) (4 7) (2 6) (5 5) (6 4) (8 3) (3 2) (7 1))
  ((1 8) (3 7) (6 6) (2 5) (5 4) (8 3) (4 2) (7 1))
  ((1 8) (2 7) (4 6) (6 5) (8 4) (3 3) (5 2) (7 1))
  ((1 8) (2 7) (6 6) (3 5) (8 4) (4 3) (5 2) (7 1))
  ((1 8) (3 7) (6 6) (4 5) (2 4) (8 3) (5 2) (7 1))
  ((1 8) (6 7) (2 6) (3 5) (4 4) (8 3) (5 2) (7 1))
  ((1 8) (2 7) (4 6) (8 5) (5 4) (3 3) (6 2) (7 1))
  ((2 8) (4 7) (1 6) (5 5) (6 4) (7 3) (3 2) (8 1))
  ((3 8) (1 7) (6 6) (2 5) (5 4) (7 3) (4 2) (8 1))
  ((3 8) (1 7) (6 6) (4 5) (2 4) (7 3) (5 2) (8 1))
  ((2 8) (6 7) (1 6) (3 5) (4 4) (7 3) (5 2) (8 1))
  ((3 8) (1 7) (4 6) (5 5) (7 4) (2 3) (6 2) (8 1))
  ((2 8) (4 7) (1 6) (7 5) (5 4) (3 3) (6 2) (8 1))
  ((2 8) (5 7) (1 6) (4 5) (7 4) (3 3) (6 2) (8 1))
  ((3 8) (1 7) (7 6) (2 5) (4 4) (5 3) (6 2) (8 1))
  ((4 8) (1 7) (3 6) (5 5) (6 4) (2 3) (7 2) (8 1))
  ((2 8) (4 7) (5 6) (1 5) (6 4) (3 3) (7 2) (8 1))
  ((4 8) (1 7) (5 6) (2 5) (6 4) (3 3) (7 2) (8 1))
  ((5 8) (1 7) (2 6) (4 5) (6 4) (3 3) (7 2) (8 1))
  ((2 8) (3 7) (6 6) (4 5) (1 4) (5 3) (7 2) (8 1))
  ((2 8) (4 7) (6 6) (1 5) (3 4) (5 3) (7 2) (8 1))
  ((4 8) (1 7) (6 6) (2 5) (3 4) (5 3) (7 2) (8 1))
  ((2 8) (6 7) (3 6) (1 5) (4 4) (5 3) (7 2) (8 1)))
```

### Exercise 2.43
> Louis Reasoner is having a terrible time doing Exercise 2.42. His queens procedure seems to work, but it runs extremely slowly. (Louis never does manage to wait long enough for it to solve even the $6 × 6$ case.) When Louis asks Eva Lu Ator for help, she points out that he has interchanged the order of the nested mappings in the $flatmap$, writing it as
```
(flatmap
 (lambda (new-row)
   (map (lambda (rest-of-queens)
          (adjoin-position new-row k rest-of-queens))
        (queen-cols (- k 1))))
 (enumerate-interval 1 board-size))
```
> Explain why this interchange makes the program run slowly. Estimate how long it will take Louis’s program to solve theeight-queens puzzle, assuming that the program in Exercise 2.42 solves the puzzle in time T.
---
> 慢的原因比较好理解，$Louis$ 的答案每一次都要把 $queen-cols$ 计算 `(enumerate-interval 1 board-size)` 遍，一共算了 $board-size^{board-size}$ 遍，对于八皇后问题就是 $8^8$ 遍；对于练习 2.42 的原方法，每次循环都会减一次，所以一共计算了 $n!$ 次，如果原方法时间为 $T$，那么 $Louis$ 的方法要用的时间是 $\frac{8^8}{8!}T$.

## 2.2.4 Example: A Picture Language
> 我在这一章遇到了一个大问题，就是书上用的那些函数 $beside, wave, flip-vert$ 我统统用不了。我用的是 DrRacket 这个软件，在网上查了半天，终于找到了解决办法。
> 首先是官方教程，在 DrRacket 中依次打开 File -> Package Manager...，在弹出的页面中 "Do What I Mean" 菜单页的输入：sicp，回车之后自动安装就行了。
> 但是我试了好几次，总是因为网络问题没法下载成功，最后求助于 chatgpt 终于解决了。
> 首先是手动下载 [sicp](https://github.com/sicp-lang/sicp.git) 包到 Racket 安装目录，然后打开 cmd 命令行，输入 `raco pkg install ./sicp` 即可用本地的 sicp 目录安装包。
> 安装好之后，重启 DrRacket 软件，依次点击上方菜单栏的 Language -> Choose Language，在弹出的页面中，找到 Teaching Languages(ctl-T) 下选择 SICP(PLaneT 1.18)，点击 OK。
> 再次回到代码编辑页面后，就不需要开头的 #lang racket 了，直接写代码就行。
> 还有一点，安装的 sicp 包里也是没有 $wave, rogers$ 的，但是提供了 $einstein$，所以可以用 `(define wave einstein)` 替换掉或者把 书上所有代码里的 $wave$ 都用 $einstein$ 代替。不过直接在文件里输入 `einstein` 或者 `wave` 是看不到图象的，而是以以 #procedure 的形式存在的，需要用 `(paint einstein)` 显式地调用，这样就可以看到爱神的头像了。

###  Exercise 2.44
> Define the procedure $up-split$ used by $corner-split$. It is similar to $right-split$, except that it switches the roles of $below$ and $beside$.
---
> 这道题非常的简单，就像题目所说的那样，只要交换 $below$ 和 $beside$ 的位置就行。
```
(paint (right-split wave 1))

(define (up-split painter n)
  (if (= n 0)
      painter
      (let ((smaller (up-split painter (- n 1))))
        (below painter (beside smaller smaller)))))

(paint (up-split wave 1))

(define (corner-split painter n)
  (if (= n 0)
      painter
      (let ((up (up-split painter (- n 1)))
            (right (right-split painter (- n 1))))
        (let ((top-left (beside up up))
              (bottom-right (below right right))
              (corner (corner-split painter (- n 1))))
          (beside (below painter top-left)
                  (below bottom-right corner))))))

(paint (corner-split wave 1))
(paint (corner-split wave 2))
```
> 效果如下图：

![Alt text](<images/exer 2.44-right-split.png>)

![Alt text](<images/exer 2.44-up-split.png>)

![Alt text](<images/exer 2.44-corner-split-1.png>)

![Alt text](<images/exer 2.44-corner-split-2.png>)

> 不过这是全新的内容，我觉得最好先理解 $below$ 和 $beside$ 的作用，其实就是字面意思，$beside$ 是把2个图形左右排列，第一个图形在左边; $below$ 是把2个图形上下排列，但是要注意它是把第二个图形放在上面，如下图所示：
```
(define wave einstein)

(paint (beside wave (below wave wave)))
(paint (below (beside wave wave) wave))
```
![Alt text](<images/exer 2.44-beside.png>)

![Alt text](<images/exer 2.44-below.png>)

### Exercise 2.45
> $right-split$ and $up-split$ can be expressed as instances of a general splitting operation. Define a procedure $split$ with the property that evaluating
```
(define right-split-2 (split beside below))
(define up-split-2 (split below beside))
```
> produces procedures $right-split$ and $up-split$ with the same behaviors as the ones already defined.
---
> 这道题本身没什么难度，但是我再次遇到了环境问题。。之前在台式电脑上装的sicp包，用同样的步骤在笔记本上怎么都不行，卸载重装了好几次，最后参考[这篇文章](https://www.neilvandyke.org/racket/sicp/)终于找到了解决办法。
> 方法其实也不复杂，随便打开一个窗口，输入 `#lang planet neil/sicp`，然后点击右上角的 run 等待安装完毕重启 DrRacket，再依次点击 Language -> Choose Language，就可以选择看到 SICP(PLaneT 1.18) 了。但是这么简单的方法我用了2个多小时才找到。。
> 回到这道题，只要注意到 $split$ 的返回值也是一个函数，且它的两个参数分别为 $painter$ 和 $n$，至于实现，仿照原来的 $right-split$ 或 $up-split$ 即可。
```
(define wave einstein)

(define (right-split-1 painter n)
  (if (= n 0)
      painter
      (let ((smaller (right-split-1 painter (- n 1))))
        (beside painter (below smaller smaller)))))

(define (up-split-1 painter n)
  (if (= n 0)
      painter
      (let ((smaller (up-split-1 painter (- n 1))))
        (below painter (beside smaller smaller)))))

(define (split op1 op2)
  (define (iter painter n)
    (if (= n 0)
        painter
        (let ((smaller (iter painter (- n 1))))
          (op1 painter (op2 smaller smaller)))))
  iter)

(define right-split-2 (split beside below))
(define up-split-2 (split below beside))


(paint (right-split-1 wave 1))
(paint (right-split-2 wave 1))

(paint (up-split-1 wave 1))
(paint (up-split-2 wave 1))
```
> 效果如下图所示：

![Alt text](<images/exer 2.45-right-split-1.png>)

![Alt text](<images/exer 2.45-right-split-2.png>)

![Alt text](<images/exer 2.45-up-split-1.png>)

![Alt text](<images/exer 2.45-up-split-2.png>)

### Exercise 2.46
> A two-dimensional vector $\boldsymbol v$ running from the origin to a point can be represented as a pair consisting of an x-coordinate and a y-coordinate. Implement a data abstraction for vectors 
by giving a constructor $make-vect$ and corresponding selectors $xcor-vect$ and $ycor-vect$. In terms of your selectors and constructor, implement procedures $add-vect$, $sub-vect$, and 
$scale-vect$ that perform the operations vector addition, vector subtraction, and multiplying a vector by a scalar:

$(x_1, y_1) + (x_2, y_2) = (x_1+x_2, y_1+y_2),$
$(x_1, y_1) - (x_2, y_2) = (x_1-x_2, y_1-y_2),$
$s \cdot (x, y) = (sx, sy).$
---
> 这道题没啥说的，差不多是最简单的题目了。
```
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


(define v1 (make-vect 3 4))
(define v2 (make-vect -4 3))

(xcor-vect v1)
(ycor-vect v1)

(add-vect v1 v2)
(sub-vect v1 v2)

(scale-vect 0.2 (add-vect v1 v2))

; 执行结果
3
4
(mcons -1 7)
(mcons 7 1)
(mcons -0.2 1.4000000000000001)
```

### Exercise 2.47
> Here are two possible constructors for frames:
```
(define (make-frame origin edge1 edge2)
  (list origin edge1 edge2))

(define (make-frame origin edge1 edge2)
  (cons origin (cons edge1 edge2)))
```
> For each constructor supply the appropriate selectors to produce an implementation for frames.
---
> 这道题也不难，感觉是为了让我们熟悉 $car$ 和 $cdr$ 这两个函数。
```
(define (make-frame-by-list origin edge1 edge2)
  (list origin edge1 edge2))

(define (origin-frame-by-list frame)
  (car frame))

(define (edge1-frame-by-list frame)
  (cadr frame))

(define (edge2-frame-by-list frame)
  (caddr frame))

(define (make-frame-by-cons origin edge1 edge2)
  (cons origin (cons edge1 edge2)))

(define (origin-frame-by-cons frame)
  (car frame))

(define (edge1-frame-by-cons frame)
  (cadr frame))

(define (edge2-frame-by-cons frame)
  (cddr frame))


(define origin (make-vect 1 1))
(define v1 (make-vect 3 4))
(define v2 (make-vect -4 3))

(define frame1 (make-frame-by-list origin v1 v2))
(origin-frame-by-list frame1)
(edge1-frame-by-list frame1)
(edge2-frame-by-list frame1)

(define frame2 (make-frame-by-cons origin v1 v2))
(origin-frame-by-cons frame2)
(edge1-frame-by-cons frame2)
(edge2-frame-by-cons frame2)

; 执行结果
(mcons 1 1)
(mcons 3 4)
(mcons -4 3)
(mcons 1 1)
(mcons 3 4)
(mcons -4 3)
```

### Exercise 2.48
> A directed line segment in the plane can be represented as a pair of vectors—the vector running from the origin to the start-point of the segment, and the vector running from the 
origin to the end-point of the segment. Use your vector representation from Exercise 2.46 to define a representation for segments with a constructor $make-segment$ and selectors 
$start-segment$ and $end-segment$.
---
> 这道题太简单了，没啥说的。
```
(define (make-segment v1 v2)
  (cons v1 v2))

(define (start-segment segment)
  (car segment))

(define (end-segment segment)
  (cdr segment))


(define v1 (make-vect 3 4))
(define v2 (make-vect -4 3))
  
(define a-segment (make-segment v1 v2))
a-segment
(start-segment a-segment)
(end-segment a-segment)

; 执行结果
(mcons (mcons 3 4) (mcons -4 3))
(mcons 3 4)
(mcons -4 3)
```

### Exercise 2.49
> Use $segments->painter$ to define the following primitive painters:
  >> a. The painter that draws the outline of the designated frame.
  >> b. The painter that draws an “X” by connecting opposite corners of the frame.
  >> c. The painter that draws a diamond shape by connecting the midpoints of the sides of the frame.
  >> d. The $wave$ painter.
---
> 这道题目我本来感觉不是很难，我按照题目要求把 frame 的3个点坐标取出来，然后用 make-segment 连成线，但是做了半天总是不行，
上网搜了一下其他人的答案，发现他们都是直接传的 segment-list，而不是传 frame，而且之前定义的 make-vect, make-segment 也都用不了。。
必须先导入 sicp-pict，然后再用它自带的 vect 和 segment 来创建向量和线段。完整代码如下：
```
(#%require sicp-pict)


; a 
(define outline 
  (segments->painter 
   (list 
    (segment (vect 0.0 0.0) (vect 0.0 1.0)) 
    (segment (vect 0.0 0.0) (vect 1.0 0.0)) 
    (segment (vect 0.0 1.0) (vect 1.0 1.0)) 
    (segment (vect 1.0 0.0) (vect 1.0 1.0)))))

; b 
(define x-painter 
  (segments->painter 
   (list 
    (segment (vect 0.0 0.0) (vect 1.0 1.0)) 
    (segment (vect 0.0 1.0) (vect 1.0 0.0))))) 

; c
(define diamond 
  (segments->painter 
   (list 
    (segment (vect 0.0 0.5) (vect 0.5 1.0)) 
    (segment (vect 0.5 1.0) (vect 1.0 0.5)) 
    (segment (vect 1.0 0.5) (vect 0.5 0.0)) 
    (segment (vect 0.5 0.0) (vect 0.0 0.5))))) 

; d
(define wave 
  (segments->painter (list 
                      (segment (vect .25 0) (vect .35 .5)) 
                      (segment (vect .35 .5) (vect .3 .6)) 
                      (segment (vect .3 .6) (vect .15 .4)) 
                      (segment (vect .15 .4) (vect 0 .65)) 
                      (segment (vect 0 .65) (vect 0 .85)) 
                      (segment (vect 0 .85) (vect .15 .6)) 
                      (segment (vect .15 .6) (vect .3 .65)) 
                      (segment (vect .3 .65) (vect .4 .65)) 
                      (segment (vect .4 .65) (vect .35 .85)) 
                      (segment (vect .35 .85) (vect .4 1)) 
                      (segment (vect .4 1) (vect .6 1)) 
                      (segment (vect .6 1) (vect .65 .85)) 
                      (segment (vect .65 .85) (vect .6 .65)) 
                      (segment (vect .6 .65) (vect .75 .65)) 
                      (segment (vect .75 .65) (vect 1 .35)) 
                      (segment (vect 1 .35) (vect 1 .15)) 
                      (segment (vect 1 .15) (vect .6 .45)) 
                      (segment (vect .6 .45) (vect .75 0)) 
                      (segment (vect .75 0) (vect .6 0)) 
                      (segment (vect .6 0) (vect .5 .3)) 
                      (segment (vect .5 .3) (vect .4 0)) 
                      (segment (vect .4 0) (vect .25 0)) 
                      )))

(paint outline)
(paint x-painter)
(paint diamond)
(paint wave)
```
> 效果如下：

![Alt text](<Images/exer 2.49.png>)

### Exercise 2.50
> Define the transformation flip-horiz, which flips painters horizontally, and transformations that rotate painters counterclockwise by 180 degrees and 270 degrees.
---
![Alt text](<Images/exer 2.50-illustration.png>)

> 这道题挺有意思的，搞明白这道题就明白了 frame 的3个点的位置。如上图所示，为了更好区分，特意用了长方形而不是正方形，第一幅图是原图，O 表示 origin, A 表示 edge1，B 表示 edge2。无论进行何种变换，左下坐标都是 (0, 0)，左上都是(0, 1)， 右下都是(1, 0)， 右上都是(1, 1)，我们只要把变换后的图形中 O, A, B 的新位置作为参数传进去就行。
```
#lang racket

(require (planet "sicp.ss" ("soegaard" "sicp.plt" 2 1)))


(define sub-vect vector-sub)

; Transforming and combining painters
(define (transform-painter painter origin corner1 corner2)
  (lambda (frame)
    (let ((m (frame-coord-map frame)))
      (let ((new-origin (m origin)))
        (painter (make-frame
                  new-origin
                  (sub-vect (m corner1) new-origin)
                  (sub-vect (m corner2) new-origin)))))))

(define (flip-horiz painter)
  (transform-painter painter
                     (make-vect 1.0 0.0) ; new origin
                     (make-vect 0.0 0.0) ; new end of edge1
                     (make-vect 1.0 1.0))) ; new end of edge2

(define (rotate90 painter)
  (transform-painter painter
                     (make-vect 1.0 0.0) ; new origin
                     (make-vect 1.0 1.0) ; new end of edge1
                     (make-vect 0.0 0.0))) ; new end of edge2

(define (rotate180 painter)
  (transform-painter painter
                     (make-vect 0.0 1.0) ; new origin
                     (make-vect 1.0 1.0) ; new end of edge1
                     (make-vect 0.0 0.0))) ; new end of edge2

(define (rotate270 painter)
  (transform-painter painter
                     (make-vect 0.0 1.0) ; new origin
                     (make-vect 0.0 0.0) ; new end of edge1
                     (make-vect 1.0 1.0))) ; new end of edge2

(paint einstein)
(paint (flip-horiz einstein))
(paint (rotate90 einstein))
(paint (rotate180 einstein))
(paint (rotate270 einstein))
```
> 效果如下图所示，为了跟水平翻转对比，特意把原图加上了：

![Alt text](<Images/exer 2.50-origin.png>)

![Alt text](<Images/exer 2.50-flip-horiz.png>)

![Alt text](<Images/exer 2.50-rotate90.png>)

![Alt text](<Images/exer 2.50-rotate180.png>)

![Alt text](<Images/exer 2.50-rotate270.png>)

###  Exercise2.51
> Define the below operation for painters. below takes two painters as arguments. The resulting painter, given a frame, draws with the first painter in the bottom of the frame
 and with the second painter in the top. Define below in two different ways—first by writing a procedure that is analogous to the beside procedure given above, and again
 in terms of beside and suitable rotation operations (from Exercise 2.50).
---
> 这道题目难度不大，理解了 2.50 那张图后，再仿照 beside 的代码，只要把3个坐标的位置调整一下就可以了; 至于利用 beside 和旋转来实现 below，就更简单了，先把2幅图向右旋转90°，然后 beside 排到一起，
最后再把排到一起的图形向左旋转90°即可。
```
#lang racket


(require (planet "sicp.ss" ("soegaard" "sicp.plt" 2 1)))


(define sub-vect vector-sub)

; Transforming and combining painters
(define (transform-painter painter origin corner1 corner2)
  (lambda (frame)
    (let ((m (frame-coord-map frame)))
      (let ((new-origin (m origin)))
        (painter (make-frame
                  new-origin
                  (sub-vect (m corner1) new-origin)
                  (sub-vect (m corner2) new-origin)))))))

(define (beside painter1 painter2)
  (let ((split-point (make-vect 0.5 0.0)))
    (let ((paint-left
           (transform-painter
            painter1
            (make-vect 0.0 0.0)
            split-point
            (make-vect 0.0 1.0)))
          (paint-right
           (transform-painter
            painter2
            split-point
            (make-vect 1.0 0.0)
            (make-vect 0.5 1.0))))
      (lambda (frame)
        (paint-left frame)
        (paint-right frame)))))

; analogous to beside
(define (below painter1 painter2)
  (let ((split-point (make-vect 0.0 0.5)))
    (let ((paint-up
           (transform-painter
            painter2
            split-point
            (make-vect 1.0 0.5)
            (make-vect 0.0 1.0)))
          (paint-low
           (transform-painter
            painter1
            (make-vect 0.0 0.0)
            (make-vect 1.0 0.0)
            split-point)))
      (lambda (frame)
        (paint-up frame)
        (paint-low frame)))))

(paint (below einstein (beside einstein einstein)))

(define (rotate90 painter)
  (transform-painter painter
                     (make-vect 1.0 0.0) ; new origin
                     (make-vect 1.0 1.0) ; new end of edge1
                     (make-vect 0.0 0.0))) ; new end of edge2

(define (rotate180 painter)
  (transform-painter painter
                     (make-vect 0.0 1.0) ; new origin
                     (make-vect 1.0 1.0) ; new end of edge1
                     (make-vect 0.0 0.0))) ; new end of edge2

(define (rotate270 painter)
  (transform-painter painter
                     (make-vect 0.0 1.0) ; new origin
                     (make-vect 0.0 0.0) ; new end of edge1
                     (make-vect 1.0 1.0))) ; new end of edge2

; in terms of beside and suittable rotation
(define (below- painter1 painter2)
  (rotate90 (beside (rotate270 painter1) (rotate270 painter2))))

(paint (below- einstein (beside einstein einstein)))
```
> 结果如下所示：

![Alt text](<Images/exer 2.51-beside.png>)

![Alt text](<Images/exer 2.51-beside.png>)

### Exercise 2.52
> Make changes to the square limit of wave shown in Figure 2.9 by working at each of the levels described above. In particular:
>> a. Add some segments to the primitive wave painter of Exercise 2.49 (to add a smile, for example).
>> b. Change the paern constructed by corner-split (for example, by using only one copy of the up-split and right-split images instead of two).
>> c. Modify the version of square-limit that uses square-of-four so as to assemble the corners in a different pateern. (For example, you might make the big Mr.Rogers look outward from each corner of the square.)
---
> 对于我来说，这道题最大的难度在于理解题意，我根据自己的理解修改之后想：就这么简单？然后去查了其他人的答案，发现还真就这么简单 ：）
```
(#%require sicp-pict)


(define wave 
  (segments->painter (list 
                      (segment (vect .25 0) (vect .35 .5)) 
                      (segment (vect .35 .5) (vect .3 .6)) 
                      (segment (vect .3 .6) (vect .15 .4)) 
                      (segment (vect .15 .4) (vect 0 .65)) 
                      (segment (vect 0 .65) (vect 0 .85)) 
                      (segment (vect 0 .85) (vect .15 .6)) 
                      (segment (vect .15 .6) (vect .3 .65)) 
                      (segment (vect .3 .65) (vect .4 .65)) 
                      (segment (vect .4 .65) (vect .35 .85)) 
                      (segment (vect .35 .85) (vect .4 1)) 
                      (segment (vect .4 1) (vect .6 1)) 
                      (segment (vect .6 1) (vect .65 .85)) 
                      (segment (vect .65 .85) (vect .6 .65)) 
                      (segment (vect .6 .65) (vect .75 .65)) 
                      (segment (vect .75 .65) (vect 1 .35)) 
                      (segment (vect 1 .35) (vect 1 .15)) 
                      (segment (vect 1 .15) (vect .6 .45)) 
                      (segment (vect .6 .45) (vect .75 0)) 
                      (segment (vect .75 0) (vect .6 0)) 
                      (segment (vect .6 0) (vect .5 .3)) 
                      (segment (vect .5 .3) (vect .4 0)) 
                      (segment (vect .4 0) (vect .25 0)) 
                      )))

(define (right-split painter n)
  (if (= n 0)
      painter
      (let ((smaller (right-split painter (- n 1))))
        (beside painter (below smaller smaller)))))

(define (up-split painter n)
  (if (= n 0)
      painter
      (let ((smaller (up-split painter (- n 1))))
        (beside painter (below smaller smaller)))))

; a
(define wave-with-smile
  (segments->painter (list 
                      (segment (vect .25 0) (vect .35 .5)) 
                      (segment (vect .35 .5) (vect .3 .6)) 
                      (segment (vect .3 .6) (vect .15 .4)) 
                      (segment (vect .15 .4) (vect 0 .65)) 
                      (segment (vect 0 .65) (vect 0 .85)) 
                      (segment (vect 0 .85) (vect .15 .6)) 
                      (segment (vect .15 .6) (vect .3 .65)) 
                      (segment (vect .3 .65) (vect .4 .65)) 
                      (segment (vect .4 .65) (vect .35 .85))
                      (segment (vect .35 .85) (vect .4 1))
                      (segment (vect .4 1) (vect .6 1)) 
                      (segment (vect .6 1) (vect .65 .85))
                      (segment (vect .65 .85) (vect .6 .65)) 
                      (segment (vect .6 .65) (vect .75 .65)) 
                      (segment (vect .75 .65) (vect 1 .35)) 
                      (segment (vect 1 .35) (vect 1 .15)) 
                      (segment (vect 1 .15) (vect .6 .45)) 
                      (segment (vect .6 .45) (vect .75 0)) 
                      (segment (vect .75 0) (vect .6 0)) 
                      (segment (vect .6 0) (vect .5 .3)) 
                      (segment (vect .5 .3) (vect .4 0)) 
                      (segment (vect .4 0) (vect .25 0))
                      (segment (vect .45 .76) (vect .5 0.72))
                      (segment (vect .5 0.72) (vect .55 .76))
                      )))

(paint wave-with-smile)


(define (corner-split painter n)
  (if (= n 0)
      painter
      (let ((up (up-split painter (- n 1)))
            (right (right-split painter (- n 1))))
        (let ((top-left up)
              (bottom-right (below right right))
              (corner (corner-split painter (- n 1))))
          (beside (below painter top-left)
                  (below bottom-right corner))))))

(paint (corner-split wave-with-smile 1))

(define (square-of-four tl tr bl br)
  (lambda (painter)
    (let ((top (beside (tl painter) (tr painter)))
          (bottom (beside (bl painter) (br painter))))
      (below bottom top))))

(define (square-limit painter n)
  (let ((combine4 (square-of-four flip-vert rotate180
                                  identity flip-horiz)))
    (combine4 (corner-split painter n))))

(paint (square-limit wave-with-smile 1))
```
> 执行结果如下图所示：

![alt text](<Images/exer 2.52.png>)


# 2.3 Symbolic Data

## 2.3.1 Quotation

###  Exercise2.53
> What would the interpreter print in response to evaluating each of the following expressions?
```
(list 'a 'b 'c)
(list (list 'george))
(cdr '((x1 x2) (y1 y2)))
(cadr '((x1 x2) (y1 y2)))
(pair? (car '(a short list)))
(memq 'red '((red shoes) (blue socks)))
(memq 'red '(red shoes blue socks))
```
---
> 结果如下：
```
'(a b c)
'((george))
'((y1 y2))
'(y1 y2)
#f
#f
'(red shoes blue socks)
```

### Exercise 2.54
> Two lists are said to be equal? if they contain equal elements arranged in the same order. For example,

`(equal? '(this is a list) '(this is a list))`
> is true, but

`(equal? '(this is a list) '(this (is a) list))`
>  is false. To be more precise, we can define equal? recursively in terms of the basic eq? equality of symbols by saying that a and b are equal? if they are both symbols and 
the symbols are eq?, or if they are both lists such that `(car a)` is equal? to `(car b)` and `(cdr a)` is equal? to `(cdr b)`. Using this idea, implement equal? as a procedure.
---
> 这道题挺简单的，依次比较就行了。
```
(define (equal? a b)
  (cond ((and (null? a) (null? b)) true)
        ((or (null? a) (null? b)) false)
        ((eq? (car a) (car b)) (equal? (cdr a) (cdr b)))
        (else false)))


(equal? '(this is a list) '(this is a list))
(equal? '(this is a list) '(this (is a) list))

; 执行结果
#t
#f
```

### Exercise 2.55
> Eva Lu Ator types to the interpreter the expression

`(car ''abracadabra)`
> To her surprise, the interpreter prints back quote. Explain.
---
> 因为 `(car ''abracadabra)` 被解释器理解为 `(car (quote (quote abracadabra)))`，第一个 quote 引用了后面的内容 `(quote abracadabra)`，
这实际上是一个有2个元素的 list，对这个list 调用 car 就取出了第一个元素 quote。也就是第二个 quote 没有被当作函数使用，而是被当作字符串了。

### Exercise 2.56
> Show how to extend the basic differentiator to handle more kinds of expressions. For instance, implement the differentiation rule

$\frac{d(u^n)}{dx}=n u^{n-1} \frac{du}{dx}$
> by adding a new clause to the deriv program and defining appropriate procedures exponentiation?, base, exponent, and make-exponentiation.
(You may use the symbol ** to denote exponentiation.) Build in the rules that anything raised to the power 0 is 1 and anything raised to the power 1 is the thing itself.
---
> 这道题难度不大，先仿照 make-sum, make-product 写出 make-exponentiation 函数，剩下的部分就很简单了。
```
(define (make-exponentiation base exponent)
  (cond ((=number? base 0) 0)
        ((=number? base 1) 1)
        ((and (number? base) (=number? exponent 0)) 1)
        ((and (number? base) (=number? exponent 1)) base)
        ((and (number? base) (number? exponent)) (* base (make-exponentiation base (- exponent 1))))
        (else (list '** base exponent))))

(define (exponentiation? x) (and (pair? x) (eq? (car x) '**)))

(define (base e) (cadr e))

(define (exponent e) (caddr e))

(define (deriv exp var)
  (cond ((number? exp) 0)
        ((variable? exp) (if (same-variable? exp var) 1 0))
        ((exponentiation? exp)
         (let ((base (base exp))
               (n (exponent exp)))
           (if (same-variable? base var)
               (make-product n
                             (make-exponentiation base (- n 1)))
               0)))
        ((sum? exp) (make-sum (deriv (addend exp) var)
                              (deriv (augend exp) var)))
        ((product? exp)
         (make-sum
          (make-product (multiplier exp)
                        (deriv (multiplicand exp) var))
          (make-product (deriv (multiplier exp) var)
                        (multiplicand exp))))
        (else
         (error "unknown expression type: DERIV" exp))))


(deriv '(** x 3) 'x)
(deriv '(** x 3) 'y)

; 执行结果
'(* 3 (** x 2))
0
```

### Exercise 2.57
> Extend the differentiation program to handle sums and products of arbitrary numbers of (two or more) terms. Then the last example above could be expressed as

`(deriv '(* x y (+ x 3)) 'x)`
> Try to do this by changing only the representation for sums and products, without changing the deriv procedure at all. For example, the addend of a sum would be the first term,
 and the augend would be the sum of the rest of the terms.
---
> 这道题挺难的，我理解了题目提示的方法，就是把剩下的项也表示为和或者乘的形式，但是我不明白该怎么实现，递归调用并不能达到要求，最后上网搜了一下才知道怎么做。
```
(define (augend s)
  (let ((last (cddr s)))
    (if (null? (cdr last))
        (car last)
        (cons '+ last))))

(define (multiplicand p)
    (let ((last (cddr p)))
    (if (null? (cdr last))
        (car last)
        (cons '* last))))

(deriv '(* x y (+ x 3)) 'x)
(deriv '(+ x (* 3 (+ x (+ y 2)))) 'x)
(deriv '(+ x (* 3 (+ x y 2))) 'x)

; 执行结果
'(+ (* x y) (* y (+ x 3)))
4
4
```

###  Exercise 2.58
> Suppose we want to modify the differentiation program so that it works with ordinary mathematical notation, in which + and * are infix rather than prefix operators. Since the differentiation program is defined 
in terms of abstract data, we ca modify it to work with different representations of expressions solely by changing the predicates, selectors, and constructors that define the representation of the algebraic 
expressions on which the differentiator is to operate.
>> a. Show how to do this in order to differentiate algebraic expressions presented in infix form, such as (x + (3 * (x + (y + 2)))). To simplify the task, assume that + and * always take two arguments and that 
expressions are fully parenthesized.
>> b. The problem becomes substantially harder if we allow standard algebraic notation, such as (x + 3 * (x + y + 2)), which drops unnecessary parentheses and assumes that multiplication is done before addition.
 Can you design appropriate predicates, selectors, and constructors for this notation such that our derivative program still works?
---
> 这道题乍一看很棘手，但是仔细一想其实挺简单的，只要把构造函数和选择器里 + 和 * 的位置改一下就行了，还有原来的前缀表示法要多加一个 + 或 *，现在也可以直接省略掉了。
```
(define (make-sum a1 a2)
  (cond ((=number? a1 0) a2)
        ((=number? a2 0) a1)
        ((and (number? a1) (number? a2)) (+ a1 a2))
        (else (list a1 '+ a2))))

(define (sum? x) (and (pair? x) (eq? (cadr x) '+)))

(define (addend s) (car s))

(define (augend s)
  (let ((last (cddr s)))
    (if (null? (cdr last))
        (car last)
        last)))

(define (make-product m1 m2)
  (cond ((or (=number? m1 0) (=number? m2 0)) 0)
        ((=number? m1 1) m2)
        ((=number? m2 1) m1)
        ((and (number? m1) (number? m2)) (* m1 m2))
        (else (list m1 '* m2))))

(define (product? x) (and (pair? x) (eq? (cadr x) '*)))

(define (multiplier p) (car p))

(define (multiplicand p)
    (let ((last (cddr p)))
    (if (null? (cdr last))
        (car last)
        last)))


(deriv '(x + (3 * (x + (y + 2)))) 'x)
(deriv '(x + 3 * (x + y + 2)) 'x)

; 执行结果
4
4
```

### Exercise 2.59
> Implement the union-set operation for the unordered-list representation of sets.
---
> 这道题很简单，仿照 intersection-set 稍作修改就可以实现了
```
(define (union-set set1 set2)
  (cond ((null? set1) set2)
        ((element-of-set? (car set1) set2)
         (union-set (cdr set1) set2))
        (else (cons (car set1) (union-set (cdr set1) set2)))))


(define set1 (list 1 3 5 'a 'b 'c))
(define set2 (list 2 4 6 'a 'd 'c))

(union-set set1 set2)

; 执行结果 
'(1 3 5 b 2 4 6 a d c)
```

### Exercise2.60
> We specified that a set would be represented as a list with no duplicates. Now suppose we allow duplicates. For instance, the set {1, 2, 3} could be represented as the list (2 3 2 1 3 2 2). Design procedures element of-set?, adjoin-set, union-set, and intersection-set that operate on this representation. How does the efficiency of each compare with the corresponding procedure for the non-duplicate representation? Are there applications for which you would use this representation in preference to the nonduplicate one?
---
> 这道题目我有点没理解，如果允许重复的话，交集该怎么处理？所以最后交集我没有改变，element-of-set? 也没有修改。
```
(define (element-of-set? x set)
  (cond ((null? set) false)
        ((equal? x (car set)) true)
        (else (element-of-set? x (cdr set)))))

(define (adjoin-set x set)
  (cons x set))

(define (union-set set1 set2)
  (append set1 set2))

(define (intersection-set set1 set2)
  (cond ((or (null? set1) (null? set2)) '())
        ((element-of-set? (car set1) set2)
         (cons (car set1) (intersection-set (cdr set1) set2)))
        (else (intersection-set (cdr set1) set2))))


(define set1 (list 1 3 5 'a 'b 'c))
(define set2 (list 2 4 6 'a 'd 'c))

(adjoin-set 'a set1)
(union-set set1 set2)
(intersection-set set1 set2)

; 执行结果
'{a 1 3 5 a b c}
'{1 3 5 a b c 2 4 6 a d c}
'{a c}
```

###  Exercise 2.61
> Give an implementation of adjoin-set using the ordered representation. By analogy with element-of-set? show how to take advantage of the ordering to produce a procedure that requires
 on the average about half as many steps as with the unordered representation.
---
> 这道题实现起来倒是不难，每次比较一下集合第一个元素和要插入的元素的大小，如果要插入的数小于等于集合第一个元素，就直接用 cons 把这个新元素和集合连接起来; 如果要插入的元素大于集合第一个元素，
就把集合第一个元素和要插入元素和集合其他项连接的结果连接起来就行了。最差的情况就是，要插入的元素比集合最大的元素还要大，这样要遍历整个集合，此时和原来的实现没有区别; 在其他情况，平均应该可以节省一半的步骤。
```
(define (adjoin-set x set)
  (let ((first (car set)))
    (cond ((null? set) (list x))
          ((<= x first) (cons x set))
          (else (cons first (adjoin-set x (cdr set)))))))
      

(define set1 (list 1 3 5 7 9))
(adjoin-set 6 set1)

; 执行结果 
'(1 3 5 6 7 9)
```

### Exercise 2.62
> Give a (n) implementation of union-set for sets represented as ordered lists.
---
> 这道题难度也不大，思路是依次从两个集合中取第一个元素，比较他们的大小，把小的那个和剩下所有元素连接的结果连接起来。由于两个集合中每个元素都只需要取出一次，所以时间复杂度应该是 O(n)。
```
(define (union-set set1 set2)
  (cond ((null? set1) set2)
        ((null? set2) set1)
        ((let ((s1 (car set1))
               (s2 (car set2)))
           (if (<= s1 s2)
               (cons s1 (union-set (cdr set1) set2))
               (cons s2 (union-set set1 (cdr set2))))))))

(define set1 (list 1 3 5 7 9))
(define set2 (list 2 4 6 8 10))

(union-set set1 set2)

; 结果如下所示
'(1 2 3 4 5 6 7 8 9 10)
```

###  Exercise 2.63
> Each of the following two procedures converts a binary tree to a list.
```
(define (tree->list-1 tree)
  (if (null? tree)
      '()
      (append (tree->list-1 (left-branch tree))
              (cons (entry tree)
                    (tree->list-1
                     (right-branch tree))))))


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
```
>> a. Do the two procedures produce the same result for every tree? If not, how do the results differ? What lists do the two procedures produce for the trees in Figure 2.16?
>> b. Do the two procedures have the same order of growth in the number of steps required to convert a balanced tree withn elements to a list? If not, which one grows more slowly?
---
> a. 对于 图2.16 的三种形式，这两个函数执行的结果是相同的，如下所示：
```
(define t1 (make-tree 3 (make-tree 1 '() '()) (make-tree 5 '() '())))
(define t2 (make-tree 9 '() (make-tree 11 '() '())))
(define test1 (make-tree 7 t1 t2))

(tree->list-1 test1)
(tree->list-2 test1)


(define t3 (make-tree 3 (make-tree 1 '() '()) '()))
(define t4 (make-tree 9 (make-tree 7 '() '()) (make-tree 11 '() '())))
(define test2 (make-tree 5 t3 t4))

(tree->list-1 test2)
(tree->list-2 test2)


(define t5 (make-tree 1 '() '()))
(define t6 (make-tree 7 (make-tree 5 '() '()) (make-tree 9 '() (make-tree 11 '() '()))))
(define test3 (make-tree 3 t5 t6))

(tree->list-1 test3)
(tree->list-2 test3)

; 结果如下
'(1 3 5 7 9 11)
'(1 3 5 7 9 11)
'(1 3 5 7 9 11)
'(1 3 5 7 9 11)
'(1 3 5 7 9 11)
'(1 3 5 7 9 11)
```
> b. 对于 tree->list-1，因为 append 需要花费线性时间，所以T(n) = 2 * T(n/2) + O(n/2)，时间复杂度为 O(n * log n); 对于 tree->list-2，T(n) = 2*T(n/2) + O(1)，时间复杂度为 O(n)，第二个增长的慢一些。

### Exercise 2.64
> The following procedure list->tree converts an ordered list to a balanced binary tree. The helper procedure partial-tree takes as arguments an integer n and list of at least n elements 
and constructs a balanced tree containing the firstn elements of the list. The result returned by partial-tree is a pair (formed with cons) whose car is the constructed tree and 
whose cdr is the list of elements not included in the tree.
```
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
```
>> a. Write a short paragraph explaining as clearly as you can how partial-tree works. Draw the tree produced by list->tree for the list (1 3 5 7 9 11).
>> b. What is the order of growth in the number of steps required by list->tree to convert a list ofn elements?
---
> a. 这个函数首先取前 (n-1)/2 个元素作为树的左子树，取剩下的元素中第一个作为树的根，然后把剩下的元素作为右子树，对于每一个子树也采用同样的方法，最后把左子树、根和右子树拼起来作为返回结果的第一个元素。
结果如下所示：

![alt text](<Images/exer 2.64-a.png>)

> b. partial-tree 每一次都把列表分成2个大概是 n/2 的新列表和中间的一个元素，然后再把他们拼成一颗树。所以 T(n) = 2T(n/2) + O(1)，根据 Master theorem，a=2, b=2, f(n) = O(1) = O(n^0), 即 c=0.
则 T(n) = O(n)，具体计算方法参考这篇[维基百科](https://en.wikipedia.org/wiki/Master_theorem_(analysis_of_algorithms)#Generic_form)。

### Exercise 2.65
> Use the results of Exercise 2.63 and Exercise 2.64 to give (n) implementations of union-set and intersection-set for sets implemented as (balanced) binary trees.
---
> 这道题难度还是挺大的，一开始我不知道怎么直接对2颗树求交集和并集，而且要在 O(n) 的时间复杂度内。上网看了一下别人的答案，发现他们都是先用 2.63 的 tree->list-2 把树转为列表，然后再求交集并集，最后再用 2.64 的 list->tree 把结果转成树结构。
这样我就明白怎么做了，尤其是求并集可以直接参考 2.62 的答案，但是稍作修改，让它能去除重复元素，求交集虽然没有现成的，但是参考并集的方法也不难。
```
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

; 结果如下
'(7 () (9 () ()))
'(6 (3 (1 () (2 () ())) (4 () (5 () ()))) (9 (7 () (8 () ())) (10 () (11 () ()))))
```

### Exercise 2.66
> Implement the lookup procedure for the case where the set of records is structured as a binary tree, ordered by the numerical values of the keys.
---
> 这道题还是挺简单的，由于是有序的二叉树，所以可以先比较根与要查找的数字的大小，如果相等就查到了；如果根小于要查找的数，则递归调用判断右子树中是否包含这个数; 如果根大于要查找的数，则去左子树去查即可。
```
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

; 结果如下
#t
#f
```

## 2.3.4 Example: Huffman Encoding Trees

### Exercise 2.67
> Define an encoding tree and a sample message:
```
(define (make-leaf-set pairs)
  (if (null? pairs)
      '()
      (let ((pair (car pairs)))
        (adjoin-set (make-leaf (car pair)      ; symbol
                               (cadr pair))    ; frequency
                    (make-leaf-set (cdr pairs))))))

(define sample-tree
  (make-code-tree (make-leaf 'A 4)
                  (make-code-tree
                   (make-leaf 'B 2)
                   (make-code-tree
                    (make-leaf 'D 1)
                    (make-leaf 'C 1)))))

(define sample-message '(0 1 1 0 0 1 0 1 0 1 1 1 0))
```
> Use the decode procedure to decode the message, and give the result.
---
> 这道题纯粹是为了展示前面定义的 Huffman 算法的作用，结果如下：
```
> (decode sample-message sample-tree)
'(A D A B B C A)(decode sample-message sample-tree)
```

### Exercise 2.68
> The encode procedure takes as arguments a message and a tree and produces the list of bits that gives the encoded message.
```
(define (encode message tree)
  (if (null? message)
      '()
      (append (encode-symbol (car message) tree)
              (encode (cdr message) tree))))
```
> encode-symbol is a procedure, which you must write, that returns the list of bits that encodes a given symbol according to a given tree. You should design encode-symbol 
so that it signals an error if the symbol is not in the tree at all. Test your procedure by encoding the result you obtained in Exercise 2.67 with the sample tree and seeing 
whether it is the same as the original sample message.
---
> 这道题对我来说难度挺大的，我一开始就被如果符号就是树的根怎么表示难住了，因为书上讲的好像都是左边是0，右边是1，却没有关于根上字符的表示，我也没有想到可以直接用“空”表示。。最后看了别人的答案才终于明白了。
```
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
        (if (element-of-set? symbol left)
            (cons 0 (encode-symbol symbol left))
            (cons 1 (encode-symbol symbol (right-branch tree)))))))


(define sample-tree
  (make-code-tree (make-leaf 'A 4)
                  (make-code-tree
                   (make-leaf 'B 2)
                   (make-code-tree
                    (make-leaf 'D 1)
                    (make-leaf 'C 1)))))

(define sample-message '(A D A B B C A))

; 期望答案是 '(0 1 1 0 0 1 0 1 0 1 1 1 0)
(encode sample-message sample-tree)

; 结果如下
'(0 1 1 0 0 1 0 1 0 1 1 1 0)
```

### Exercise 2.69
> The following procedure takes as its argument a list of symbol-frequency pairs (where no symbol appears in more than one pair) and generates a Huffman encoding tree according to the Huffman algorithm.
```
(define (generate-huffman-tree pairs)
  (successive-merge (make-leaf-set pairs)))
```
> make-leaf-set is the procedure given above that transforms the list of pairs into an ordered set of leaves. successive merge is the procedure you must write, using make-code-tree to successively merge the smallest-weight elements of the set until there is only one element left, which is the desired Huffman tree. (This procedure is slightly tricky, but not really complicated. If you find yourself designing a complex procedure, then you are almost certainly doing something wrong. You can take significant advantage of the fact that we are using an ordered set representation.)
---
> 这道题虽然题目说不会很复杂，但是我觉得还是挺难的。首先是要理解 successive-merge 的作用，它是要把一个个叶子按照权重由小到大依次合并成一个树，由于参数已经用 make-leaf-set 进行了排序，所以我们只要从前往后依次把这些“叶子”合并起来就行，每次合并好的树作为一个新的“叶子”与其他叶子一起进行新的合并；这里要注意合并后的树的权重可能会超过排在它之后的叶子，所以要重新对这些“叶子”按权重排序，这里我们可以直接用前面的 adjoin-set 来实现，完整代码如下：
```
(define (successive-merge leaf-set)
  (if (null? leaf-set)
      '()
      (let ((first (car leaf-set))
            (last (cdr leaf-set)))
        (if (null? last)
            first
            (successive-merge (adjoin-set (make-code-tree first (car last))
                                          (cdr last)))))))

(define pairs1 '((A 4) (B 2) (C 1) (D 1)))
(define pairs2 '((A 8) (B 3) (C 1) (D 1) (E 1) (F 1) (G 1) (H 1)))

(generate-huffman-tree pairs1)
(generate-huffman-tree pairs2)

; 结果如下
'((leaf A 4) ((leaf B 2) ((leaf D 1) (leaf C 1) (D C) 2) (B D C) 4) (A B D C) 8)
'((leaf A 8)
  ((((leaf H 1) (leaf G 1) (H G) 2) ((leaf F 1) (leaf E 1) (F E) 2) (H G F E) 4)
   (((leaf D 1) (leaf C 1) (D C) 2) (leaf B 3) (D C B) 5)
   (H G F E D C B)
   9)
  (A H G F E D C B)
  17)
```

### Exercise 2.70
> The following eight-symbol alphabet with associated relative frequencies was designed to efficiently encode the lyrics of 1950s rock songs. (Note that the “symbols” of an “alphabet” need not be individual letters.) 
```
A    2   GET 2   SHA 3   WAH 1
BOOM 1   JOB 2   NA  16  YIP 9
```
> Use generate-huffman-tree (Exercise 2.69) to generate a corresponding Huffmantree and use encode (Exercise 2.68) to encode the following message:
```
 Get a job
 Sha na na na na na na na na
 Get a job
 Sha na na na na na na na na
 Wah yip yip yip yip yip yip yip yip yip
 Sha boom
```
> How many bits are required for the encoding? What is the smallest number of bits that would be needed to encode this song if we used a fixed-length code for the eight-symbol alphabet?
---
> 这道题本来应该是非常简单的，只需要调用 2.68 和 2.69 的函数就行，但是我却遇到了好几个麻烦，第一个是大小写问题，我在生成霍夫曼树的时候，用的都是题目中默认的大写字母，但是要翻译的歌词却是既有大写又有小写，所以在 encode-symbol 函数的 `(eq? symbol (symbol-leaf tree))` 这一步就会跳出，我尝试了好几个方法也没找到怎么解决，最后直接把歌词改成全大写了。解决了大小写问题，我又遇到了相同的提示，一步步调试之后终于发现了问题，我练习 2.68 的 encode-symbol 本身就有问题，改完之后终于成功了。最后就是统计了一下长度，如果使用固定长度的编码，那么每个“符号”至少需要3个字符，程序如下所示：
```
(define (encode-symbol symbol tree)
  (if (leaf? tree)
      (if (eq? symbol (symbol-leaf tree))
          '()
          (error "bad symbol: The symbol is not in the tree at all!" symbol))
      (let ((left (left-branch tree)))
        (if (element-of-set? symbol (symbols left))
            (cons 0 (encode-symbol symbol left))
            (cons 1 (encode-symbol symbol (right-branch tree)))))))


(define pairs '((A 2) (GET 2) (SHA 3) (WAH 1) (BOOM 1) (JOB 2) (NA 16) (YIP 9)))
(define rock-tree (generate-huffman-tree pairs))
(define rock-song '(GET A JOB SHA NA NA NA NA NA NA NA NA GET A JOB SHA NA NA NA NA NA NA NA NA WAH YIP YIP YIP YIP YIP YIP YIP YIP YIP SHA BOOM))
(define encoded-rock-song (encode rock-song rock-tree))
(length encoded-rock-song)
(* 3 (length rock-song))

; 结果如下，由于编码后的内容是竖着的，太占地方了，就不贴了
84
108
```

### Exercise 2.71
> Suppose we have a Huffman tree for an alphabet of n symbols, and that the relative frequencies of the symbols are 1,2,4, . . . ,2n 1. Sketch the tree for n = 5; for n = 10. In such a tree (for general n) how many bits are required to encode the most frequent symbol? The least frequent symbol?
---
> 这道题挺简单的，只要明白了霍夫曼编码的逻辑，自己画一下就可以了，这会是一种非常不平衡的树，除了权重最低的两个符号构成了一个完整的子树，其他的子树都只有一个叶子，n=5 时如下图所示，n=10太多了就不画了，跟这个类似。

![alt text](<Images/exer 2.71.png>)

> 可以看出，当有 n 个符号时，使用频率最高的符号只需要1位就可以表示，频率最低的则需要 n-1 位。

### Exercise 2.72
> Consider the encoding procedure that you designed in Exercise 2.68. What is the order of growth in the number of steps needed to encode a symbol? Be sure to include the number of steps needed to search the symbol list at each node encountered. To answer this question in general is difficult. Consider the special case where the relative frequencies of then symbols are as described in Exercise 2.71, and give the order of growth (as a function of n) of the number of steps needed to encode the most frequent and least frequent symbols in the alphabet.
---
> 这道题如果只考虑 2.71 的那种情况，最常用的符号永远只需要1位，时间复杂度是 O(1), 最不常用的符号根据 2.71 的图可以看出来，每增加一个符号，所增加的步骤只是常数个，所以时间复杂度应该是 O(n)。

# 2.4 Multiple Representations for Abstract Data

## 2.4.1 Representations for Complex Numbers

### Exercise 2.73
> Section 2.3.2 described a program that performs symbolic differentiation:
```
(define (deriv exp var)
  (cond ((number? exp) 0)
        ((variable? exp)
         (if (same-variable? exp var) 1 0))
        ((sum? exp)
         (make-sum (deriv (addend exp) var)
                   (deriv (augend exp) var)))
        ((product? exp)
         (make-sum (make-product
                    (multiplier exp)
                    (deriv (multiplicand exp) var))
                   (make-product
                    (deriv (multiplier exp) var)
                    (multiplicand exp))))
        ⟨more rules can be added here⟩
        (else (error "unknown expression type: DERIV" exp))))
```
>  We can regard this program as performing a dispatch on the type of the expression to be differentiated. In this situation the “type tag” of the datum is the algebraic operator symbol (such as +) and the operation being performed is deriv. We can transform this program into data-directed style by rewriting the basic derivative procedure as
```
(define (deriv exp var)
  (cond ((number? exp) 0)
        ((variable? exp) (if (same-variable? exp var) 1 0))
        (else ((get 'deriv (operator exp))
               (operands exp) var))))

(define (operator exp) (car exp))
(define (operands exp) (cdr exp))
```
>> a. Explain what was done above. Why can’t we assimilate the predicates number? and variable? into the data-directed dispatch?
>> b. Write the procedures for derivatives of sums and products, and the auxiliary code required to install them in the table used by the program above.
>> c. Choose any additional differentiation rule that you like, such as the one for exponents (Exercise 2.56), and install it in this data-directed system.
>> d. In this simple algebraic manipulator the type of an expression is the algebraic operator that binds it together. Suppose, however, we indexed the procedures in the opposite way, so that the dispatch line in deriv looked like
```
((get (operator exp) 'deriv) (operands exp) var)
```
>> What corresponding changes to the derivative system are required?
---
> 首先做这道题之前要先把 put 和 get 函数给加进来
```
(define *operation-table* (make-hash))

(define (put op-type op-name procedure)
  (hash-set! *operation-table* (list op-type op-name) procedure))

(define (get op-type op-name)
  (hash-ref *operation-table* (list op-type op-name) #f))
```
> a. 上面的程序就是从 data-directed dispatch 表里取出一个操作为 deriv，类型为 (operator exp) 的过程，并把表达式和变量传给这个提取出的过程。不把 number? 和 variable? 放到 data-directed dispatch 表的原因是因为它们两个只需要一个参数，而这个程序会给取出的过程2个参数。我看到别人的答案基本都是说这两个过程没有标签，而且不需要加标签，所以不能放入 data-directed dispatch 表，但是题目问的是 why can't，它们的解释不是 can't 而是 needn't，不知道我的理解对不对。
> b&c. 这两问情况一样，难度也不大，参考 2.56 的练习，只需要修改一下取操作数的逻辑就可以了，因为 “+, *, **” 本身已经作为区分采用哪个过程的符号，所以取操作数不是从第二个取，而是第一个，其他地方就照搬过来就可以了。
```
(define (install-deriv-package)
  ;; internal procedures
  ;; sum
  (define (make-sum a1 a2)
    (cond ((=number? a1 0) a2)
          ((=number? a2 0) a1)
          ((and (number? a1) (number? a2)) (+ a1 a2))
          (else (list '+ a1 a2))))

  (define (sum? x) (and (pair? x) (eq? (car x) '+)))

  (define (addend s) (car s))

  (define (augend s) (cadr s))

  (define (sum-deriv expr var) 
    (make-sum (deriv (addend expr) var) 
              (deriv (augend expr) var))) 

  ;; product
  (define (make-product m1 m2)
    (cond ((or (=number? m1 0) (=number? m2 0)) 0)
          ((=number? m1 1) m2)
          ((=number? m2 1) m1)
          ((and (number? m1) (number? m2)) (* m1 m2))
          (else (list '* m1 m2))))

  (define (product? x) (and (pair? x) (eq? (car x) '*)))

  (define (multiplier p) (car p))

  (define (multiplicand p) (cadr p))

  (define (product-deriv expr var) 
    (make-sum (make-product (deriv (multiplier expr) var) 
                            (multiplicand expr))
              (make-product (multiplier expr)
                            (deriv (multiplicand expr) var))))

  ;; exponentiate
  (define (make-exponentiation base exponent)
    (cond ((=number? base 0) 0)
          ((=number? base 1) 1)
          ((and (number? base) (=number? exponent 0)) 1)
          ((and (number? base) (=number? exponent 1)) base)
          ((and (number? base) (number? exponent)) (* base (make-exponentiation base (- exponent 1))))
          (else (list '** base exponent))))

  (define (base e) (car e))

  (define (exponent e) (cadr e))

  (define (exponentation-deriv expr var) 
    (make-product (exponent expr) 
                  (make-product  
                   (make-exponentiation (base expr) 
                                        (make-sum (exponent expr) -1)) 
                   (deriv (base expr) var))))
               
  ;; interface to the rest of the system
  (put 'deriv '+ sum-deriv)
  (put 'deriv '* product-deriv)
  (put 'deriv '** exponentation-deriv)
  'done)


(install-deriv-package)


(deriv '(+ x x x) 'x) 
(deriv '(* x x x) 'x) 
(deriv '(+ x (* x  (+ x (+ y 2)))) 'x) 
(deriv '(+ x (* 3 (+ x (+ y 2)))) 'x)
(deriv '(** x 3) 'x) 

; 结果如下
'done
2
'(+ x x)
'(+ 1 (+ (+ x (+ y 2)) x))
4
'(* 3 (** x 2))
```
> d. 这样的话，只要在使用 put 函数的时候也先传类型，再传操作就可以了。

### Exercise 2.74
> Insatiable Enterprises, Inc., is a highly decentralized conglomerate company consisting of a large number of independent divisions located all over the world. The company’s computer 
facilities have just been interconnected by means of a clever network-interfacing scheme that makes the entire network appear to any user to be a single computer. Insatiable’s president, 
in her first attempt to exploit the ability of the network to extract administrative information from division files, is dismayed to discover that, although all the division files have been 
implemented as data structures in Scheme, the particular data structure used varies from division to division. A meeting of division managers is hastily called to search for a strategy 
to integrate the files that will satisfy headquarters’ needs while preserving the existing autonomy of the divisions.
> Show how such a strategy can be implemented with data-directed programming. As an example, suppose that each division’s personnel records consist of a single file, which contains 
a set of records keyed on employees’ names. The structure of the set varies from division to division. Furthermore, each employee’s record is itself a set (structured differently 
from division to division) that contains information keyed under identifiers such as address and salary.
> In particular:
>> a. Implement for headquarters a get-record procedure that retrieves a specified employee’s record from a specified personnel file. The procedure should be applicable to any division’s file. 
Explain how the individual divisions’ files should be structured. In particular, what type information must be supplied?
>> b. Implement for headquarters a get-salary procedure that returns the salary information from a given employee’s record from any division’s personnel file. How should the record be structured 
in order to make this operation work?
>> c. Implement for headquarters a find-employee-record procedure. This should search all the divisions’ files for the record of a given employee and return the record. Assume that 
this procedure takes as arguments an employee’s name and a list of all the divisions’ files.
>> d. When Insatiable takes over a new company, what changes must be made in order to incorporate the new personnel information into the central system?
---
> a. 这道题里，部门名称就相当于前面所说的类型，获取部门信息就是操作，我们根据这两个信息从提前建好的二维表里提取雇员所属部门的文件。每个部门文件都应该有一个 get-division 的过程，它根据雇员姓名获取对应的部门文件。
```
(define (get-record get-division employee-name) 
   ((get 'division get-division) employee-name)) 
```
> b. 这道题跟上一题很像，只是这次是从某个雇员的记录中获取工资信息。
```
(define (get-salary get-division record) 
  ((get 'salary get-division) record)) 
```
> c. 这道题就是依次检查所有部门，根据雇员名称获取记录。
```
(define (find-employee-record employee-name division-list) 
  (if (null? division-list) 
      #f 
      (or (get-record (car division-list) employee-name) 
          (find-employee-record employee-name (cdr division-list))))) 
```
> d. 每次接管一个新公司，都要把上述提到的过程添加到二维表里，使用的时候根据部门类型和操作来获取对应公司的过程。

### Exercise2.75
> Implement the constructor make-from-mag-ang in message-passing style. This procedure should be an alogous to the make-from-real-imag procedure given above.
---
> 这道题非常简单，只要稍微修改一下 make-from-real-imag 就行了
```
(define (make-from-mag-ang r a)
  (define (dispatch op)
    (cond ((eq? op 'magnitude) r)
          ((eq? op 'angle) a)
          ((eq? op 'real-part) (* (r (cos a))))
          ((eq? op 'imag-part) (* (r (sin a))))
          (else (error "Unknown op: MAKE-FROM-MAG-ANG" op))))
  dispatch)
```

### Exercise 2.76
> As a large system with generic operations evolves, new types of data objects or new operations may be needed. For each of the three strategies—generic operations with explicit dispatch data-directed style, and message-passing-style -- describe the changes that must be made to a system in order to add new types or new operations. Which organization would be most appropriate for a system in which new types must often be added? Which would be most appropriate for a system in which new operations must often be added?
---
> 对于 explicit dispatch 风格，每添加一种新类型，都需要编写新类型自身的操作函数，并在每个通用操作函数的 cond 中，添加一个新的分支；而添加新的操作，除了编写新的通用操作函数，还需要为每个类型添加类型相关的操作函数。
> 对于 data-directed 风格，添加一种新类型时，只需要添加相应的 install-new-package 函数，在一个地方编写好新类型自身的操作函数。通过二维表进行分发管理，通用函数本身不用做任何修改；而添加新操作，需要在每个包中添加相应的类型操作函数，并注册到二维表中；无论是添加操作还是类型，都比较简单。
> 对于 message-passing 风格，它使用一个动态的函数作为分发的依据，要添加新的类型，只需要为新类型添加一个分发函数；但是要添加新的操作，就需要在每个类型的分发函数中，添加一个新的分支，原有类型越多，添加新操作修改的地方就越多。
> 对于需要频繁新增类型的系统，应该选择 message-passing 风格，因为它新增类型非常简单，不需要修改旧的代码；对于需要频繁新增操作的系统，应该选择 data-directed 风格，添加操作只需要在实现了新的函数后，添加到二维表中即可。

# 2.5 Systems with Generic Operations

## 2.5.1 Generic Arithmetic Operations

### Exercise 2.77
> Louis Reasoner tries to evaluate the expression (magnitude z) where z is the object shown in Figure 2.24. To his surprise, instead of the answer she gets an error message from apply-generic, saying there is no method for the operation magnitude on the types (complex). He shows this interaction to Alyssa P. Hacker, who says “The problem is that the complex-number selectors were never defined for complex numbers, just for polar and rectangular numbers. All you have to do to make this work is add the following to the complex package:”
```
  (put 'real-part '(complex) real-part)
  (put 'imag-part '(complex) imag-part)
  (put 'magnitude '(complex) magnitude)
  (put 'angle '(complex) angle)
```
> Describe in detail why this works. As an example, trace through all the procedures called in evaluating the expression (magnitude z) where z is the object shown in Figure 2.24. In particular, how many times is apply-generic invoked? What procedure is dispatched to in each case?
---
> 这道题我想的是先把代码跑起来，因为直接按题目提示添加了那4行代码还是会报错，最终能运行的代码如下：
```
(define (install-rectangular-package)
  ;; internal procedures
  (define (real-part z) (car z))
  (define (imag-part z) (cdr z))
  (define (make-from-real-imag x y) (cons x y))
  (define (magnitude z)
    (sqrt (+ (square (real-part z))
             (square (imag-part z)))))
  (define (angle z)
    (atan (imag-part z) (real-part z)))
  (define (make-from-mag-ang r a)
    (cons (* r (cos a)) (* r (sin a))))
  ;; interface to the rest of the system
  (define (tag x) (attach-tag 'rectangular x))
  (put 'real-part '(rectangular) real-part)
  (put 'imag-part '(rectangular) imag-part)
  (put 'magnitude '(rectangular) magnitude)
  (put 'angle '(rectangular) angle)
  (put 'make-from-real-imag 'rectangular
       (lambda (x y) (tag (make-from-real-imag x y))))
  (put 'make-from-mag-ang 'rectangular
       (lambda (r a) (tag (make-from-mag-ang r a))))
  'done)

(define (install-polar-package)
  ;; internal procedures
  (define (magnitude z) (car z))
  (define (angle z) (cdr z))
  (define (make-from-mag-ang r a) (cons r a))
  (define (real-part z) (* (magnitude z) (cos (angle z))))
  (define (imag-part z) (* (magnitude z) (sin (angle z))))
  (define (make-from-real-imag x y)
    (cons (sqrt (+ (square x) (square y)))
          (atan y x)))
  ;; interface to the rest of the system
  (define (tag x) (attach-tag 'polar x))
  (put 'real-part '(polar) real-part)
  (put 'imag-part '(polar) imag-part)
  (put 'magnitude '(polar) magnitude)
  (put 'angle '(polar) angle)
  (put 'make-from-real-imag 'polar
       (lambda (x y) (tag (make-from-real-imag x y))))
  (put 'make-from-mag-ang 'polar
       (lambda (r a) (tag (make-from-mag-ang r a))))
  'done)

;; 复数
(define (install-complex-package)
  ;; imported procedures from rectangular and polar packages
  (define (make-from-real-imag x y)
    ((get 'make-from-real-imag 'rectangular) x y))
  (define (make-from-mag-ang r a)
    ((get 'make-from-mag-ang 'polar) r a))
  ;; internal procedures
  (define (add-complex z1 z2)
    (make-from-real-imag (+ (real-part z1) (real-part z2))
                         (+ (imag-part z1) (imag-part z2))))
  (define (sub-complex z1 z2)
    (make-from-real-imag (- (real-part z1) (real-part z2))
                         (- (imag-part z1) (imag-part z2))))
  (define (mul-complex z1 z2)
    (make-from-mag-ang (* (magnitude z1) (magnitude z2))
                       (+ (angle z1) (angle z2))))
  (define (div-complex z1 z2)
    (make-from-mag-ang (/ (magnitude z1) (magnitude z2))
                       (- (angle z1) (angle z2))))
  ;; interface to rest of the system
  (define (tag z) (attach-tag 'complex z))
  (put 'add '(complex complex)
       (lambda (z1 z2) (tag (add-complex z1 z2))))
  (put 'sub '(complex complex)
       (lambda (z1 z2) (tag (sub-complex z1 z2))))
  (put 'mul '(complex complex)
       (lambda (z1 z2) (tag (mul-complex z1 z2))))
  (put 'div '(complex complex)
       (lambda (z1 z2) (tag (div-complex z1 z2))))
  (put 'make-from-real-imag 'complex
       (lambda (x y) (tag (make-from-real-imag x y))))
  (put 'make-from-mag-ang 'complex
       (lambda (r a) (tag (make-from-mag-ang r a))))
  (put 'real-part '(complex) real-part)
  (put 'imag-part '(complex) imag-part)
  (put 'magnitude '(complex) magnitude)
  (put 'angle '(complex) angle)
  'done)

(define (make-complex-from-real-imag x y)
  ((get 'make-from-real-imag 'complex) x y))
(define (make-complex-from-mag-ang r a)
  ((get 'make-from-mag-ang 'complex) r a))

(define (real-part z) (apply-generic 'real-part z)) 
(define (imag-part z) (apply-generic 'imag-part z)) 
(define (magnitude z) (apply-generic 'magnitude z)) 
(define (angle z) (apply-generic 'angle z))

(install-rectangular-package)
(install-polar-package)
(install-complex-package)


(define z (make-complex-from-real-imag 3 4))
(magnitude z)

; 结果如下
5.000000000053722
```
> 这里要注意2点，一个是要安装这几个包，另一个是在安装这些包之前需要加上 `(define (magnitude z) (apply-generic 'magnitude z))`，不然会报错。
> 执行 `(magnitude z)` 的函数调用依次是：
```
(magnitude z)
(magnitude '(complex rectangular 3 . 4))
(apply-generic 'magnitude '(complex rectangular 3 . 4))
(get 'magnitude '(complex))
(apply magnitude (map contents '((complex rectangular 3 . 4))))

(magnitude '(rectangular 3 . 4))
(apply-generic 'magnitude '(rectangular 3 . 4))
(get 'magnitude '(rectangular))
(apply magnitude-rectangular (map contents '((rectangular 3 . 4))))
(magnitude-rectangular '(3 . 4))
5
```
> 为了看得更清楚，这里用 magnitude-rectangular 表示 install-rectangular-package 包中的 magnitude 过程。可以看出，在上面的过程中，一共调用了2次 apply-generic，第一次它根据 complex 和 magnitude 去寻找 install-complex-package 包中对应的过程；第二次它根据 rectangular 和 magnitude 找到了 install-rectangular-package 包中的 magnitude 过程。

### Exercise2.78
> The internal procedures in the scheme-number package are essentially nothing more than calls to the primitive procedures +, -, etc. It was not possible to use the primitives of the language directly because our type-tag system requires that each data object have a type attached to it. In fact, however, all Lisp implementations do have a type system, which they use internally. Primitive predicates such as symbol? and number? determine whether data objects have particular types. Modify the definitions of type-tag, contents, and attach-tag from Section 2.4.2 so that our generic system takes advantage of Scheme’s internal type system. That is to say, the system should work as before except that ordinary numbers should be represented simply as Scheme numbers rather than as pairs whose car is the symbol scheme-number.
---
> 这道题难度不大，就是说我们在设计程序的时候，先用内置的 number? 函数来判断，如果确实是数字，那就不用添加 scheme-number 标签，否则还跟之前一样。
```
(define (attach-tag type-tag contents)
  (if (number? contents)
      contents
      (cons type-tag contents)))

(define (type-tag datum)
  (cond ((number? datum) 'scheme-number)
        ((pair? datum) (car datum))
        (else (error "Bad tagged datum: TYPE-TAG" datum))))

(define (contents datum)
  (cond ((number? datum) datum)
        ((pair? datum) (cdr datum))
        (else (error "Bad tagged datum: CONTENTS" datum))))
```
> 上网看了别人的答案后，我发现 install-scheme-number-package 也能做一定简化，如下所示：
```
(define (install-scheme-number-package)
  (put 'add '(scheme-number scheme-number) +)
  (put 'sub '(scheme-number scheme-number) -)
  (put 'mul '(scheme-number scheme-number) *)
  (put 'div '(scheme-number scheme-number) /)
  (put 'make 'scheme-number (lambda (x) (attach-tag 'scheme-number x)))
  'done)

(define (make-scheme-number n)
  ((get 'make 'scheme-number) n))

(install-scheme-number-package)

(define m (make-scheme-number 5))
(define n (make-scheme-number 10))
(add m n)
(sub m n)
(mul m n)
(div m n)

; 执行结果
'done
15
-5
50
1/2
```

### Exercise2.79
> Define a generic equality predicate equ? that tests the equality of two numbers, and install it in the generic arithmetic package. This operation should work for ordinary numbers, rational numbers, and complex numbers.
---
> 这道题也挺简单的，分别在一般数字、有理数和复数包里实现这个函数就行了，以下代码复数部分在 2.77 的基础上添加，一般数字和有理数在书上 2.5.1 的基础上添加
```
(define (equ? x y) (apply-generic 'equ? x y))

; 一般数字
(put 'equ? '(scheme-number scheme-number) =)

; 有理数
(define (equ? x y)
  ;; 先化简为最简有理数
  (let ((simple-x (make-rat (numer x) (denom x)))
        (simple-y (make-rat (numer y) (denom y))))
    (and (= (numer simple-x) (numer simple-y))
         (= (denom simple-x) (denom simple-y)))))

(put 'equ? '(rational rational)
     (lambda (x y) (equ? x y)))

; 复数，只用在 install-complex-package 里添加就行
(define (equ? z1 z2)
  (and (= (real-part z1) (real-part z2))
       (= (imag-part z1) (imag-part z2))))

(put 'equ? '(complex complex)
     (lambda (z1 z2) (equ? z1 z2)))


; 测试
(install-scheme-number-package)
(define n1 (make-scheme-number 5))
(define n2 (make-scheme-number 10))
(define n3 (make-scheme-number 10))
(equ? n1 n2)
(equ? n2 n3)

(newline)
(install-rational-package)
(define r1 (make-rational 5 5))
(define r2 (make-rational 10 10))
(define r3 (make-rational 10 20))
(equ? r1 r2)
(equ? r2 r3)

(newline)
(install-rectangular-package)
(install-polar-package)
(install-complex-package)
(define z1 (make-complex-from-real-imag 3 4))
(define z2 (make-complex-from-real-imag 3 4))
(define z3 (make-complex-from-real-imag 3 5))
(equ? z1 z2)
(equ? z2 z3)

; 结果如下
'done
#f
#t

'done
#t
#f

'done
'done
'done
#t
#f
```
> 看了一下别人的答案，有理数部分可以通过十字相乘来使得答案更简单。
```
(define (equ? x y) 
   (= (* (numer x) (denom y)) (* (numer y) (denom x)))) 
```

### Exercise 2.80
> Define a generic predicate =zero? that tests if its argument is zero, and install it in the generic arithmetic package. This operation should work for ordinary numbers, rational numbers, and complex numbers.
---
> 这道题更简单，直接与0相比较就行，以下代码在 2.79 的基础上修改
```
(define (=zero? x) (apply-generic '=zero? x))

; 一般数字
(put '=zero? '(scheme-number) (lambda (x) (= x 0)))

; 有理数
(put '=zero? '(rational) (lambda (x) (= (numer x) 0)))

; 复数，这里我有点奇怪，用 (= (magnitude z) 0) 实现居然检查不出来，我也没找到原因是啥
(put '=zero? '(complex) (lambda (z) (= (real-part z) (imag-part z) 0)))

(install-scheme-number-package)
(define n1 (make-scheme-number 0))
(define n2 (make-scheme-number 10))
(=zero? n1)
(=zero? n2)

(newline)
(install-rational-package)
(define r1 (make-rational 5 10))
(define r2 (make-rational 0 20))
(=zero? r1)
(=zero? r2)

(newline)
(install-rectangular-package)
(install-polar-package)
(install-complex-package)
(define z1 (make-complex-from-real-imag 3 4))
(define z2 (make-complex-from-real-imag 0 0))
(=zero? z1)
(=zero? z2)

; 执行结果
'done
#t
#f

'done
#f
#t

'done
'done
'done
#f
#t
```

## 2.5.2 Combining Data of Different Types

### Exercise2.81
> Louis Reasoner has noticed that apply-generic may try to coerce the arguments to each other’s type even if they already have the same type. Therefore, he reasons, we need to put procedures in the coercion table to coerce arguments of each type to their own type. For example, in addition to the scheme-number->complex coercion shown above, he would do:
```
(define (scheme-number->scheme-number n) n)
(define (complex->complex z) z)
(put-coercion 'scheme-number
              'scheme-number
              scheme-number->scheme-number)
(put-coercion 'complex 'complex complex->complex)
```
>> a. With Louis’s coercion procedures installed, what happens if apply-generic is called with two arguments of type scheme-number or two arguments of type complex for an operation that is not found in the table for those types? For example, assume that we’ve defined a generic exponentiation operation:
```
(define (exp x y) (apply-generic 'exp x y))
```
>> and have put a procedure for exponentiation in the Scheme-number package but not in any other package:
```
;; following added to Scheme-number package
(put 'exp '(scheme-number scheme-number)
     (lambda (x y) (tag (expt x y))))
     ; using primitive expt
```
>> What happens if we call exp with two complex numbers as arguments?

>> b. Is Louis correct that something had to be done about coercion with arguments of the same type, or does apply-generic work correctly as is?

>> c. c. Modify apply-generic so that it doesn’t try coercion if the two arguments have the same type.
---
> 这道题要想看到实际执行结果，首先要实现 put-coercion 和 get-coercion 过程，我从网上找到的代码如下：
```
(define *operation-table* (make-hash))

; A function to add a coercion entry to the table
(define (put-coercion type1 type2 fn)
  (hash-set! *operation-table* (list type1 type2) fn))

; A function to get a coercion function from type1 to type2
(define (get-coercion type1 type2)
  (hash-ref *operation-table* (list type1 type2) #f))
```
> a. 我在 2.80 和本节的新 apply-generic 的基础上添加了本题所需的代码，然后生成了2个复数 3+4i 和 5+12i，第一次直接运行程序陷入了无穷递归调用，所以我添加了 trace 函数追踪 apply-generic 的调用情况。
```
(require racket/trace)

(define (scheme-number->scheme-number n) n)
(define (complex->complex z) z)
(put-coercion 'scheme-number
              'scheme-number
              scheme-number->scheme-number)
(put-coercion 'complex 'complex complex->complex)


(install-rectangular-package)
(install-polar-package)
(install-complex-package)
(define c1 (make-complex-from-real-imag 3 4))
(define c2 (make-complex-from-real-imag 5 12))

(trace apply-generic)
(exp c1 c2)

; 结果如下
>(apply-generic
  'exp
  '(complex rectangular 3 . 4)
  '(complex rectangular 5 . 12))
>(apply-generic
  'exp
  '(complex rectangular 3 . 4)
  '(complex rectangular 5 . 12))
...
```
> 可以看出现在的程序在找不到对应的过程时，不停使用相同的参数调用 apply-generic 过程。

> b. 很显然 Louis 的代码对于2个参数是相同类型时的情况是不正确的，不仅没有解决相同类型参数的问题，反而使得问题更严重了。因为没有添加强制类型转换过程时，对复数求 exp 时，程序会报错：`No method for these types '(exp (complex complex))`，修改之后反而会死循环。

> 因为修改后，`(get-coercion 'complex 'complex)` 可以找到从 coercion 表中找到对应的过程，所以 apply-generic 过程里的 t1->t2 条件就成立了，开始执行 `(apply-generic op (t1->t2 a1) a2)`。但是 t1->t2 会返回自身， `(t1->t2 a1)` 结果为 a1，因此程序就会不断循环执行，如下所示：
```
(get-coercion 'complex 'complex)
(apply-generic op (t1->t2 a1) a2)
(apply-generic op a1 a2)

(get-coercion 'complex 'complex)
(apply-generic op (t1->t2 a1) a2)
(apply-generic op a1 a2)

(get-coercion 'complex 'complex)
(apply-generic op (t1->t2 a1) a2)
(apply-generic op a1 a2)

...
```
> c. 要解决死循环的问题，只要在判断 t1->t2 之前先判断 t1 和 t2 是否是相同类型，如果类型相同就不进行强制类型转换。
```
(define (apply-generic op . args) 
  (define (no-method type-tags) 
    (error "No method for these types" 
           (list op type-tags))) 
  
  (let ((type-tags (map type-tag args))) 
    (let ((proc (get op type-tags))) 
      (if proc 
          (apply proc (map contents args)) 
          (if (= (length args) 2) 
              (let ((type1 (car type-tags)) 
                    (type2 (cadr type-tags)) 
                    (a1 (car args)) 
                    (a2 (cadr args)))
                ; 判断两个参数的类型是否相同
                (if (equal? type1 type2) 
                    (no-method type-tags) 
                    (let ((t1->t2 (get-coercion type1 type2)) 
                          (t2->t1 (get-coercion type2 type1)) 
                          (a1 (car args)) 
                          (a2 (cadr args))) 
                      (cond (t1->t2 
                             (apply-generic op (t1->t2 a1) a2)) 
                            (t2->t1 
                             (apply-generic op a1 (t2->t1 a2))) 
                            (else (no-method type-tags)))))) 
              (no-method type-tags))))))
```
> 再次执行，得到如下反馈信息：`No method for these types '(exp (complex complex))`

### Exercise 2.82
> Show how to generalize apply-generic to handle coercion in the general case of multiple arguments. One strategy is to attempt to coerce all the arguments to the type of the first argument, 
then to the type of the second argument, and so on. Give an example of a situation where this strategy (and likewise the two-argument version given above) is not sufficiently general.
(Hint: Consider the case where there are some suitable mixed-type operations present in the table that will not be tried.)
---
> 这道题还是挺难的，题目的提示是通过一个双循环来依次进行类型转换，我参考别人的代码修改了很久最后才能跑通，用下面的代码替换上一题的 apply-generic 过程，可以验证是否能用。
```
(define (apply-generic op . args) 
  (define (no-method type-tags) 
    (error "No method for these types" 
           (list op type-tags)))
  
  (define (type-tags args) 
         (map type-tag args))

  ; 对每一个参数尝试进行强制类型转换
  (define (try-coerce-to target)
    (map (lambda (origin)
           (if (eq? (type-tag origin) (type-tag target))
               (lambda (x) x)   ; 如果类型一致，不进行转换
               (let ((coercor (get-coercion (type-tag origin) (type-tag target)))) 
                 (if coercor 
                     (coercor origin) 
                     origin)))) 
           args))
  
  (define (iterate next) 
    (if (null? next)
        (no-method (type-tags args)) 
        (let ((coerced (try-coerce-to (car next)))) 
          (let ((proc (get op (type-tags coerced)))) 
            (if proc 
                (apply proc (map contents coerced)) 
                (iterate (cdr next))))))) 
  
  (let ((proc (get op (type-tags args)))) 
    (if proc 
        (apply proc (map contents args)) 
        (iterate args))))
```

### Exercise 2.83
> Suppose you are designing a generic arithmetic system for dealing with the tower of types shown in Figure 2.25: integer, rational, real, complex. For each type (except complex), 
design a procedure that raises objects of that type one level in the tower. Show how to install a generic raise operation that will work for each type (except complex).
---
> 这道题挺简单的，只要在每个包里用下一级的构造方法生成符合下一级规则的数就行。因为有理数本身就可以直接看成实数，所以我没有写有理数到实数和实数到复数的转换过程，这样直接在 2.81 的基础上修改就行了。
```
(define (raise x) (apply-generic 'raise x))

; interger to rational，在 scheme-number 包添加如下代码
(put 'raise '(scheme-number) (lambda (x) make-rational x 1))

; rational to complex，在 rational 包添加如下代码
(put 'raise '(rational) (lambda (x) (make-complex-from-real-imag x 0)))

; 如果要实现有理数到实数的转换，只要将有理数转换为分子分母相除再乘以 1.0 即可
```
> 重做：这道题确实不复杂，只要依次实现 integer -> rational -> real -> complex 的转换逻辑就行了，以下是修改后的完整代码
```
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

(define (apply-generic op . args) 
  (define (no-method type-tags) 
    (error "No method for these types" 
           (list op type-tags)))
  
  (define (type-tags args) 
    (map type-tag args))

  ; 对每一个参数尝试进行强制类型转换
  (define (try-coerce-to target)
    (map (lambda (origin)
           (if (eq? (type-tag origin) (type-tag target))
               (lambda (x) x)   ; 如果类型一致,不进行转换
               (let ((coercor (get-coercion (type-tag origin) (type-tag target)))) 
                 (if coercor 
                     (coercor origin) 
                     origin)))) 
         args))
  
  (define (iterate next) 
    (if (null? next)
        (no-method (type-tags args)) 
        (let ((coerced (try-coerce-to (car next)))) 
          (let ((proc (get op (type-tags coerced)))) 
            (if proc 
                (apply proc (map contents coerced)) 
                (iterate (cdr next))))))) 
  
  (let ((proc (get op (type-tags args)))) 
    (if proc 
        (apply proc (map contents args)) 
        (iterate args))))

(define (add x y) (apply-generic 'add x y))
(define (sub x y) (apply-generic 'sub x y))
(define (mul x y) (apply-generic 'mul x y))
(define (div x y) (apply-generic 'div x y))
(define (equ? x y) (apply-generic 'equ? x y))
(define (=zero? x) (apply-generic '=zero? x))
(define (exp x y) (apply-generic 'exp x y))
(define (raise x) (apply-generic 'raise x))

;; 整数运算包
(define (install-integer-package)
  (define (tag x) (attach-tag 'integer x))
  (put 'add '(integer integer)
       (lambda (x y) (tag (+ x y))))
  (put 'sub '(integer integer)
       (lambda (x y) (tag (- x y))))
  (put 'mul '(integer integer)
       (lambda (x y) (tag (* x y))))
  (put 'div '(integer integer)
       (lambda (x y) (tag (/ x y))))
  (put 'equ? '(integer integer) =)
  (put '=zero? '(integer) (lambda (x) (= x 0)))
  (put 'exp '(integer integer)
       ; using primitive expt
       (lambda (x y) (attach-tag 'integer (expt x y))))
  (put 'raise '(integer)
       (lambda (x) (make-rational x 1)))
  (put 'make 'integer
       (lambda (x) (attach-tag 'integer x))))

(define (make-integer n)
  ((get 'make 'integer) n))

;; 有理数
(define (install-rational-package)
  ;; internal procedures
  (define (numer x) (car x))
  (define (denom x) (cdr x))
  (define (make-rat n d)
    (let ((g (gcd n d)))
      (cons (/ n g) (/ d g))))
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
  (define (equ? x y)
    ;; 先化简为最简有理数
    (let ((simple-x (make-rat (numer x) (denom x)))
          (simple-y (make-rat (numer y) (denom y))))
      (and (= (numer simple-x) (numer simple-y))
           (= (denom simple-x) (denom simple-y)))))

  ;; 用十字相乘更简单
  ;; (define (equ? x y) (= (* (numer x) (denom y)) (* (numer y) (denom x))))
  
  ;; interface to rest of the system
  (define (tag x) (attach-tag 'rational x))
  (put 'add '(rational rational)
       (lambda (x y) (tag (add-rat x y))))
  (put 'sub '(rational rational)
       (lambda (x y) (tag (sub-rat x y))))
  (put 'mul '(rational rational)
       (lambda (x y) (tag (mul-rat x y))))
  (put 'div '(rational rational)
       (lambda (x y) (tag (div-rat x y))))
  (put 'equ? '(rational rational)
       (lambda (x y) (equ? x y)))
  (put '=zero? '(rational) (lambda (x) (= (numer x) 0)))
  (put 'raise '(rational) (lambda (x) (make-real (/ (numer x) (denom x)))))
  (put 'make 'rational
       (lambda (n d) (tag (make-rat n d))))
  'done)

(define (make-rational n d)
  ((get 'make 'rational) n d))

;; 实数
(define (install-real-package)
  (define (tag x) (attach-tag 'real x))
  (put 'add '(real real)
       (lambda (x y) (tag (+ x y))))
  (put 'sub '(real real)
       (lambda (x y) (tag (- x y))))
  (put 'mul '(real real)
       (lambda (x y) (tag (* x y))))
  (put 'div '(real real)
       (lambda (x y) (tag (/ x y))))
  (put 'equ? '(real real)
       (lambda (x y) (= x y)))
  (put '=zero? '(real)
       (lambda (x) (= x 0)))
  (put 'raise '(real)
       (lambda (x) (make-complex-from-real-imag x 0)))
  (put 'make 'real (lambda (x) (tag x))))

(define (make-real r)
  ((get 'make 'real) r))


;; 复数
(define (install-rectangular-package)
  ;; internal procedures
  (define (real-part z) (car z))
  (define (imag-part z) (cdr z))
  (define (make-from-real-imag x y) (cons x y))
  (define (magnitude z)
    (sqrt (+ (square (real-part z))
             (square (imag-part z)))))
  (define (angle z)
    (atan (imag-part z) (real-part z)))
  (define (make-from-mag-ang r a)
    (cons (* r (cos a)) (* r (sin a))))
  ;; interface to the rest of the system
  (define (tag x) (attach-tag 'rectangular x))
  (put 'real-part '(rectangular) real-part)
  (put 'imag-part '(rectangular) imag-part)
  (put 'magnitude '(rectangular) magnitude)
  (put 'angle '(rectangular) angle)
  (put 'make-from-real-imag 'rectangular
       (lambda (x y) (tag (make-from-real-imag x y))))
  (put 'make-from-mag-ang 'rectangular
       (lambda (r a) (tag (make-from-mag-ang r a))))
  'done)

(define (install-polar-package)
  ;; internal procedures
  (define (magnitude z) (car z))
  (define (angle z) (cdr z))
  (define (make-from-mag-ang r a) (cons r a))
  (define (real-part z) (* (magnitude z) (cos (angle z))))
  (define (imag-part z) (* (magnitude z) (sin (angle z))))
  (define (make-from-real-imag x y)
    (cons (sqrt (+ (square x) (square y)))
          (atan y x)))
  ;; interface to the rest of the system
  (define (tag x) (attach-tag 'polar x))
  (put 'real-part '(polar) real-part)
  (put 'imag-part '(polar) imag-part)
  (put 'magnitude '(polar) magnitude)
  (put 'angle '(polar) angle)
  (put 'make-from-real-imag 'polar
       (lambda (x y) (tag (make-from-real-imag x y))))
  (put 'make-from-mag-ang 'polar
       (lambda (r a) (tag (make-from-mag-ang r a))))
  'done)

(define (install-complex-package)
  ;; imported procedures from rectangular and polar packages
  (define (make-from-real-imag x y)
    ((get 'make-from-real-imag 'rectangular) x y))
  (define (make-from-mag-ang r a)
    ((get 'make-from-mag-ang 'polar) r a))
  ;; internal procedures
  (define (add-complex z1 z2)
    (make-from-real-imag (+ (real-part z1) (real-part z2))
                         (+ (imag-part z1) (imag-part z2))))
  (define (sub-complex z1 z2)
    (make-from-real-imag (- (real-part z1) (real-part z2))
                         (- (imag-part z1) (imag-part z2))))
  (define (mul-complex z1 z2)
    (make-from-mag-ang (* (magnitude z1) (magnitude z2))
                       (+ (angle z1) (angle z2))))
  (define (div-complex z1 z2)
    (make-from-mag-ang (/ (magnitude z1) (magnitude z2))
                       (- (angle z1) (angle z2))))
  (define (equ? z1 z2)
    (and (= (real-part z1) (real-part z2))
         (= (imag-part z1) (imag-part z2))))
  ;; interface to rest of the system
  (define (tag z) (attach-tag 'complex z))
  (put 'add '(complex complex)
       (lambda (z1 z2) (tag (add-complex z1 z2))))
  (put 'sub '(complex complex)
       (lambda (z1 z2) (tag (sub-complex z1 z2))))
  (put 'mul '(complex complex)
       (lambda (z1 z2) (tag (mul-complex z1 z2))))
  (put 'div '(complex complex)
       (lambda (z1 z2) (tag (div-complex z1 z2))))
  (put 'equ? '(complex complex)
       (lambda (z1 z2) (equ? z1 z2)))
  (put '=zero? '(complex) (lambda (z) (= (real-part z) (imag-part z) 0)))
  (put 'make-from-real-imag 'complex
       (lambda (x y) (tag (make-from-real-imag x y))))
  (put 'make-from-mag-ang 'complex
       (lambda (r a) (tag (make-from-mag-ang r a))))
  (put 'real-part '(complex) real-part)
  (put 'imag-part '(complex) imag-part)
  (put 'magnitude '(complex) magnitude)
  (put 'angle '(complex) angle)
  'done)

(define (make-complex-from-real-imag x y)
  ((get 'make-from-real-imag 'complex) x y))
(define (make-complex-from-mag-ang r a)
  ((get 'make-from-mag-ang 'complex) r a))

(define (real-part z) (apply-generic 'real-part z)) 
(define (imag-part z) (apply-generic 'imag-part z)) 
(define (magnitude z) (apply-generic 'magnitude z)) 
(define (angle z) (apply-generic 'angle z))


(install-integer-package) 
(install-rational-package)
(install-real-package)
(install-rectangular-package) 
(install-polar-package) 
(install-complex-package) 
  
(define n1 (make-integer 1)) 
(define n2 (make-integer 2)) 
  
(define r1 (make-rational 2 3)) 
(define r2 (make-rational 2 5)) 

(define real1 (make-real 5))
(define real2 (make-real 3.2))

(raise n1)
(raise n2)

(raise r1)
(raise r2)

(raise real1)
(raise real2)

; 执行结果
'(rational 1 . 1)
'(rational 2 . 1)
'(real . 2/3)
'(real . 2/5)
'(complex rectangular 5 . 0)
'(complex rectangular 3.2 . 0)
```
> base.rkt 里面是常用但是 racket 没有定义的一些函数，这里主要用到了 put 和 get，如下图所示：
```
(provide put)
(provide get)

(define *operation-table* (make-hash))

(define (put op-type op-name procedure)
  (hash-set! *operation-table* (list op-type op-name) procedure))

(define (get op-type op-name)
  (hash-ref *operation-table* (list op-type op-name) #f))
```

### Exercise 2.84
> Using the raise operation of Exercise 2.83, modify the apply-generic procedure so that it coerces its arguments to have the same type by the method of successive raising, as discussed in this section. 
You will need to devise a way to test which of two types is higher in the tower. Do this in a manner that is “compatible” with the rest of the system and will not lead to problems in adding new levels to the tower.
---
> 这道题难度也不大，而且 tower 结构更简单，参考 2.81 和 2.83 再针对参数类型分别进行处理就行了
```
(define (apply-generic op . args) 
  (define (no-method type-tags) 
    (error "No method for these types" 
           (list op type-tags)))
  
  (define (type-tags args) 
    (map type-tag args))

  ; 将当前的类型升级为上一级，如果不存在对应的转换函数，返回 false
  (define (tower-raise origin target)
    (let ((o-type (type-tag origin))
          (t-type (type-tag target)))
      (cond ((eq? o-type t-type)
             origin)
            ((get 'raise (list o-type))
             (tower-raise ((get 'raise (list o-type)) (contents origin) target)))
            (else false))))

  (let ((proc (get op (type-tags args)))) 
    (if proc 
        (apply proc (map contents args))
        (if (= (length args) 2)
            ;; 假设类型以简单的 tower 形式排序，从低到高
            (let ((curr (car args))
                  (next (cadr args)))
              (cond ((eq? (type-tag curr) (type-tag next))
                     (no-method (type-tags args)))
                    ((tower-raise curr next)
                     (apply-generic op (tower-raise curr next) next))
                    ((tower-raise curr next)
                     (apply-generic op (tower-raise next curr) curr))
                    (else (no-method (type-tags args)))))
            (no-method (type-tags args))))))
```
> 重做：这道题开始怎么都跑不通，后来我一顿乱改，忽然就行了。对比了一下原来的代码，变化主要是把 apply-generic 中关于参数类型的判断删掉了一个。完整代码如下：
```
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

(define (apply-generic op . args) 
  (define (no-method type-tags) 
    (error "No method for these types" 
           (list op type-tags)))
  
  (define (type-tags args) 
    (map type-tag args))

  ; 将当前的类型升级为上一级，如果不存在对应的转换函数，返回 false
  (define (tower-raise origin target)
    (let ((o-type (type-tag origin))
          (t-type (type-tag target)))
      (cond ((eq? o-type t-type)    ; 如果参数类型相同，不需要
             origin)
            ((get 'raise (list o-type))
             (tower-raise ((get 'raise (list o-type)) (contents origin)) target))
            (else false))))

  (let ((proc (get op (type-tags args)))) 
    (if proc 
        (apply proc (map contents args))
        (if (= (length args) 2)
            ;; 假设类型以简单的 tower 形式排序，从低到高
            (let ((a1 (car args))
                  (a2 (cadr args)))
              (cond ((tower-raise a1 a2)
                     (apply-generic op (tower-raise a1 a2) a2))
                    ((tower-raise a2 a1)
                     (apply-generic op a1 (tower-raise a2 a1)))
                    (else (no-method (type-tags args)))))
            (no-method (type-tags args))))))

(define (add x y) (apply-generic 'add x y))
(define (sub x y) (apply-generic 'sub x y))
(define (mul x y) (apply-generic 'mul x y))
(define (div x y) (apply-generic 'div x y))
(define (equ? x y) (apply-generic 'equ? x y))
(define (=zero? x) (apply-generic '=zero? x))
(define (exp x y) (apply-generic 'exp x y))
(define (raise x) (apply-generic 'raise x))

;; 整数运算包
(define (install-integer-package)
  (define (tag x) (attach-tag 'integer x))
  (put 'add '(integer integer)
       (lambda (x y) (tag (+ x y))))
  (put 'sub '(integer integer)
       (lambda (x y) (tag (- x y))))
  (put 'mul '(integer integer)
       (lambda (x y) (tag (* x y))))
  (put 'div '(integer integer)
       (lambda (x y) (tag (round (/ x y)))))     ; 四舍五入
  (put 'equ? '(integer integer) =)
  (put '=zero? '(integer) (lambda (x) (= x 0)))
  (put 'exp '(integer integer)
       ; using primitive expt
       (lambda (x y) (attach-tag 'integer (expt x y))))
  (put 'raise '(integer)
       (lambda (x) (make-rational x 1)))
  (put 'make 'integer
       (lambda (x) (attach-tag 'integer x))))

(define (make-integer n)
  ((get 'make 'integer) n))

;; 有理数
(define (install-rational-package)
  ;; internal procedures
  (define (numer x) (car x))
  (define (denom x) (cdr x))
  (define (make-rat n d)
    (let ((g (gcd n d)))
      (cons (/ n g) (/ d g))))
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
  (define (equ? x y)
    ;; 先化简为最简有理数
    (let ((simple-x (make-rat (numer x) (denom x)))
          (simple-y (make-rat (numer y) (denom y))))
      (and (= (numer simple-x) (numer simple-y))
           (= (denom simple-x) (denom simple-y)))))

  ;; 用十字相乘更简单
  ;; (define (equ? x y) (= (* (numer x) (denom y)) (* (numer y) (denom x))))
  
  ;; interface to rest of the system
  (define (tag x) (attach-tag 'rational x))
  (put 'add '(rational rational)
       (lambda (x y) (tag (add-rat x y))))
  (put 'sub '(rational rational)
       (lambda (x y) (tag (sub-rat x y))))
  (put 'mul '(rational rational)
       (lambda (x y) (tag (mul-rat x y))))
  (put 'div '(rational rational)
       (lambda (x y) (tag (div-rat x y))))
  (put 'equ? '(rational rational)
       (lambda (x y) (equ? x y)))
  (put '=zero? '(rational) (lambda (x) (= (numer x) 0)))
  (put 'raise '(rational)
       (lambda (x) (make-real (/ (numer x) (denom x)))))
  (put 'make 'rational
       (lambda (n d) (tag (make-rat n d))))
  'done)

(define (make-rational n d)
  ((get 'make 'rational) n d))

;; 实数，用小数形式近似表示
(define (install-real-package)
  (define (tag x) (attach-tag 'real x))
  (put 'add '(real real)
       (lambda (x y) (tag (+ x y))))
  (put 'sub '(real real)
       (lambda (x y) (tag (- x y))))
  (put 'mul '(real real)
       (lambda (x y) (tag (* x y))))
  (put 'div '(real real)
       (lambda (x y) (tag (/ x y))))
  (put 'equ? '(real real)
       (lambda (x y) (= x y)))
  (put '=zero? '(real)
       (lambda (x) (= x 0)))
  (put 'raise '(real)
       (lambda (x) (make-complex-from-real-imag x 0)))
  (put 'make 'real (lambda (x) (tag (* 1.0 x)))))

(define (make-real r)
  ((get 'make 'real) r))


;; 复数
(define (install-rectangular-package)
  ;; internal procedures
  (define (real-part z) (car z))
  (define (imag-part z) (cdr z))
  (define (make-from-real-imag x y) (cons x y))
  (define (magnitude z)
    (sqrt (+ (square (real-part z))
             (square (imag-part z)))))
  (define (angle z)
    (atan (imag-part z) (real-part z)))
  (define (make-from-mag-ang r a)
    (cons (* r (cos a)) (* r (sin a))))
  ;; interface to the rest of the system
  (define (tag x) (attach-tag 'rectangular x))
  (put 'real-part '(rectangular) real-part)
  (put 'imag-part '(rectangular) imag-part)
  (put 'magnitude '(rectangular) magnitude)
  (put 'angle '(rectangular) angle)
  (put 'make-from-real-imag 'rectangular
       (lambda (x y) (tag (make-from-real-imag x y))))
  (put 'make-from-mag-ang 'rectangular
       (lambda (r a) (tag (make-from-mag-ang r a))))
  'done)

(define (install-polar-package)
  ;; internal procedures
  (define (magnitude z) (car z))
  (define (angle z) (cdr z))
  (define (make-from-mag-ang r a) (cons r a))
  (define (real-part z) (* (magnitude z) (cos (angle z))))
  (define (imag-part z) (* (magnitude z) (sin (angle z))))
  (define (make-from-real-imag x y)
    (cons (sqrt (+ (square x) (square y)))
          (atan y x)))
  ;; interface to the rest of the system
  (define (tag x) (attach-tag 'polar x))
  (put 'real-part '(polar) real-part)
  (put 'imag-part '(polar) imag-part)
  (put 'magnitude '(polar) magnitude)
  (put 'angle '(polar) angle)
  (put 'make-from-real-imag 'polar
       (lambda (x y) (tag (make-from-real-imag x y))))
  (put 'make-from-mag-ang 'polar
       (lambda (r a) (tag (make-from-mag-ang r a))))
  'done)

(define (install-complex-package)
  ;; imported procedures from rectangular and polar packages
  (define (make-from-real-imag x y)
    ((get 'make-from-real-imag 'rectangular) x y))
  (define (make-from-mag-ang r a)
    ((get 'make-from-mag-ang 'polar) r a))
  ;; internal procedures
  (define (add-complex z1 z2)
    (make-from-real-imag (+ (real-part z1) (real-part z2))
                         (+ (imag-part z1) (imag-part z2))))
  (define (sub-complex z1 z2)
    (make-from-real-imag (- (real-part z1) (real-part z2))
                         (- (imag-part z1) (imag-part z2))))
  (define (mul-complex z1 z2)
    (make-from-mag-ang (* (magnitude z1) (magnitude z2))
                       (+ (angle z1) (angle z2))))
  (define (div-complex z1 z2)
    (make-from-mag-ang (/ (magnitude z1) (magnitude z2))
                       (- (angle z1) (angle z2))))
  (define (equ? z1 z2)
    (and (= (real-part z1) (real-part z2))
         (= (imag-part z1) (imag-part z2))))
  ;; interface to rest of the system
  (define (tag z) (attach-tag 'complex z))
  (put 'add '(complex complex)
       (lambda (z1 z2) (tag (add-complex z1 z2))))
  (put 'sub '(complex complex)
       (lambda (z1 z2) (tag (sub-complex z1 z2))))
  (put 'mul '(complex complex)
       (lambda (z1 z2) (tag (mul-complex z1 z2))))
  (put 'div '(complex complex)
       (lambda (z1 z2) (tag (div-complex z1 z2))))
  (put 'equ? '(complex complex)
       (lambda (z1 z2) (equ? z1 z2)))
  (put '=zero? '(complex) (lambda (z) (= (real-part z) (imag-part z) 0)))
  (put 'make-from-real-imag 'complex
       (lambda (x y) (tag (make-from-real-imag x y))))
  (put 'make-from-mag-ang 'complex
       (lambda (r a) (tag (make-from-mag-ang r a))))
  (put 'real-part '(complex) real-part)
  (put 'imag-part '(complex) imag-part)
  (put 'magnitude '(complex) magnitude)
  (put 'angle '(complex) angle)
  'done)

(define (make-complex-from-real-imag x y)
  ((get 'make-from-real-imag 'complex) x y))
(define (make-complex-from-mag-ang r a)
  ((get 'make-from-mag-ang 'complex) r a))

(define (real-part z) (apply-generic 'real-part z)) 
(define (imag-part z) (apply-generic 'imag-part z)) 
(define (magnitude z) (apply-generic 'magnitude z)) 
(define (angle z) (apply-generic 'angle z))


(install-integer-package) 
(install-rational-package)
(install-real-package)
(install-rectangular-package) 
(install-polar-package) 
(install-complex-package) 
  
(define n1 (make-integer 1)) 
(define n2 (make-integer 2)) 
  
(define rat1 (make-rational 2 3)) 
(define rat2 (make-rational 2 5)) 

(define r1 (make-real 5))
(define r2 (make-real 3.2))

(define c1 (make-complex-from-real-imag 10 0))
(define c2 (make-complex-from-real-imag 10 -20))

(newline)
(display "测试样例")
(newline)

(add n1 rat1)
(add rat1 n1)
(add r2 rat1)
(add c2 rat2)
(sub n1 r1)
(sub r1 n1)
(mul n1 c1)
(mul c1 n1)
(div n1 c2)
(div c2 n2)

; 检查对 apply-generic 修改是否影响到了前面的其他过程
(newline)
(display "检查对 apply-generic 修改是否影响到了前面的其他过程")
(newline)
(add n1 n2)
(sub n1 n2)
(mul n1 n2)
(div n1 n2)
(add rat1 (raise n1))
(sub (raise n2) rat2)
(mul rat1 (raise n2))
(div (raise n1) rat2)
(add r1 (raise rat1))
(sub (raise rat1) r2)
(mul r1 (raise rat2))
(div (raise rat2) r2)
(add c1 (raise r1))
(sub (raise r1) c2)
(mul c1 (raise r2))
(div (raise r2) c2)
(exp n2 n2)

; 结果如下
测试样例
'(rational 5 . 3)
'(rational 5 . 3)
'(real . 3.8666666666666667)
'(complex rectangular 10.4 . -20)
'(real . -4.0)
'(real . 4.0)
'(complex polar 10.000000000139897 . 0)
'(complex polar 10.000000000139897 . 0)
'(complex polar 0.04472135953997919 . 1.1071487177940904)
'(complex polar 11.180339370551705 . -1.1071487177940904)

检查对 apply-generic 修改是否影响到了前面的其他过程
'(integer . 3)
'(integer . -1)
'(integer . 2)
'(integer . 0)
'(rational 5 . 3)
'(rational 8 . 5)
'(rational 4 . 3)
'(rational 5 . 2)
'(real . 5.666666666666667)
'(real . -2.5333333333333337)
'(real . 2.0)
'(real . 0.125)
'(complex rectangular 15.0 . 0)
'(complex rectangular -5.0 . 20)
'(complex polar 32.00000006647572 . 0)
'(complex polar 0.14310835082321982 . 1.1071487177940904)
'(integer . 4)
```

### Exercise 2.85
> This section mentioned a method for “simplifying” a data object by lowering it in the tower of types as far as possible. Design a procedure drop that accomplishes this for the tower described in Exercise 2.83. 
The key is to decide, in some general way, whether an object can be lowered. For example, the complex number 1.5 + 0i can be lowered as far as real, the complex number 1 + 0i can be lowered as far as integer, 
and the complex number 2 +3i cannot be lowered at all. Here is a plan for determining whether an object can be lowered: Begin by defining a generic operation project that “pushes” an object down in the tower. 
For example, projecting a complex number would involve throwing away the imaginary part. Then a number can be dropped if, when we project it and raise the result back to the type we started with, we end up with 
something equal to what we started with. Show how to implementthis idea indetail, by writing a drop procedure that drops an object as far as possible. You will need to design the various projection operations53 
and install project as a generic operation in the system. You will also need to make use of a generic equality predicate, such as described in Exercise 2.79. Finally, use drop to rewrite apply-generic 
from Exercise 2.84 so that it “simplifies” its answers.
---
```
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

; 将当前的类型升级为上一级,如果不存在对应的转换函数,返回 false
(define (tower-raise origin target)
  (let ((o-type (type-tag origin))
        (t-type (type-tag target)))
    (cond ((eq? o-type t-type)    
           origin)
          ((get 'raise (list o-type))
           (tower-raise ((get 'raise (list o-type)) (contents origin)) target))
          (else false))))

(define (raise origin)
  (let ((raise-proc (get 'raise (list (type-tag origin)))))
    (if raise-proc
        (raise-proc (contents origin))
        false)))

(define (project origin)
  (let ((project-proc (get 'project (list (type-tag origin)))))
    (if project-proc
        (project-proc (contents origin))
        false)))

;; 在不失精度地前提下,把一个数的类型降到最底层
(define (drop origin)
  (if (pair? origin)    ; 过滤 false 等没有 type-tag 的参数
      (let ((project-number (project origin)))
        (if (and project-number
                 (equ? origin (raise project-number)))
            (drop project-number)
            origin))
      origin))

(define (apply-generic op . args) 
  (define (no-method type-tags) 
    (error "No method for these types" 
           (list op type-tags)))

  (let ((type-tags (map type-tag args)))
    (let ((proc (get op type-tags))) 
      (if proc 
          (drop (apply proc (map contents args)))
          (if (and (= (length args) 2)
                   (not (equal? (car type-tags) (cadr type-tags))))    ; 如果参数类型相同,不需要转换
              ;; 假设类型以简单的 tower 形式排序,从低到高
              (let ((a1 (car args))
                    (a2 (cadr args)))
                (cond ((tower-raise a1 a2)
                       (apply-generic op (tower-raise a1 a2) a2))
                      ((tower-raise a2 a1)
                       (apply-generic op a1 (tower-raise a2 a1)))
                      (else (no-method type-tags))))
              (no-method type-tags))))))


(define (add x y) (apply-generic 'add x y))
(define (sub x y) (apply-generic 'sub x y))
(define (mul x y) (apply-generic 'mul x y))
(define (div x y) (apply-generic 'div x y))
(define (equ? x y) (apply-generic 'equ? x y))
(define (=zero? x) (apply-generic '=zero? x))
(define (exp x y) (apply-generic 'exp x y))

;; 整数运算包
(define (install-integer-package)
  (define (tag x) (attach-tag 'integer x))
  (put 'add '(integer integer)
       (lambda (x y) (tag (+ x y))))
  (put 'sub '(integer integer)
       (lambda (x y) (tag (- x y))))
  (put 'mul '(integer integer)
       (lambda (x y) (tag (* x y))))
  (put 'div '(integer integer)
       (lambda (x y) (tag (round (/ x y)))))     ; 四舍五入
  (put 'equ? '(integer integer) =)
  (put '=zero? '(integer) (lambda (x) (= x 0)))
  (put 'exp '(integer integer)
       ; using primitive expt
       (lambda (x y) (tag (expt x y))))
  (put 'raise '(integer)
       (lambda (x) (make-rational x 1)))
  (put 'make 'integer
       (lambda (x) (tag x))))

(define (make-integer n)
  ((get 'make 'integer) n))

;; 有理数
(define (install-rational-package)
  ;; internal procedures
  (define (numer x) (car x))
  (define (denom x) (cdr x))
  (define (make-rat n d)
    (let ((g (gcd n d)))
      (cons (/ n g) (/ d g))))
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
  (define (equ? x y)
    ;; 先化简为最简有理数
    (let ((simple-x (make-rat (numer x) (denom x)))
          (simple-y (make-rat (numer y) (denom y))))
      (and (= (numer simple-x) (numer simple-y))
           (= (denom simple-x) (denom simple-y)))))

  ;; 用十字相乘更简单
  ;; (define (equ? x y) (= (* (numer x) (denom y)) (* (numer y) (denom x))))
  
  ;; interface to rest of the system
  (define (tag x) (attach-tag 'rational x))
  (put 'add '(rational rational)
       (lambda (x y) (tag (add-rat x y))))
  (put 'sub '(rational rational)
       (lambda (x y) (tag (sub-rat x y))))
  (put 'mul '(rational rational)
       (lambda (x y) (tag (mul-rat x y))))
  (put 'div '(rational rational)
       (lambda (x y) (tag (div-rat x y))))
  (put 'equ? '(rational rational)
       (lambda (x y) (equ? x y)))
  (put '=zero? '(rational)
       (lambda (x) (= (numer x) 0)))
  (put 'raise '(rational)
       (lambda (x) (make-real (/ (numer x) (denom x)))))
  (put 'project '(rational)
       (lambda (x) (make-integer (round (/ (numer x) (denom x))))))
  (put 'make 'rational
       (lambda (n d) (tag (make-rat n d)))))

(define (make-rational n d)
  ((get 'make 'rational) n d))

(define (install-real-package)
  (define (tag x) (attach-tag 'real x))
  (put 'add '(real real)
       (lambda (x y) (tag (+ x y))))
  (put 'sub '(real real)
       (lambda (x y) (tag (- x y))))
  (put 'mul '(real real)
       (lambda (x y) (tag (* x y))))
  (put 'div '(real real)
       (lambda (x y) (tag (/ x y))))
  (put 'equ? '(real real)
       (lambda (x y) (= x y)))
  (put '=zero? '(real)
       (lambda (x) (= x 0)))
  (put 'raise '(real)
       (lambda (x) (make-complex-from-real-imag x 0)))
  (put 'project '(real)
       ;; 实数转为有理数没啥简单的好办法
       ;; 我采用了对实数四舍五入然后转为分母为1的有理数的逻辑
       (lambda (x) (make-rational (round x) 1)))
  (put 'make 'real (lambda (x) (tag (* 1.0 x)))))

(define (make-real r)
  ((get 'make 'real) r))


;; 复数
(define (install-rectangular-package)
  ;; internal procedures
  (define (real-part z) (car z))
  (define (imag-part z) (cdr z))
  (define (make-from-real-imag x y) (cons x y))
  
  (define (magnitude z)
    (sqrt (+ (square (real-part z))
             (square (imag-part z)))))
  (define (angle z)
    (atan (imag-part z) (real-part z)))
  (define (make-from-mag-ang r a)
    (cons (* r (cos a)) (* r (sin a))))
  
  ;; interface to the rest of the system
  (define (tag x) (attach-tag 'rectangular x))
  (put 'real-part '(rectangular) real-part)
  (put 'imag-part '(rectangular) imag-part)
  (put 'magnitude '(rectangular) magnitude)
  (put 'angle '(rectangular) angle)
  (put 'make-from-real-imag 'rectangular
       (lambda (x y) (tag (make-from-real-imag x y))))
  (put 'make-from-mag-ang 'rectangular
       (lambda (r a) (tag (make-from-mag-ang r a)))))

(define (install-polar-package)
  ;; internal procedures
  (define (magnitude z) (car z))
  (define (angle z) (cdr z))
  (define (make-from-mag-ang r a) (cons r a))
  
  (define (real-part z) (* (magnitude z) (cos (angle z))))
  (define (imag-part z) (* (magnitude z) (sin (angle z))))
  (define (make-from-real-imag x y)
    (cons (sqrt (+ (square x) (square y)))
          (atan y x)))
  
  ;; interface to the rest of the system
  (define (tag x) (attach-tag 'polar x))
  (put 'real-part '(polar) real-part)
  (put 'imag-part '(polar) imag-part)
  (put 'magnitude '(polar) magnitude)
  (put 'angle '(polar) angle)
  (put 'make-from-real-imag 'polar
       (lambda (x y) (tag (make-from-real-imag x y))))
  (put 'make-from-mag-ang 'polar
       (lambda (r a) (tag (make-from-mag-ang r a)))))

(define (install-complex-package)
  ;; imported procedures from rectangular and polar packages
  (define (make-from-real-imag x y)
    ((get 'make-from-real-imag 'rectangular) x y))
  (define (make-from-mag-ang r a)
    ((get 'make-from-mag-ang 'polar) r a))
  ;; internal procedures
  (define (add-complex z1 z2)
    (make-from-real-imag (+ (real-part z1) (real-part z2))
                         (+ (imag-part z1) (imag-part z2))))
  (define (sub-complex z1 z2)
    (make-from-real-imag (- (real-part z1) (real-part z2))
                         (- (imag-part z1) (imag-part z2))))
  (define (mul-complex z1 z2)
    (make-from-mag-ang (* (magnitude z1) (magnitude z2))
                       (+ (angle z1) (angle z2))))
  (define (div-complex z1 z2)
    (make-from-mag-ang (/ (magnitude z1) (magnitude z2))
                       (- (angle z1) (angle z2))))
  (define (equ? z1 z2)
    (and (= (real-part z1) (real-part z2))
         (= (imag-part z1) (imag-part z2))))
  ;; interface to rest of the system
  (define (tag z) (attach-tag 'complex z))
  (put 'add '(complex complex)
       (lambda (z1 z2) (tag (add-complex z1 z2))))
  (put 'sub '(complex complex)
       (lambda (z1 z2) (tag (sub-complex z1 z2))))
  (put 'mul '(complex complex)
       (lambda (z1 z2) (tag (mul-complex z1 z2))))
  (put 'div '(complex complex)
       (lambda (z1 z2) (tag (div-complex z1 z2))))
  (put 'equ? '(complex complex)
       (lambda (z1 z2) (equ? z1 z2)))
  (put '=zero? '(complex)
       (lambda (z) (= (real-part z) (imag-part z) 0)))
  (put 'project '(complex)
       (lambda (z) (make-real (real-part z))))
  (put 'make-from-real-imag 'complex
       (lambda (x y) (tag (make-from-real-imag x y))))
  (put 'make-from-mag-ang 'complex
       (lambda (r a) (tag (make-from-mag-ang r a))))
  (put 'real-part '(complex) real-part)
  (put 'imag-part '(complex) imag-part)
  (put 'magnitude '(complex) magnitude)
  (put 'angle '(complex) angle))

(define (make-complex-from-real-imag x y)
  ((get 'make-from-real-imag 'complex) x y))
(define (make-complex-from-mag-ang r a)
  ((get 'make-from-mag-ang 'complex) r a))

(define (real-part z) (apply-generic 'real-part z)) 
(define (imag-part z) (apply-generic 'imag-part z)) 
(define (magnitude z) (apply-generic 'magnitude z)) 
(define (angle z) (apply-generic 'angle z))


(install-integer-package) 
(install-rational-package)
(install-real-package)
(install-rectangular-package) 
(install-polar-package) 
(install-complex-package) 
  
(define n1 (make-integer 1)) 
(define n2 (make-integer 2)) 
  
(define rat1 (make-rational 2 3)) 
(define rat2 (make-rational 2 5)) 

(define r1 (make-real 5))
(define r2 (make-real 3.2))

(define c1 (make-complex-from-real-imag 12 0))
(define c2 (make-complex-from-mag-ang 10 (/ pi 3)))

(newline)
(display "测试样例")
(newline)

(display "测试 project")
(newline)
(project rat1)
(project rat2)
(project r1)
(project r2)
(project c1)
(project c2)

(newline)
(display "测试 drop")
(newline)
(drop rat1)
(drop rat2)
(drop r1)
(drop r2)
(drop c1)
(drop c2)


; 检查对 apply-generic 修改是否影响到了前面的其他过程
(newline)
(display "检查对 apply-generic 修改是否影响到了前面的其他过程")
(newline)

(add n1 n2)
(sub n1 n2)
(mul n1 n2)
(div n1 n2)
(add rat1 (raise n1))
(sub (raise n2) rat2)
(mul rat1 (raise n2))
(div (raise n1) rat2)
(add r1 (raise rat1))
(sub (raise rat1) r2)
(mul r1 (raise rat2))
(div (raise rat2) r2)
(add c1 (raise r1))
(sub (raise r1) c2)
(mul c1 (raise r2))
(div (raise r2) c2)
(exp n2 n2)

(add n1 rat1)
(add rat1 n1)
(add r2 rat1)
(add c2 rat2)
(sub n1 r1)
(sub r2 n2)
(newline)
(display "因为复数乘法都是用 magnitude 和 angle 表示的,所以类型都是 polar")
(newline)
(mul n1 c1)
(mul c1 n1)
(div n1 c2)
(div c2 n2)

; 执行结果
测试样例
测试 project
'(integer . 1)
'(integer . 0)
'(rational 5.0 . 1.0)
'(rational 3.0 . 1.0)
'(real . 12.0)
'(real . 5.000000000000001)

测试 drop
'(rational 2 . 3)
'(rational 2 . 5)
'(integer . 5.0)
'(real . 3.2)
'(integer . 12.0)
'(complex polar 10 . 1.0471975511965976)

检查对 apply-generic 修改是否影响到了前面的其他过程
'(integer . 3)
'(integer . -1)
'(integer . 2)
'(integer . 0)
'(rational 5 . 3)
'(rational 8 . 5)
'(rational 4 . 3)
'(rational 5 . 2)
'(real . 5.666666666666667)
'(real . -2.5333333333333337)
'(integer . 2.0)
'(real . 0.125)
'(integer . 17.0)
'(complex rectangular -8.881784197001252e-16 . -8.660254037844386)
'(real . 38.40000011894146)
'(complex polar 0.3200000006602805 . -1.0471975511965976)
'(integer . 4)
'(rational 5 . 3)
'(rational 5 . 3)
'(real . 3.8666666666666667)
'(complex rectangular 5.400000000000001 . 8.660254037844386)
'(integer . -4.0)
'(real . 1.2000000000000002)

因为复数乘法都是用 magnitude 和 angle 表示的,所以类型都是 polar
'(real . 12.000000012408687)
'(real . 12.000000012408687)
'(complex polar 0.1 . -1.0471975511965976)
'(complex polar 4.999999767694274 . 1.0471975511965976)
```

### Exercise 2.86
> Suppose we want to handle complex numbers whose real parts, imaginary parts, magnitudes, and angles can be either ordinary numbers, rational numbers, or other numbers we might wish to add to the system. Describe and implement the changes to the system needed to accommodate this. You will have to define operations such as sineandcosinethataregeneric over ordinary numbers and rational numbers.
---
```
#lang racket 
  
;;; 
;;; put-coersion & get-coersion 
;;; from https://gist.github.com/kinoshita-lab/b76a55759a0d0968cd97 
;;; 
  
(define coercion-list '()) 
  
(define (clear-coercion-list) 
  (set! coercion-list '())) 
  
(define (put-coercion type1 type2 item) 
  (if (get-coercion type1 type2) coercion-list 
      (set! coercion-list 
            (cons (list type1 type2 item) 
                  coercion-list)))) 
  
(define (get-coercion type1 type2) 
  (define (get-type1 listItem) 
    (car listItem)) 
  (define (get-type2 listItem) 
    (cadr listItem)) 
  (define (get-item listItem) 
    (caddr listItem)) 
  (define (get-coercion-iter list type1 type2) 
    (if (null? list) #f 
        (let ((top (car list))) 
          (if (and (equal? type1 (get-type1 top)) 
                   (equal? type2 (get-type2 top))) 
              (get-item top) 
              (get-coercion-iter (cdr list) type1 type2))))) 
  (get-coercion-iter coercion-list type1 type2)) 
  
;;; 
;;; Put & Get, from https://stackoverflow.com/a/19114031 
;;; 
  
(define *op-table* (make-hash)) 
(define (put op type proc) 
  (hash-set! *op-table* (list op type) proc)) 
(define (get op type) 
  (hash-ref *op-table* (list op type) #f)) 
  
;;; 
;;; Tags from 2.4.2 
;;; 
  
(define (attach-tag type-tag z) 
  (cons type-tag z)) 
  
(define (type-tag datum) 
  (if (pair? datum) 
      (car datum) 
      (error "Not a pair: TYPE-TAG" datum))) 
(define (contents datum) 
  (if (pair? datum) 
      (cdr datum) 
      (error "Not a pair: CONTENT" datum))) 
  
;;; 
;;; 2.4.3 Data-Directed Programming and Additivity 
;;; 
  
(define (install-rectangular-package) 
  ;; internal procedures 
  (define (real-part z) (car z)) 
  (define (imag-part z) (cdr z)) 
  (define (make-from-real-imag x y) 
    (cons x y)) 
  
  ;; change sqrt, +, square, atan, *, cos, sin to generic procedures 
  (define (magnitude z) 
    (sqrt-generic (add (square-generic (real-part z)) 
                       (square-generic (imag-part z))))) 
  (define (angle z) 
    (atan-generic (imag-part z) (real-part z))) 
  (define (make-from-mag-ang r a) 
    (cons (mul r (cosine a)) (mul r (sine a)))) 
  
  ;; interface to the rest of the system 
  (define (tag x) 
    (attach-tag 'rectangular x)) 
  (put 'real-part '(rectangular) real-part) 
  (put 'imag-part '(rectangular) imag-part) 
  (put 'magnitude '(rectangular) magnitude) 
  (put 'angle '(rectangular) angle) 
  (put 'make-from-real-imag 'rectangular 
       (lambda (x y) 
         (tag (make-from-real-imag x y)))) 
  (put 'make-from-mag-ang 'rectangular 
       (lambda (r a) 
         (tag (make-from-mag-ang r a)))) 
  'done) 
  
(define (install-polar-package) 
  ;; internal procedures 
  (define (magnitude z) (car z)) 
  (define (angle z) (cdr z)) 
  (define (make-from-mag-ang r a) (cons r a)) 
  
  ;; change *, cos, sin, sqrt, +, square, atan to generic procedures 
  (define (real-part z) 
    (mul (magnitude z) (cosine (angle z)))) 
  (define (imag-part z) 
    (mul (magnitude z) (sine (angle z)))) 
  (define (make-from-real-imag x y) 
    (cons (sqrt-generic (add (square-generic x) (square-generic y))) 
          (atan-generic y x))) 
  
  ;; interface to the rest of the system 
  (define (tag x) (attach-tag 'polar x)) 
  (put 'real-part '(polar) real-part) 
  (put 'imag-part '(polar) imag-part) 
  (put 'magnitude '(polar) magnitude) 
  (put 'angle '(polar) angle) 
  (put 'make-from-real-imag 'polar 
       (lambda (x y) 
         (tag (make-from-real-imag x y)))) 
  (put 'make-from-mag-ang 'polar 
       (lambda (r a) 
         (tag (make-from-mag-ang r a)))) 
  'done) 
  
  
(define (real-part z) 
  (apply-generic 'real-part z)) 
(define (imag-part z) 
  (apply-generic 'imag-part z)) 
(define (magnitude z) 
  (apply-generic 'magnitude z)) 
(define (angle z) 
  (apply-generic 'angle z)) 
  
;;; 
;;; APPLY-GENERIC 
;;; From 2.5.2 Combining Data of Different Types -> Coercion 
;;; 
  
(define (apply-generic op . args) 
  (let ((type-tags (map type-tag args))) 
    (let ((proc (get op type-tags))) 
      (if proc 
          (apply proc (map contents args)) 
          (if (= (length args) 2) 
              (let ((type1 (car type-tags)) 
                    (type2 (cadr type-tags)) 
                    (a1 (car args)) 
                    (a2 (cadr args))) 
                (let ((t1->t2 (get-coercion type1 type2)) 
                      (t2->t1 (get-coercion type2 type1))) 
                  (cond (t1->t2 
                         (apply-generic op (t1->t2 a1) a2)) 
                        (t2->t1 
                         (apply-generic op a1 (t2->t1 a2))) 
                        (else (error "No method for these types: 
                                       APPLY-GENERIC" 
                                     (list op type-tags)))))) 
              (error "No method for these types: APPLY-GENERIC" 
                     (list op type-tags))))))) 
  
;;; 
;;; Added 
;;; Coerce rational to scheme-number 
;;; 
  
(define (rational->scheme-number x) 
  (let ((numer (car (contents x))) 
        (denom (cdr (contents x)))) 
    (make-scheme-number (/ (* numer 1.0) denom)))) 
  
(put-coercion 'rational 'scheme-number rational->scheme-number) 
  
;;; 
;;; 2.5.1 Generic Arithmetic Operations 
;;; 
  
(define (add x y) (apply-generic 'add x y)) 
(define (sub x y) (apply-generic 'sub x y)) 
(define (mul x y) (apply-generic 'mul x y)) 
(define (div x y) (apply-generic 'div x y)) 
  
;; Add definitons of generic procedures 
(define (sine x) (apply-generic 'sine x)) 
(define (cosine x) (apply-generic 'cosine x)) 
(define (sqrt-generic x) (apply-generic 'sqrt-generic x)) 
(define (atan-generic y x) (apply-generic 'atan-generic y x)) 
(define (square-generic x) (mul x x)) 
  
(define (install-scheme-number-package) 
  (define (tag x) 
    (attach-tag 'scheme-number x)) 
  (put 'add '(scheme-number scheme-number) 
       (lambda (x y) (tag (+ x y)))) 
  (put 'sub '(scheme-number scheme-number) 
       (lambda (x y) (tag (- x y)))) 
  (put 'mul '(scheme-number scheme-number) 
       (lambda (x y) (tag (* x y)))) 
  (put 'div '(scheme-number scheme-number) 
       (lambda (x y) (tag (/ x y)))) 
  (put 'make 'scheme-number 
       (lambda (x) (tag x))) 
  
  ;; added 
  (put 'sine '(scheme-number) (lambda (x) (tag (sin x)))) 
  (put 'cosine '(scheme-number) (lambda (x) (tag (cos x)))) 
  (put 'sqrt-generic '(scheme-number) (lambda (x) (tag (sqrt x)))) 
  (put 'atan-generic '(scheme-number scheme-number) (lambda (y x) (tag (atan y x)))) 
  
  'done) 
  
(define (make-scheme-number n) 
  ((get 'make 'scheme-number) n)) 
  
(define (install-rational-package) 
  ;; internal procedures 
  (define (numer x) (car x)) 
  (define (denom x) (cdr x)) 
  (define (make-rat n d) 
    (let ((g (gcd n d))) 
      (cons (/ n g) (/ d g)))) 
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
  ;; interface to rest of the system 
  (define (tag x) (attach-tag 'rational x)) 
  (put 'add '(rational rational) 
       (lambda (x y) (tag (add-rat x y)))) 
  (put 'sub '(rational rational) 
       (lambda (x y) (tag (sub-rat x y)))) 
  (put 'mul '(rational rational) 
       (lambda (x y) (tag (mul-rat x y)))) 
  (put 'div '(rational rational) 
       (lambda (x y) (tag (div-rat x y)))) 
  (put 'make 'rational 
       (lambda (n d) (tag (make-rat n d)))) 
  
  ;; added 
  (define (tag-schemenumber x) 
    (attach-tag 'scheme-number x)) 
  (put 'sine '(rational) 
       (lambda (x) 
         (tag-schemenumber (sin (/ (numer x) (denom x)))))) 
  (put 'cosine '(rational) 
       (lambda (x) 
         (tag-schemenumber (cos (/ (numer x) (denom x)))))) 
  (put 'sqrt-generic '(rational) 
       (lambda (x) 
         (tag-schemenumber (sqrt (/ (* 1.0 (numer x)) (denom x)))))) 
  (put 'atan-generic '(rational rational) 
       (lambda (y x) 
         (tag-schemenumber (atan (/ (numer y) (denom y)) 
                                 (/ (numer x) (denom x)))))) 
  
  'done) 
  
(define (make-rational n d) 
  ((get 'make 'rational) n d)) 
  
(define (install-complex-package) 
  ;; imported procedures from rectangular 
  ;; and polar packages 
  (define (make-from-real-imag x y) 
    ((get 'make-from-real-imag 
          'rectangular) 
     x y)) 
  (define (make-from-mag-ang r a) 
    ((get 'make-from-mag-ang 'polar) 
     r a)) 
  ;; internal procedures 
  
  ;; change +, -, *, / to generic procedures 
  (define (add-complex z1 z2) 
    (make-from-real-imag 
     (add (real-part z1) (real-part z2)) 
     (add (imag-part z1) (imag-part z2)))) 
  (define (sub-complex z1 z2) 
    (make-from-real-imag 
     (sub (real-part z1) (real-part z2)) 
     (sub (imag-part z1) (imag-part z2)))) 
  (define (mul-complex z1 z2) 
    (make-from-mag-ang 
     (mul (magnitude z1) (magnitude z2)) 
     (add (angle z1) (angle z2)))) 
  (define (div-complex z1 z2) 
    (make-from-mag-ang 
     (div (magnitude z1) (magnitude z2)) 
     (sub (angle z1) (angle z2)))) 
  
  ;; interface to rest of the system 
  (define (tag z) (attach-tag 'complex z)) 
  (put 'add '(complex complex) 
       (lambda (z1 z2) 
         (tag (add-complex z1 z2)))) 
  (put 'sub '(complex complex) 
       (lambda (z1 z2) 
         (tag (sub-complex z1 z2)))) 
  (put 'mul '(complex complex) 
       (lambda (z1 z2) 
         (tag (mul-complex z1 z2)))) 
  (put 'div '(complex complex) 
       (lambda (z1 z2) 
         (tag (div-complex z1 z2)))) 
  (put 'make-from-real-imag 'complex 
       (lambda (x y) 
         (tag (make-from-real-imag x y)))) 
  (put 'make-from-mag-ang 'complex 
       (lambda (r a) 
         (tag (make-from-mag-ang r a)))) 
  'done) 
  
(define (make-complex-from-real-imag x y) 
  ((get 'make-from-real-imag 'complex) x y)) 
(define (make-complex-from-mag-ang r a) 
  ((get 'make-from-mag-ang 'complex) r a)) 
  
  
;;; 
;;; Test 
;;; 
  
(install-scheme-number-package) 
(install-rational-package) 
(install-rectangular-package) 
(install-polar-package) 
(install-complex-package) 
  
(define x1 (make-scheme-number 1)) 
(define x2 (make-scheme-number 2)) 
  
(define y1 (make-rational 2 3)) 
(define y2 (make-rational 2 5)) 
  
(define z1 (make-complex-from-mag-ang x1 x2)) 
(define z2 (make-complex-from-mag-ang x1 y1)) 
(define z3 (make-complex-from-real-imag y1 y2)) 
  
(add z1 z2) 
(add z1 z3) 
(sub z1 z2) 
(sub z1 z3) 
(mul z1 z2) 
(mul z1 z3) 
(div z1 z2) 
(div z1 z3) 

; 执行结果
'(complex rectangular (scheme-number . 0.36974042422980563) scheme-number . 1.5276672298954188)
'(complex rectangular (scheme-number . 0.2505198301195242) scheme-number . 1.3092974268256818)
'(complex rectangular (scheme-number . -1.2020340973240904) scheme-number . 0.2909276237559447)
'(complex rectangular (scheme-number . -1.082813503213809) scheme-number . 0.5092974268256817)
'(complex polar (scheme-number . 1) scheme-number . 2.6666666666666665)
'(complex polar (scheme-number . 0.77746025264604) scheme-number . 2.540419500270584)
'(complex polar (scheme-number . 1) scheme-number . 1.3333333333333335)
'(complex polar (scheme-number . 1.2862393885688164) scheme-number . 1.459580499729416)
```
