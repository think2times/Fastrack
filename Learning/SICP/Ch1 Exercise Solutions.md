[Building Abstractions with Procedures]()

# 1. The Elements of Programming

## Exercise 1.1
> Below is a sequence of expressions. What is the result printed by the interpreter in response to each expression? Assume that the sequence is to be evaluated in
the order in which it is presented. 

![Alt text](<images/exer 1.1.png>)

## Exercise 1.2
> Translate the following expression into prefix form: $\frac{5+4+(2-(3-(6+\frac45)))}{3(6-2)(2-7)}$.
```
(/ (+ 5
      (+ 4
         (- 2
            (- 3
               (+ 6
                  (/ 4 5))))))
    (* 3
       (- 6 2)
       (- 2 7)))
```
![Alt text](<images/exer 1.2.png>)

## Exercise 1.3
> Define a procedure that takes three numbers as arguments and returns the sum of the squares of the two larger numbers.
```
(define (smaller-of-two-numbers x y)
  (if (< x y) x y))

(define (sum-of-two-larger-numbers-of-three x y z)
  (- (+ x y z)
     (smaller-of-two-numbers (smaller-of-two-numbers x y) z)))
```
![Alt text](<images/exer 1.3.png>)

## Exercise 1.4
> Observe that our model of evaluation allows for combinations whose operators are compound expressions. Use this observation to describe the behavior of the following procedure:
```
(define (a-plus-abs-b a b)
  ((if (> b 0) + -) a b))
```
> 首先定义了一个名为 a-plus-abs-b 的函数，它接受2个参数；然后判断b的正负，如果b为正，则计算$a+b$，如果b不为正，则计算$a-b$，也就实现了$a+|b|$的效果。

## Exercise 1.5
> Ben Bitdiddle has invented a test to determine whether the interpreter he is faced with is using applicative order evaluation or normal-order evaluation.He defines the following two procedures:
```
(define (p) (p))
(define (test x y)
  (if (= x 0) 0 y))
```
> Then he evaluates the expression `(test 0 (p))`.
> What behavior will Ben observe with an interpreter that uses applicative-order evaluation? What behavior will he observe with an interpreter that uses normal-order evaluation? Explain your answer. (Assume that the evaluation rule for the special form if is the same whether the interpreter is using normal or applicative order: The predicate expression is evaluated first, and the result determines whether to evaluate the consequent or the alternative expression.)

> applicative-order: 一直执行`(test 0 (p))`
> normal-order: 
```
(test 0 (p))
(if (= 0 0) 0 (p))
(if #t 0 (p))
0
```

## Exercise 1.6 
> Alyssa P. Hacker doesn’t see why if needs to be provided as a special form. “Why can’t I just define it as an ordinary procedure in terms of cond?” she asks. Alyssa’s friend Eva Lu Ator claims this can indeed be done, and she defines a new version of if:
```
(define (new-if predicate then-clause else-clause)
(cond (predicate then-clause)
(else else-clause)))
```
> Eva demonstrates the program for Alyssa:
```
(new-if (= 2 3) 0 5)
5
(new-if (= 1 1) 0 5)
0
```
> Delighted, Alyssa uses new-if to rewrite the square-root program:
```
(define (sqrt-iter guess x)
(new-if (good-enough? guess x)
guess
(sqrt-iter (improve guess x) x)))
```
> What happens when Alyssa aempts to use this to compute square roots? Explain.

> The default if statement is a special form which means that even when an interpreter follows applicative substitution, it only evaluates one of its parameters- not both. However, the newly created new-if doesn't have this property and hence, it never stops calling itself due to the third parameter passed to it in sqrt-iter.
> Let's see the difference between if and new-if:
```
; if
(if #t (display "good") (display "bad"))
good
; Unspecified return value
```
```
; new-if
(new-if #t (display "good") (display "bad"))
goodbad
; Unspecified return value
```
> As we can see, both was executed regardless result of the predicate when we use new-if.

