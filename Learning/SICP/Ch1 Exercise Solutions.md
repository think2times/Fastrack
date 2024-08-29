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

## Exercise 1.20
> The process that a procedure generates is of course dependent on the rules used by the interpreter. As an example, consider the iterative gcd procedure given above. Suppose we were to interpret this procedure using normal-order evaluation, as discussed in Section 1.1.5. (The normal-order-evaluation rule for if is described in Exercise 1.5.) Using the substitution method (for normal order), illustrate the process generated in evaluating (gcd 206 40) and indicate the remainder operations that are actually performed. How many remainder operations are actually performed in the normal-order evaluation of (gcd 206 40)? In the applicative-order evaluation?

> answer:
- normal-order: 18 times, 14 when evaluating the condition and 4 in the final reduction phase.
```
(gcd 206 40)
  (if (= 40 0) 206
      (gcd 40 (remainder 206 40)))

(gcd 40 (remainder 206 40))
  (if (= (remainder 206 40) 0) 40          ; (if (= 6 0) 40), remainder + 1
      (gcd (remainder 206 40) (remainder 40 (remainder 206 40))))

(gcd (remainder 206 40) (remainder 40 (remainder 206 40)))
  (if (= (remainder 40 (remainder 206 40)) 0)     ; (if (= 4 0) 6), remainder + 2
      (remainder 206 40)
      (gcd (remainder 40 (remainder 206 40)) (remainder (remainder 206 40) (remainder 40 (remainder 206 40)))))

(gcd (remainder 40 (remainder 206 40)) (remainder (remainder 206 40) (remainder 40 (remainder 206 40))))
 (if (= (remainder (remainder 206 40) (remainder 40 (remainder 206 40))) 0)       ; (if (= 2 0) 4), remainder + 4
     (remainder 40 (remainder 206 40))
     (gcd (remainder (remainder 206 40) (remainder 40 (remainder 206 40))) (remainder (remainder 40 (remainder 206 40)) (remainder (remainder 206 40) (remainder 40 (remainder 206 40))))))

(gcd (remainder (remainder 206 40) (remainder 40 (remainder 206 40))) (remainder (remainder 40 (remainder 206 40)) (remainder (remainder 206 40) (remainder 40 (remainder 206 40)))))
(if (= (remainder (remainder 40 (remainder 206 40)) (remainder (remainder 206 40) (remainder 40 (remainder 206 40)))) 0)     ; (if (= 0 0) 2), remainder + 7
    (remainder (remainder 206 40) (remainder 40 (remainder 206 40)))               ; remainder + 4, 后面的命令并未执行
    (gcd (remainder (remainder 40 (remainder 206 40)) (remainder (remainder 206 40) (remainder 40 (remainder 206 40))))
         (remainder (remainder (remainder 206 40) (remainder 40 (remainder 206 40))) (remainder (remainder 40 (remainder 206 40)) (remainder (remainder 206 40) (remainder 40 (remainder 206 40)))))))
```

- applicative-order: 4 times
```
 (gcd 206 40) 
 (gcd 40 (remainder 206 40))  
 (gcd 40 6)   
 (gcd 6 (remainder 40 6))   
 (gcd 6 4)   
 (gcd 4 (remainder 6 4))   
 (gcd 4 2)   
 (gcd 2 (remainder 4 2))   
 (gcd 2 0)   
 2 
 ```

## Exercise1.21
> Use the smallest-divisor procedure to find the smallest divisor of each of the following numbers: 199, 1999, 19999.

- 199: 199
- 1999: 1999
- 19999: 7

## Exercise 1.22
> Most Lisp implementations include a primitive called runtime that returns an integer that specifies the amount of time the system has been running (measured, for example, in microseconds). The following $timed-prime-test$ procedure, when called with an integer $n$, prints $n$ and checks to see if $n$ is prime. If $n$ is prime, the procedure prints three asterisks followed by the amount of time used in performing the test.

```
(define (timed-prime-test n)
  (newline)
  (display n)
  (start-prime-test n (runtime)))
(define (start-prime-test n start-time)
  (if (prime? n)
      (report-prime (- (runtime) start-time))))
(define (report-prime elapsed-time)
  (display " *** ")
  (display elapsed-time))
```