## Exercise 1.7:
> The good-enough? test used in computing square roots will not be very effective for finding the square roots of very small numbers. Also, in real computers, arithmetic operations are almost always performed with limited precision. This makes our test inadequate for very large numbers. Explain these statements, with examples showing how the test fails for small and large numbers. An alternative strategy for implementing good-enough? is to watch how guess changes from one iteration to the next and to stop when the change is a very small fraction of the guess. Design a square-root procedure that uses this kind of end test. Does this work beer for small and large numbers?

> 对于比较小的数，计算结果会不准确，因为设定的差值可能比所求数还要大；对于比较大的数，程序会一直运行，因为猜测值跟所求数的绝对差值会一直大于设定的差值。
> 按题目提示重新设计$good-enough?$函数可以解决这个问题
```
(define epsilon (expt 2 -52))
(define tolerance (* (/ 9 4) epsilon))
(define (good-enough? guess)
  (or (= guess 0) (< (abs (- (improve guess) guess)) (* tolerance guess))))
```

##  Exercise 1.8:
> Newton’s method for cube roots is based on the fact that if y is an approximation to the cube root of x, then a beer approximation is given by the value $\frac{\frac{x}{y^2}+2y}3$.
> Use this formula to implement a cube-root procedure analogous to the square-root procedure.(In Section 1.3.4 we will see how to implement Newton’s method in general as an abstraction of these square-root and cube-root procedures.)

> 这个题目很简单，只要把计算平方根的算法里的$improve$函数修改一下就行
```
(define (improve guess)
  (/ (+ (* 2 guess) (/ x (square guess))) 3))
```

## Exercise 1.9
> Each of the following two procedures defines a method for adding two positive integers in terms of the procedures inc, which increments its argument by 1, and dec, which decrements its argument by 1.
```
(define (+ a b)
(if (= a 0) b (inc (+ (dec a) b))))
(define (+ a b)
(if (= a 0) b (+ (dec a) (inc b))))
```
> Using the substitution model, illustrate the process generated by each procedure in evaluating (+ 4 5). Are these processes iterative or recursive?

> The process generated by the first procedure is recursive:
```
(+ 4 5) 
(inc (+ (dec 4) 5)) 
(inc (+ 3 5)) 
(inc (inc (+ (dec 3) 5))) 
(inc (inc (+ 2 5))) 
(inc (inc (inc (+ (dec 2) 5)))) 
(inc (inc (inc (+ 1 5)))) 
(inc (inc (inc (inc (+ (dec 1) 5))))) 
(inc (inc (inc (inc (+ 0 5))))) 
(inc (inc (inc (inc 5)))) 
(inc (inc (inc 6))) 
(inc (inc 7)) 
(inc 8)  
(9)
```
> The process generated by the second procedure is iterative:
```
(+ 4 5) 
(+ (dec 4) (inc 5)) 
(+ 3 6) 
(+ (dec 3) (inc 6)) 
(+ 2 7) 
(+ (dec 2) (inc 7)) 
(+ 1 8) 
(+ (dec 1) (inc 8)) 
(+ 0 9) 
(9)
```
> The easiest way to spot that the first process is recursive (without writing out the substitution) is to note that the "+" procedure calls itself at the end while nested in another expression; the second calls itself, but as the top expression.

## Exercise 1.10
> The following procedure computes a mathematical function called Ackermann’s function.
```
(define (A x y)
(cond ((= y 0) 0)
((= x 0) (* 2 y))
((= y 1) 2)
(else (A (- x 1) (A x (- y 1))))))
```
> What are the values of the following expressions?
```
(A 1 10)
(A 2 4)
(A 3 3)
```
> Consider the following procedures, where A is the procedure defined above:
```
(define (f n) (A 0 n))
(define (g n) (A 1 n))
(define (h n) (A 2 n))
(define (k n) (* 5 n n))
 ```
> Giveconcisemathematicaldefinitionsforthefunctionscomputed by the procedures f, g, and h for positive integer values of n. For example, $(k n)$ computes $5n^2$.