> Using this procedure, write a procedure $search-for-primes$ that checks the primality of consecutive odd integers in a specified range. Use your procedure to find the three smallest primes larger than 1000; larger than 10,000; larger than 100,000; larger than 1,000,000. Note the time needed to test each prime. Since the testing algorithm has order of growth of $\Theta(\sqrt n)$, you should expect that testing for primes around 10,000 should take about $\sqrt 10$ times as long as testing for primes around 1000. Do your timing data bear this out? How well do the data for 100,000 and 1,000,000 support the $\Theta(\sqrt n)$ prediction? Is your result compatible with the notion that programs on your machine run in time proportional to the number of steps required for the computation?

> answer:
```
(define (search-for-primes n count)
  (cond ((and (< count 3) (prime? n)) (and (timed-prime-test n) (search-for-primes (+ n 1) (+ count 1))))
        ((< count 3) (search-for-primes (+ n 1) count))))

; 由于这里已经判断了是否为质数，所以打印的时候就不用判断了
(define (start-prime-test n start-time)
  (report-prime (- (runtime) start-time)))
```
- 这是修改start-prime-test前的执行时间
![Alt text](<images/exer 1.22-1000.png>)
![Alt text](<images/exer 1.22-10000.png>)
![Alt text](<images/exer 1.22-100000.png>)
![Alt text](<images/exer 1.22-1000000.png>)
> 从1000到10000，执行时间只有2倍左右的差距，但是从10000到100000，从100000到1000000确实差不多是$\sqrt 10$倍的差距。这可能跟我们追踪的时间只是其中部分代码有关，当执行次数较少时，那些“无关”代码的执行时间占比比较大，所以从1000到10000执行时间只有2倍的差距；随着执行次数增多，“无关”代码的执行时间占比越来越少，执行时间的关系就逐渐符合数学分析的结果了。

- 这是修改start-prime-test后的执行时间，可以发现时间急剧降低，但是代价是没法监测$prime?$的执行时间了。。
![Alt text](<images/exer 1.22-new.png>)

## Exercise 1.23
> The smallest-divisor procedure shown at the start of this section does lots of needless testing: After it checks toseeif thenumberisdivisibleby2thereisnopoint in checking to see if it is divisible by any larger even numbers. is suggests that the values used for test-divisor should not be 2, 3, 4, 5, 6, ..., but rather 2, 3, 5, 7, 9, ....
> To implement this change, define a procedure next that returns 3 if its input is equal to 2 and otherwise returns its input plus 2. Modify the smallest-divisor procedure to use (next test-divisor) instead of (+ test-divisor 1). With timed-prime-test incorporating this modified version of smallest-divisor, run the test for each of the 12 primesfoundinExercise1.22. Since this modification halves the number of test steps, you should expect it to run about twice as fast. Is this expectation confirmed? If not, what is the observed ratio of the speeds of the two algorithms, and how do you explain the fact that it is different from 2?

> answer:
```
(define (next n)
  (if (= n 2) 3 (+ n 2)))
```
> 根据上道题目的教训，当n太小时执行时间的差距可能不会跟数学分析相同，这次我特意选了比较大的数字：1000000000000000，但是执行时间的差距也还是达不到2倍的差距，只有差不多1.5倍。原因主要是因为$next$里有有个$if$判断，虽然输入的检测少了一半，但是每次都要额外做一次$if$检查，然后再+2，而原来是直接进行+1操作，所以执行的操作其实并没有减少。执行时间的降低大概是因为$if$所对应的机器步骤比加法要少，所以虽然算法操作没有变，但是机器步骤却变少了，所以执行时间还是降低了。
- 1.22
![Alt text](<images/exer 1.23-old.png>)
- 1.23
![Alt text](<images/exer 1.23-new.png>)

## Exercise1.24
> Modify the $timed-prime-test$ procedure of Exercise 1.22 to use fast-prime? (the Fermat method), and test each of the 12 primes you found in that exercise. Since the Fermat test has $\Theta(\log{n})$ growth, how would you expect the time to test primes near 1,000,000 to compare with the  time needed to test primes near 1000? Do your data bear this out? Can you explain any discrepancy you find?

> 由于$fast-prime?$的时间复杂度是$\Theta(\log{n})$，为了便于计算，取10为底，则$\log_{10}^{1000}=3, \log_{10}^{1000000}=6$，所以执行时间应该有2倍左右的差距，由下图可以看出，实际情况跟数学分析很接近。
![Alt text](<images/exer 1.24.png>)

## Exercise 1.25
> Alyssa P. Hacker complains that we went to a lot of extra work in writing expmod. Aer all, she says, since we already know how to compute exponentials, we could have simply written
```
(define (expmod base exp m)
  (remainder (fast-expt base exp) m))
 ```
Is she correct? Would this procedure serve as well for our fast prime tester? Explain.

> 这个写法是可以实现功能的，但是速度会变慢，用下面的代码来演示一下：
```
; The Fermat Test
; calculate the remainder of base^exp modulo m
(define (expmod base exp m) 
  (cond ((= exp 0) 1) 
        ((even? exp) 
          (remainder 
            (square (expmod base (/ exp 2) m)) ; (1) 
            m)) 
        (else 
          (remainder 
            (* base (expmod base (- exp 1) m)) 
            m))))

; The modified procedures 
(define (modified-expmod base exp m) 
  (remainder (fast-expt base exp) m))

; Helper procedures 
(define (fast-expt b n) 
  (cond ((= n 0) 1) 
        ((even? n) (square (fast-expt b (/ n 2)))) 
        (else (* b (fast-expt b (- n 1)))))) 

; calculate run time of a procedure
(define (report-elapsed-time start-time) 
  (display " *** ") 
  (display (- (runtime) start-time)))


; Test the speed 
(define start-time1 (runtime)) 
(expmod 999999 1000000 1000000) 
(report-elapsed-time start-time1)
(newline)

(define start-time2 (runtime)) 
(modified-expmod 999999 1000000 1000000) 
(report-elapsed-time start-time2)
```
![Alt text](<images/exer 1.25.png>)

## Exercise 1.26
> Louis Reasoner is having great difficulty doing Exercise 1.24. His $fast-prime?$ test seems to run more slowly than his $prime?$ test. Louis calls his friend Eva Lu Ator over to help. When they examine Louis’s code, they f ind that he has rewrien the expmod procedure to use an explicit multiplication, rather than calling $square$:
```
(define (expmod base exp m)
  (cond ((= exp 0) 1)
        ((even? exp)
         (remainder (* (expmod base (/ exp 2) m)
                       (expmod base (/ exp 2) m))
                    m))
        (else
         (remainder (* base
                       (expmod base (- exp 1) m))
                    m))))
 ```
> “I don’t see what difference that could make,” says Louis. 
> “I do.” says Eva. “By writing the procedure like that, you have transformed the $\Theta(\log n)$ process into a $\Theta n$ process.” Explain.

> Instead of a linear recursion, the rewritten $expmod$ generates a tree recursion,whose execution time grows exponentially with the depth of the tree, which is the logarithm of $N$. Therefore, the execution time is linear with $N$.

## Exercise 1.27
> Demonstrate that the Carmichael numbers listed in Footnote 1.47 really do fool the Fermat test. That is, write a procedure that takes an integer $n$ and tests whether $a^n$ is congruent to a modulo $n$ for every $a < n$,and try your procedure on the given Carmichael numbers.

> 修改后的$fast-prime?$如下，$n$表示要检测的数，$a$表示$2\le a \lt n$的任意整数，结果也确实检查不出来那些Carmichael numbers是质数。
```
(define (fast-prime? n a)
  (cond ((= a n) true)
        ((= (expmod a n n) a) (fast-prime? n (+ a 1)))
        (else false)))

(fast-prime? 561 2)      ; 能被3整除
(fast-prime? 1105 2)     ; 能被5整除
(fast-prime? 1729 2)     ; 能被7整除
(fast-prime? 2465 2)     ; 能被5整除
(fast-prime? 2821 2)     ; 能被7整除
(fast-prime? 6601 2)     ; 能被7整除
```
![Alt text](<images/exer 1.27.png>)

## Exercise 1.28
> One variant of the Fermat test that cannot be fooled is called the $Miller-Rabin test$ (Miller 1976; Rabin 1980). This starts from an alternate form of Fermat’s Little Theorem, which states that if $n$ is a prime number and $a$ is any positive integer less than $n$,then $a$ raised to the $(n-1)$-st poweris congruent to 1 modulo $n$. To test the primality of a  number $n$ by the Miller-Rabin test, we pick a random number $a < n$ and raise $a$ to the $(n-1)$-st power modulo $n$ using the $expmod$ procedure. However, whenever we perform the  squaring step in $expmod$, we check to see if we have discovered a “nontrivial square root of 1 modulon,” that is, a number not equal to 1 or $n-1$ whose square is equal to 1 modulo  $n$. It is possible to prove that if such a nontrivial square root of 1 exists, then $n$ is not prime. It is also possible to prove that if $n$ is an odd number that is not prime, then,for at least half the numbers $a < n$, computing an 1 in this way will reveal a nontrivial square root of 1 modulo $n$. (This is why the Miller-Rabin test cannot be fooled.) Modify the expmod procedure to signal if it discovers a nontrivial square root of 1, and use this to implement the Miller-Rabin test with a procedure analogous to $fermat-test$. Check your procedure by testing various known primes and non-primes. Hint: One convenient way to make $expmod$ signal is to have it return 0.