- `(A 1 10)`
```
(A 0 (A 1 9))
(A 0 (A 0 (A 1 8)))
(A 0 (A 0 (A 0 (A 1 7))))
(A 0 (A 0 (A 0 (A 0 (A 1 6)))))
(A 0 (A 0 (A 0 (A 0 (A 0 (A 1 5))))))
(A 0 (A 0 (A 0 (A 0 (A 0 (A 0 (A 1 4)))))))
(A 0 (A 0 (A 0 (A 0 (A 0 (A 0 (A 0 (A 1 3))))))))
(A 0 (A 0 (A 0 (A 0 (A 0 (A 0 (A 0 (A 0 (A 1 2)))))))))
(A 0 (A 0 (A 0 (A 0 (A 0 (A 0 (A 0 (A 0 (A 0 (A 1 1))))))))))
(A 0 (A 0 (A 0 (A 0 (A 0 (A 0 (A 0 (A 0 (A 0 2)))))))))
(A 0 (A 0 (A 0 (A 0 (A 0 (A 0 (A 0 (A 0 4))))))))
(A 0 (A 0 (A 0 (A 0 (A 0 (A 0 (A 0 8)))))))
(A 0 (A 0 (A 0 (A 0 (A 0 (A 0 16))))))
(A 0 (A 0 (A 0 (A 0 (A 0 32)))))
(A 0 (A 0 (A 0 (A 0 64))))
(A 0 (A 0 (A 0 128)))
(A 0 (A 0 256))
(A 0 512)
(1024)
```
- `(A 2 4)`
```
(A 1 (A 2 3))
(A 1 (A 1 (A 2 2)))
(A 1 (A 1 (A 1 (A 2 1))))
(A 1 (A 1 (A 1 2)))
(A 1 (A 1 (A 0 (A 1 1))))
(A 1 (A 1 (A 0 2)))
(A 1 (A 1 4))
; 根据上一问可知，(A 1 n)=2^n
(A 1 16)
(2^16)
```
- `(A 3 3)`
```
(A 2 (A 3 2))
(A 2 (A 2 (A 3 1)))
(A 2 (A 2 2))
(A 2 (A 2 2))
; 根据上一问可知，(A 2 2)=4
(A 2 4)
(2^16)
```
- `(f n)`: $2n$
- `(g n)`: $0~ for~ n=0, 2^n~ for~ n>0$
- `(h n)`: $0~ for~ n=0, 2~ for~ n=1, 2^{2^{2^{2^...n times}}} for~ n > 1$

## Exercise 1.11
> A function f is defined by the rule that
![Alt text](<images/exer 1.11.png>)
> Write a procedure that computes f by means of a recursive process. Write a procedure that computes f by means of an iterative process.

- Recursive
```
(define (f-recur n)
  (if (< n 3)
      n
      (+ (f-recur (- n 1))
         (* 2 (f-recur (- n 2)))
         (* 3 (f-recur (- n 3))))))
```
- Iterative
```
(define (f-iter n)
  ; a相当于f(n-1), b相当于f(n-2), c相当于f(n-3), n相当于计数器
  ; 虽然题目给的公式是倒着算，但是实现的算法是正着算，依次把f(3), f(4)...算出来
  ; 当作为计数器的n恰好等于3时，a此时正好为f(n-1)，所以需要再算一次才能得到f(n)
  (define (iter a b c n)
    (if (< n 3)
        a
        (iter (+ a
                 (* 2 b)
                 (* 3 c))
              a
              b
              (- n 1))))

  (iter 2 1 0 n))
```

## Exercise 1.12
> The following paern of numbers is called Pascal’s triangle.
![Alt text](<images/exer 1.12.png>)
> The numbers at the edge of the triangle are all 1, and each number inside the triangle is the sum of the two numbers above it. Write a procedure that computes elements of Pascal’s triangle by means of a recursive process.

```
(define (pascal row col)
  (cond ((or (< row 1) (< col 1) (< row col)) 0)     ; 排除非法参数
        ((or (= col 1) (= row col)) 1)               ; 当该位置在两边时,值都为1
        (else (+ (pascal (- row 1) (- col 1))        ; 其他位置的数都等于上一行“肩膀”2数之和
                 (pascal (- row 1) col)))))
```

## Exercise 1.13
> Prove that $Fib(n)$ is the closest integer to $\frac{ϕ^n}{\sqrt5}$, where $ϕ = \frac{1 + \sqrt5}{2}$. Hint: Let $\psi=\frac{1 - \sqrt5}{2}$. Use induction and the definition of the Fibonacci numbers (see Section 1.2.2) to prove that $Fib(n)=\frac{ϕ^n-\psi^n}{\sqrt5}$.

> Proof: 
![Alt text](<images/exer 1.13.png>)

## Exercise 1.14
> Draw the tree illustrating the process generated by the count-change procedure of Section 1.2.2 in making change for 11 cents. What are the orders of growth of the space and number of steps used by this process as the amount to be changed increases?

![Alt text](<images/exer 1.14.png>)

> changing an amount $a$ using $n$ kinds of coins:  
> The space required by the process is the height of the tree: $R(a, n) = \theta(a)$  
> The number of steps required by the process: $R(a,n) = \theta (a^n)$,  
> a detailed explanation for this: https://sicp-solutions.net/post/sicp-solution-exercise-1-14/  
> Implement the solution in only $n^2$ is here: https://github.com/sarabander/p2pu-sicp/blob/master/1.2/Ex1.14.scm

## Exercise 1.15
> The sine of an angle (specified in radians)can be computed by making use of the approximation $\sin x \approx x$ if $x$ is sufficiently small, and the trigonometric identity
> $\sin x = 3\sin\frac{x}{3}-4\sin^3\frac{x}{3}$
> to reduce the size of the argument of sin. (For purposes of this exercise an angle is considered “sufficiently small” if its magnitude is not greater than 0.1 radians.) These ideas are incorporated in the following procedures:
```
(define (cube x) (* x x x))
(define (p x) (- (* 3 x) (* 4 (cube x))))
(define (sine angle)
  (if (not (> (abs angle) 0.1))
    angle
    (p (sine (/ angle 3.0)))))
 ```
> - a. How many times is the procedure $p$ applied when (sine 12.15) is evaluated?
> - b. What is the order of growth in space and number of steps (as a function of $a$)used by the process generated by the sine procedure when (sine a) is evaluated?

> answer for a: 5
![Alt text](<images/exer 1.15-sine 12.15.png>)

> answer for b: The angle $a$ is divided by 3 each time the procedure $p$ is applied. Expressing this differently, we can say that $p$ is applied once for each complete power of 3 contained within the angle $a$. Therefore, given a positive argument, let the number of times $p$ is applied as $t$, then $a * \frac{1}{3}^t < 0.1$. We can calculate that $t$ is the ceiling of the base 3 logarithm of the argument $a$ divided by 0.1, or $\lceil \log{3}^{\frac{a}{0.1}} \rceil$. 
> If we measure the required space and the number of steps by counting the invocations of $p$, the order of growth of the process generated by (sine $a$) is logarithmic. Exactly, the number of steps required are $\lceil \log{3}^{\frac{a}{0.1}} \rceil$. In other words we have $O\log{a}$ order of growth.

> Let's check it, if we increase $a$ to 3 times, we'll find the number of executions of $p$ will be increased by one.
- sine 10, 5 times

![Alt text](<images/exer 1.15-sine 10.png>)

- sine 30, 6 times

![Alt text](<images/exer 1.15-sine 30.png>)

- sine 90, 7 times

![Alt text](<images/exer 1.15-sine 90.png>)

## Exercise 1.16
> Design a procedure that evolves an iterative exponentiation process that uses successive squaring and uses a logarithmic number of steps, as does fast-expt.
(Hint: Using the observation that $(b^{\frac{n}2})^2=(b^2)^{\frac{n}2}$, keep,along with the exponent $n$ and the base $b$, an additionalstate variable $a$, and define the state transformation in such a way that the product $ab^n$ is unchanged from state to state. At the beginning of the process a is taken to be 1, and the answer is given by the value of $a$ at the end of the process. In general, the technique of defining an invariant quantity that remains unchanged from state to state is a powerful way to think about the design of iterative algorithms.)