> answer:
```
; calculate the remainder of base^exp modulo m
(define (expmod base exp m)
  (cond ((= exp 0) 1)
        ((even? exp)
         (remainder
          (sqmod (expmod base (/ exp 2) m) m)
          m))
        (else
         (remainder
          (* base (expmod base (- exp 1) m))
          m))))

; Return 0 if `x^2 mod m` is equal to `1 mod m` and x != m - 1 and x != 1;
; x^2 otherwise."
(define (sqmod x m)  
  (cond ((and (= (remainder (square x) m) 1)    ; 1 mod m = 1 
              (not (= x (- m 1))) 
              (not (= x 1)))
         0)
        (else (square x))))

; Miller-Rabin test
; if n is a prime number and a is any positive integer less than n, then a raised to the (n-1)-st power is congruent to 1 modulo n.
; we pick a random number a < n and raise a to the (n 1)-st power modulo n to test if it is congruent to 1 modulon.
(define (miller-rabin-test n)
  (define (try-it a)
    (define (check-it x)
      (and (not (= x 0)) (= x 1)))
    (check-it (expmod a (- n 1) n)))         ; 检查a^(n-1)是否为n的倍数，且a^(n-1)÷n余数为1
  (try-it (+ 1 (random (- n 1)))))           ; random returns a nonnegative integer less than its integer input(from 1 to n).

; runs the test a given number of times, as specified by a parameter
(define (fast-prime? n times)
  (cond ((< n 2) false)            ; 2是最小的质数，所以小于2的数都不是质数
        ((= times 0) true)
        ((miller-rabin-test n) (fast-prime? n (- times 1)))
        (else false)))

(define (prime? n)
  (fast-prime? n 100))

(prime? 2)
(prime? 3)
(prime? 5)
(prime? 7)
(prime? 0)
(prime? 1)
(prime? 4)
(prime? 6)
(prime? 8)
(prime? 9)
(prime? 561)      ; 能被3整除
(prime? 1105)     ; 能被5整除
(prime? 1729)     ; 能被7整除
(prime? 2465)     ; 能被5整除
(prime? 2821)     ; 能被7整除
(prime? 6601)     ; 能被7整除
```

![Alt text](<images/exer 1.28.png>)

## Exercise 1.29
> Simpson’s Rule is a more accurate methodof numerical integration than the method illustrated above. Using Simpson’s Rule, the integral of a function $f$ between $a$ and $b$ is approximated as 
$\frac{h}{3}(y_0+4y_1+2y_2+4y_3+2y_4+...+2y_{n-2}+4y_{n-1}+y_n)$, 
where $h = \frac{b − a}n$, for some even integer $n$, and $y_k = f(a + kh)$. (Increasing $n$ increases the accuracy of the approximation.) Define a procedure that takes as arguments $f, a, b$, and $n$ and returns the value of the integral, computed using Simpson’s Rule. Use your procedure to integrate cube between 0 and 1 (with $n = 100$ and $n = 1000$), and compare the results to those of the integral procedure shown above.

```
; template of "summation according to Simpson’s Rule".
(define (simpson-sum term a next b n)
  ; 由于n取得是偶数，所以得到的factor会是2, 4, 2, 4, ... , 1
  ; 与Simpson’s Rule相比，第一项加了2遍，最后需要把第一项减掉一次
  (define factor (cond ((= n 0) 1)
                       ((even? n) 2)
                       (else 4)))
  (if (> a b)
      0
      (+ (* factor (term a))
         (simpson-sum term (next a) next b (- n 1)))))


(define (integral f a b n)
  (define h (/ (- b a) n))
  (define (integral-next x)
    (+ x h))
  (* (/ h 3.0)
     ; 把第一项减掉一次
     (- (simpson-sum f a integral-next b n) (f a))))


(integral cube 0 1 100)
(integral cube 0 1 1000)

; 输出
0.25
0.25
```