```
(define (expt-iter-by-square b n)
  (define (iter b n a)
    (cond ((= n 0) a)
          ((even? n) (iter (square b)
                           (/ n 2)
                           a))
          (else (iter b
                      (- n 1)
                      (* a b)))))
  (iter b n 1))
```

## Exercise 1.17
> The exponentiation algorithms in this section are based on performing exponentiation by means of repeated multiplication. In a similar way, one can perform integer multiplication by means of repeated addition. The following multiplication procedure (in which it is assumed that our language can only add, not multiply) is analogous to the expt procedure:
```
(define (* a b)
  (if (= b 0)
      0
      (+ a (* a (- b 1)))))
```
> This algorithm takes a number of steps that is linear in b. Now suppose we include, together with addition, operations double, which doubles an integer, and halve, which divides an (even) integer by 2. Using these, design a multiplication procedure analogous to fast-expt that uses a logarithmic number of steps.

```
(define (multiply-recur a b)
  (cond ((= b 0) 0)
        ((even? b) (multiply-recur (double a) (halve b)))
        (else (+ a (multiply-recur a (- b 1))))))
```

## Exercise 1.18
> Using the results of Exercise 1.16 and Exercise 1.17, devise a procedure that generates an iterative process for multiplying two integers in terms of adding, doubling, and halving and uses a logarithmic number of steps.

```
(define (multiply-iter a b)
  (define (iter a b answer)
    (cond ((= b 0) answer)
          ((even? b) (iter (double a) (halve b) answer))
          (else (iter a (- b 1) (+ answer a)))))
  (iter a b 0))
```

## Exercise 1.19
> There is a clever algorithm for computing the Fibonacci numbers in a logarithmic number of steps. Recall the transformation of the state variables $a$ and $b$ in the fib-iter process of Section 1.2.2: $a ← a + b$ and $b ← a$. Call this transformation $T$, and observe that applying $T$ over and over again $n$ times, starting with 1 and 0, produces the pair $Fib(n + 1)$ and $Fib(n)$. In other words, the Fibonacci numbers are produced by applying $T^n$, the $n^{th}$ power of the transformationT , starting with the pair (1, 0). Now consider $T$ to be the special case of $p = 0$ and $q = 1$ in a family of transformations $T_{pq}$ , where $T_{pq}$ transforms the pair $(a, b)$ according to $a ← bq + aq + ap$ and $b ← bp + aq$. Show that if we apply such a transformation $T_{pq}$ twice, the effect is the same as using a single transformation $T_{p'q'}$ of the same form, and compute $p′$ and $q′$ in terms of $p$ and $q$. This gives us an explicit way to square these transformations, and thus we can compute $T^n$ using successive squaring, as in the fast-expt procedure. Put this all together to complete the following procedure, which runs in a logarithmic number of steps:

```
(define (fib n)
  (fib-iter 1 0 0 1 n))
(define (fib-iter a b p q count)
  (cond ((= count 0) b)
        ((even? count)
         (fib-iter a
                   b
                    ; compute p′
                    ; compute q′
                   (/ count 2)))
        (else (fib-iter (+ (* b q) (* a q) (* a p))
                        (+ (* b p) (* a q))
                        p
                        q
                        (- count 1)))))
```

> answer: 
```
(define (fib n)
  (fib-iter 1 0 0 1 n))
(define (fib-iter a b p q count)
  (cond ((= count 0) b)
        ((even? count)
         ; count为偶数且不为0时，可以连续进行两次转换
         ; 通过简单的代数计算和化简，可以得到经过两次转换后
         ; a = b(q^2+2pq) + a(q^2+2pq) + a(p^2+q^2)
         ; b = b(p^2+q^2) + a(q^2+2pq)
         ; 所以 q' = (q^2+2pq), p' = (p^2+q^2)
         (fib-iter a
                   b
                   (+ (square p) (square q))
                   (+ (square q) (* 2 p q))
                   (/ count 2)))
         (else (fib-iter (+ (* b q) (* a q) (* a p))
                         (+ (* b p) (* a q))
                         p
                         q
                         (- count 1)))))
```