## Exercise 1.30
> The sum procedure above generates a linear recursion. The procedure can be rewrien so that the sum is performed iteratively. Show how to do this by filling in the missing expressions in the following definition:
```
(define (sum term a next b)
  (define (iter a result)
    (if ⟨??⟩
        ⟨??⟩
        (iter ⟨??⟩ ⟨??⟩)))
  (iter ⟨??⟩ ⟨??⟩))
```

> answer :
```
(define (sum term a next b)
  (define (iter a result)
    (if (> a b)
        result
        (iter (next a) (+ (term a) result))))
  (iter a 0))
```

## Exercise 1.31
- a. The sum procedure is only the simplest of a vast number of similar abstractions that can be captured as higher order procedures.51 Write an analogous procedure called product that returns the product of the values of a function at points over a given range. Show how to define factorial in terms of product. Also use product to compute approximations to π using the formula
$\frac{\pi}4=\frac{2\cdot4\cdot4\cdot6\cdot6\cdot8...}{3\cdot3\cdot5\cdot5\cdot7\cdot7...}$
- b. If your product procedure generates a recursive process, write one that generates an iterative process. If it generates an iterative process, write one that generates a recursive process.

> answer :
- a
```
(define (product-iter term a next b)
  (define (iter a result)
    (if (> a b)
        result
        (iter (next a) (* (term a) result))))
  (iter a 1))

(define (factorial n)
  (define (identity x) x)
  (product-iter identity 1 inc n))

(factorial 0)
(factorial 1)
(factorial 2)
(factorial 3)

> result
1
1
2
6
```

- b
```
(define (product-recur term a next b)
  (if (> a b)
      1
      (* (term a)
         (product-recur term (next a) next b))))

(define (factorial n)
  (define (identity x) x)
  (product-recur identity 1 inc n))

(factorial 0)
(factorial 1)
(factorial 2)
(factorial 3)

> result
1
1
2
6
```

## Exercise 1.32
> a. Show that sum and product (Exercise 1.31) are both special cases of a still more general notion called $accumulate$ that combines a collection of terms, using some general accumulation function:
`(accumulate combiner null-value term a next b)`
> $accumulate$ takes as arguments the same term and range specifications as $sum$ and $product$,together with a $combiner$ procedure (of two arguments) that specifies how the current term is to be combined with the accumulation of the preceding terms and a $null-value$ that specifies what base value to use when the terms run out. Write $accumulate$ and show how $sum$ and $product$ can both be defined as simple calls to $accumulate$.

>  b. If your $accumulate$ procedure generates a recursive process, write one that generates an iterative process. If it generates an iterative process, write one that generates a recursive process.

> answer :
- a
```
; use recursive
(define (accumulate-recur combiner null-value term a next b)
  (if (> a b)
      null-value
      (combiner (term a)
                (accumulate-recur combiner null-value term (next a) next b))))

; computes the summation of two numbers
(define (sum a b)
  (accumulate-recur + 0 identity a inc b))

; computers the production of two numbers
(define (product a b)
  (accumulate-recur * 1 identity a inc b))

(sum 3 5)
(product 3 5)
```

- b
```
; use iter
(define (accumulate-iter combiner null-value term a next b)
  (define (iter a result)
    (if (> a b)
        result
        (iter (next a) (combiner (term a) result))))
  (iter a null-value))

; computes the summation of two numbers
(define (sum a b)
  (accumulate-iter + 0 identity a inc b))

; computers the production of two numbers
(define (product a b)
  (accumulate-iter * 1 identity a inc b))

(sum 3 5)
(product 3 5)
```

## Exercise 1.33
> You can obtain an even more general version of $accumulate$ (Exercise 1.32) by introducing the notion of a $filter$ on the terms to be combined. That is,combine only those terms derived from values in the range that satisfy a specified condition. The resulting $filtered-accumulate$ abstraction takes the same arguments as accumulate, together with an additional predicate of one argument that specifies the filter. Write $filtered-accumulate$ as a procedure. Show how to express the following using $filtered-accumulate$:
- a. the sum of the squares of the prime numbers in the interval $a$ to $b$ (assuming that you have a $prime?$ predicate already written)
- b. the product of all the positive integers less thann that are relatively prime to $n$ (i.e., all positive integers $i < n$ such that $GCD(i, n) = 1$).

> answer :
```
; recursive implementation
(define (filtered-accumulate-recur combiner null-value term a next b filter)
  (if (> a b)
      null-value
      (if (filter a)
          (combiner (term a) (filtered-accumulate-recur combiner null-value term (next a) next b filter))
          (combiner null-value (filtered-accumulate-recur combiner null-value term (next a) next b filter)))))

; for a
; computes the summation of the squares of the prime numbers in the interval a to b
(define (sum-prime-square a b)
  (filtered-accumulate-recur + 0 square a inc b prime?))

; for b
; computers the production of all the positive integers less thann that are relatively prime to n
(define (product-prime n)
  (filtered-accumulate-recur * 1 identity 1 inc n prime?))

(sum-prime-square 0 10)
(product-prime 10)
> result
87
210


; iterative implementation
(define (filtered-accumulate-iter combiner null-value term a next b filter)
  (define (iter a result)
    (if (> a b)
        result
        (if (filter a)
            (iter (next a) (combiner (term a) result))
            (iter (next a) result))))
  (iter a null-value))

; for a
; computes the summation of the squares of the prime numbers in the interval a to b
(define (sum-prime-square a b)
  (filtered-accumulate-iter + 0 square a inc b prime?))

; for b
; computers the production of all the positive integers less thann that are relatively prime to n
(define (product-prime n)
  (filtered-accumulate-iter * 1 identity 1 inc n prime?))

(sum-prime-square 0 10)
(product-prime 10)
> result
87
210
```

## Exercise 1.34
> Suppose we define the procedure
`(define (f g) (g 2))`
> Then we have
```
(f square)
4
(f (lambda (z) (* z (+ z 1))))
6
```
> What happens if we(perversely) ask the interpreter to evaluate the combination $(f f)$? Explain.

> answer: 执行之后报错了，因为$f$需要一个程序来作为参数，而我们传了个数字2给它
![Alt text](<images/exer 1.34.png>)

## Exercise 1.35
> Show that the golden ratio $ϕ$ (Section 1.2.2) is a fixed point of the transformation $x = 1 + \frac{1}{x}$, and use this fact to compute $ϕ$ by means of the fixed-point procedure.

> answer: 证明$x = 1 + \frac{1}{x}$的解是黄金分割比例就是简单的一元二次方程求解，这里就不说明了，利用$fixed-point$程序求解也很简单，直接把书上1.3.3部分的程序拿来用就行
```
(define tolerance 0.001)

(define (close-enough? x y tolerance)
  (< (abs (- x y)) tolerance))

(define (fixed-point f first-guess)
  (define (close-enough? v1 v2 tolerance)
    (< (abs (- v1 v2))
       tolerance))
  (define (try guess)
    (let ((next (f guess)))
      (if (close-enough? guess next tolerance)
          next
          (try next))))
  (try first-guess))

; calculate the golden ratio φ by solve the equation: x = 1 + 1/x
(fixed-point (lambda (x) (+ 1 (/ 1 x)))
             1.0)

; result: 1.6181818181818182
```

## Exercise 1.36
> Modify fixed-point so that it prints the sequenceofapproximationsitgenerates using the $newline$ and $display$ primitives shown in Exercise 1.22. Then find a solution to $x^x = 1000$ by finding a fixed point of $x = log(1000)/log(x)$. (Use Scheme’s primitive log procedure, which computes natural logarithms.) Compare the number of steps this takes with and without average damping.(Note that you cannot start fixed-point with a guess of 1, as this would cause division by $log(1) = 0.)$

> 这道题目难度不大，计算部分直接修改书上 1.3.3 的公式就行，然后把每次的猜测值打印出来就行。
```
(define (fixed-point f first-guess)
  (define (close-enough? v1 v2 tolerance)
    (< (abs (- v1 v2))
       tolerance))
  (define (try guess count)
    (let ((next (f guess)))
      (display count)
      (display " *** ")
      (display guess)
      (newline)
      (if (close-enough? guess next tolerance)
          (and (display (+ count 1))
               (display " *** ")
               (display next))
          (try next (+ count 1)))))
  (try first-guess 1))


; with average damping
(newline)
(display "with average damping")
(newline)
(fixed-point (lambda (x) (average x (/ (log 1000) (log x))))
             1.1)
(newline)

; without average damping
(newline)
(display "without average damping")
(newline)
(fixed-point (lambda (x) (/ (log 1000) (log x)))
             1.1)
```
> 由下图可以看出，使用 average damping 只需要11次就可以找到符合要求的答案，而不用则要27次，使不使用 average damping 的差距还是挺大的。
![Alt text](<images/exer 1.36.png>)
