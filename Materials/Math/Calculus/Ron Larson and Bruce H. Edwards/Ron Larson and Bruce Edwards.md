# Preparation
## Algebra
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/P-Algebra%20Formulas.png)
## Geometry
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/P-Geometry%20Formulas.png)
## Trigonometric Functions
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/P-TRIGONOMETRY.png)
### Graphs of Trigonometric Functions
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/P-Graphs%20of%20Trigonometric%20Functions.png)
# 2. Differentiation
## Basic Differentiation Rules
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/2-Basic%20Differentiation%20Rules.png)
## 2.4 The Chain Rule
### 2.4.126 Let $k$ be a fixed positive integer. The $n'th$ derivative of $\frac{1}{x^k-1}$ has the form $\frac{P_n(x)}{(x^k-1)^{n+1}}$ where $P_n(x)$ is a polynomial. Find $P_n(1)$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/2-4-126.png)


# 3. Application of Differentiation
## 3.1 Extrema on an Interval
### 3.1.71 Determine all real numbers $a>0$ for which there exists a nonnegative continuous function $f(x)$ defined on $[0, a]$ with the property that the region $R=\{(x, y), 0 \leq x \leq a, 0 \leq y \leq f(x)\}$ has perimeter $k$ units and area $k$ square units for some real number $k$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/3-1-71.png)

## 3.2 Rolle's Theorem and the Mean Value Theorem
### 3.2.79 $Proof$ Let $p(x) = Ax2 + Bx + C$. Prove that for any interval $[a, b]$, the value $c$ guaranteed by the Mean Value Theorem is the midpoint of the interval.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/3-2-79.png)
### 3.2.85 Let $0<a<b$, Use the Mean Value Theorem to show that $\sqrt{b}-\sqrt{a} \lt \frac{b-a}{2\sqrt{a}}$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/3-2-85.png)

## 3.3 Increasing and Decreasing Functions and the First Derivative Test
### 3.3.101 Find the minimum value of $\lvert sin x+cos x+tan x+cot x+sec x+csc x \rvert$ for real numbers $x$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/3-3-101.png)

## 3.6 A Summary of Curve Sketching
### 3.6.94 Let $f(x)$ be defined for $a \leq x \leq b$. Assuming appropriate properties of continuity and derivability, prove for $a < x < b$ that $\frac{\frac{f(x)-f(a)}{x-a}-\frac{f(b)-f(a)}{b-a}}{x-b} = \frac 1 2 f''(\epsilon)$ where $\epsilon$ is some number between $a$ and $b$.
> **Proof** &emsp; Let $\lambda = \frac{\frac{f(x)-f(a)}{x-a}-\frac{f(b)-f(a)}{b-a}}{x-b}, a<x<b$ (Regard $x$ as a constant)  
> $\lambda(x-b) = \frac{f(x)-f(a)}{x-a}-\frac{f(b)-f(a)}{b-a}$  
> $\lambda(x-b)(x-a) = f(x)-f(a)-\frac{f(b)-f(a)}{b-a}(x-a)$  
> $f(x) = f(a)+\frac{f(b)-f(a)}{b-a}(x-a)+\lambda(x-b)(x-a)$  
> Let $g(t) = f(t) - [f(a)+\frac{f(b)-f(a)}{b-a}(t-a)+\lambda(t-b)(t-a)]$  
> Obviously $g(a)=g(b)=g(x)=0$  
> By Rolle's Theorem, there exists numbers $c_1$ and $c_2$, such that $a<c_1<x<c_2<b$ and $g'(c_1) = g'(c_2) = 0$  
> By Rolle's Theorem, there exists number $\epsilon \in (c_1, c_2) \subset (a, b)$, such that $g''(\epsilon) = 0$  
> $\because g'(t) = f'(t) - \frac{f(b)-f(a)}{b-a} - \lambda(t-a) - \lambda(t-b), g''(t) = f''(t) - 2 \lambda$  
> $\therefore 0 = g''(\epsilon) = f''(\epsilon) - 2 \lambda \Rightarrow f''(\epsilon) = 2 \lambda$  
> $\therefore \frac{\frac{f(x)-f(a)}{x-a}-\frac{f(b)-f(a)}{b-a}}{x-b} = \frac 1 2 f''(\epsilon)$
## 3.7 Optimization Problems
### 3.7.41 **Minimum time** &emsp; A man is in a boat 2 miles from the nearest point on the coast. He is traveling to a point $Q$, located 3 miles down the coast and 1 mile inland (see figure). He can row at 2 miles per hour and walk at 4 miles per hour. Toward what point on the coast should he row in order to reach point $Q$ in the least time?
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/3-7-41-figure.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/3-7-41-answer.png)
### 3.7.42 **Minimum time** &emsp; The conditions are the same as in Exercise 41 except that the man can row at $v_1$ miles per hour and walk at $v_2$ miles per hour. If $\theta_1$ and $\theta_2$ are the magnitudes of the angles, show that the man will reach point Q in the least time when $\frac{\sin \theta_1}{v_1} = \frac{\sin \theta_2}{v_2}$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/3-7-42.png)
### 3.7.45 **Maximum  Volume** &emsp; A sector with central angle $\theta$ is cut from a circle of radius 12 inches (see figure), and the edges of the sector are brought together to form a cone. Find the magnitude of $\theta$ such that the volume of the cone is a maximum.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/3-7-45-figure.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/3-7-45-answer.png)
### 3.7.52 **Maximum area** &emsp; Consider a symmetric cross inscribed in a circle of radius $r$ (see figure).  
### (a) Write the area A of the cross as a function of x and find the value of x that maximizes the area.
### (b) Write the area A of the cross as a function of $\theta$ and find the value of $\theta$ that maximizes the area.
### (c) Show that the critical numbers of parts (a) and (b) yield the same maximum area. What is that area?
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/3-7-52-figure.png)
![avater](Images/Ron%20Larson%20and%20Bruce%20Edwards/3-7-52-answer-a.png)
![avater](Images/Ron%20Larson%20and%20Bruce%20Edwards/3-7-52-answer-b.png)
![avater](Images/Ron%20Larson%20and%20Bruce%20Edwards/3-7-52-answer-c.png)
### 3.7.54 Find the minimum value of $\frac{(x+\frac 1 x)^6-(x^6+\frac 1 {x^6})-2}{(x+\frac 1 x)^3+(x^3+\frac 1 {x^3})}$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/3-7-54.png)

## 3.9 Differentials
### **Exercise** &emsp; Compare $\tan 1$ with $3/2$ and $2\sin 1$.
### $\frac{2\sin 1}{\tan 1} = 2\cos 1 \gt 2\cos(\frac \pi 3)=1$, so $2\sin1 > \tan 1$  
### Compare $\tan 1$ with $\frac 3 2$ by Tangent Line Approximations  
### $\tan 1 = \tan(\frac{\pi}{3}+(1-\frac{\pi}{3})) \approx \tan \frac{\pi}{3}+\sec^2(\frac{\pi}{3})(1-\frac{\pi}{3})=\sqrt3-4(\frac{\pi}{3}-1)\approx 1.54$  
### Check the figure below, we know real $\tan 1$ is greater than $1.54$, so $\tan 1 > \frac 3 2$  
### So $2\sin 1 \gt \tan 1 \gt \frac 3 2$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/3-9.png)

## Problem Solving
### 5. **Extended  Mean  Value  Theorem** &emsp; Prove the Extended Mean Value Theorem: If $f$ and $f'$ are continuous on the closed interval $[a, b]$, and if $f''$ exists in the open interval $(a, b)$, then there exists a number $c$ in $(a, b)$ such that  
### $f(b)=f(a)+f'(a)(b-a)+\frac 1 2 f''(c)(b-a)^2$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/3-PS-5.png)
### 11.  **Proof** &emsp; Let $f$ and $g$ be functions that are continuous on $[a, b]$ and differentiable on $(a, b)$. Prove that if $f(a)=g(a)$ and $g'(x)>f'(x)$ for all $x$ in $(a, b)$, then $g(b)>f(b)$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/3-PS-11.png)
### 15. **Darboux's  Theorem** &emsp; Prove Darboux's Theorem: Let $f$ be differentiable on the closed interval $[a, b]$ such that $f'(a)=y_1$ and $f'(b)=y_2$. If $d$ lies between $y_1$ and $y_2$, then there exists $c$ in $(a, b)$ such that $f'(c)=d$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/3-PS-15.png)


# 4. Integration
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/5-Basic%20Integration%20Formulas.png)
## 4.1 Antiderivatives and Indefinite Integration
### 4.1.79 **Proof** &emsp; Let $s(x)$ and $c(x)$ be two functions satisfying $s'(x)=c(x)$ and $c'(x)=-s(x)$ for all $x$. If $s(0)=0$ and $c(0)=1$, prove that $(s(x))^2+(c(x))^2=1$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/4-1-79.png)
### 4.1.81 Suppose $f$ and $g$ are non-constant, differentiable, real-valued functions defined on $(-\infty, \infty)$. Furthermore, suppose that for each pair of real numbers $x$ and $y$,  
### $f(x+y)=f(x)f(y)-g(x)g(y)$ and $g(x+y)=f(x)f(y)+g(x)g(y)$.  
### If $f'(0)=0$, prove that $(f(x))^2+(g(x))^2=1$ for all $x$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/4-1-81.png)

## 4.4 The Fundamental Theorem of Calculus
### Theorem 4.9 The Fundamental Theorem of Calculus
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/theorem-4.9.png)
### Theorem 4.10 Mean Value Theorem for Integrals
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/theorem-4.10.png)
### Theorem 4.11 The Second Fundamental Theorem of Calculus
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/theorem-4.11.png)
### 4.4.115 For each continuous function $f:[0, 1] \rightarrow R$, let $I(f)=\int_0^1 x^2f(x)dx$ and $J(f)=\int_0^1 x(f(x))^2dx$. Find the maximum value of $I(f)-J(f)$ over all such functions $f$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/4-4-115.png)

## 4.5 Integration by Substitution
### 4.5.103 If $a_0, a_1, .  .  ., a_n$ are real numbers satisfying $\frac{a_0}{1}+\frac{a_1}{2}+\frac{a_2}{3}+...+\frac{a_n}{n+1}=0$, show that equation $a_0+a_1x+a_2x^2+...+a_nx^n=0$ has at least one real root.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/4-5-103.png)
### 4.5.104 Find all the continuous positive functions $f(x)$, for $0\leq x\leq 1$, such that $\int_0^1f(x)dx=1, \int_0^1f(x)xdx=\alpha, \int_0^1f(x)x^2dx=\alpha^2$ where $\alpha$ is a given real number.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/4-5-104.png)
### 4-PS-1 **Using a Function** &emsp; Let $L(x)=\int_1^x \frac 1 t dt, x>0$.  
### (a) Find $L(1)$.
### (b) Find $L'(x)$ and $L'(1)$.
### (c) Use a graphing utility to approximate the value of $x$ (to three decimal places) for which $L(x)=1$.
### (d) Prove that $L(x_1x_2)=L(x_1)+L(x_2)$ for all positive values of $x_1$ and $x_2$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/4-PS-1.png)
### 4-PS-9 Prove &emsp; $\int_0^x f(t)(x-t)dt=\int_0^x (\int_0^t f(v)dv)dt$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/4-PS-9.png)
### 4-PS-16 Prove that if $f$ is a continuous function on a closed interval $[a, b]$, then $|\int_a^b f(x)dx| \leq \int_a^b |f(x)|dx$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/4-PS-16.png)


# 5. Logarithmic, Exponential, and Other Transcendental Functions
## 5.2 The Natural Logarithmic Function: Integration
### Integrals of Trigonometric Functions
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/5-2-Integrals%20for%20Trigonometric%20Functions.png)
### 5.2.101 Suppose that $f$ is a function on the interval $[1, 3]$ such that $-1 \leq f(x) \leq 1$ for all $x$ and $\int_1^3 f(x)dx=0$. How large can $\int_1^3 \frac{f(x)}{x}dx$ be ?
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/5-2-101.png)

## 5.4 Exponential Functions:  Differentiation and Integration
### 5.4.145  Let $S$ be a class of functions from $[0, \infty) to [0, \infty)$ that satisfies:  
### (i) The functions $f_1(x)=e^x-1$ and $f_2(x)=ln(x+1)$ are in S;  
### (ii) If $f(x)$ and $g(x)$ are in $S$, the functions $f(x)+g(x)$ and $f(g(x))$ are in S;
### (iii) If $f(x)$ and g(x) are in $S$ and $f(x)\geq g(x)$ for all $x\geq 0$, then the function $f(x)-g(x)$ is in $S$.  
### Prove that if $f(x)$ and $g(x$ are in $S$, then the function $f(x)g(x)$ is also in $S$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/5-4-145-1.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/5-4-145-2.png)

## 5.5 Bases other than e and application
### 5.5.113  Logistic Differential Equation Show that solving the logistic differential equation $\frac{dy}{dt}=\frac{8}{25} y (\frac 5 4 - y), y(0)=1$ ults in the logistic growth function $y=\frac{1.25}{1+0.25 e^{-0.4t}}, t \geq 0$.  
### $\left[Hint:\ \frac{1}{y(\frac 5 4 -y)}=\frac 4 5 \left(\frac 1 y + \frac{1}{\frac 5 4 -y}\right) \right]$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/5-5-113.png)
### 5.5.117 Show that if $x$ is positive, then $\log_e^{(1+\frac 1 x)} \gt \frac 1 {1+x}$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/5-5-117.png)

## 5.6 Indeterminate Forms and L'Hôpital's Rule
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-5.17.png)
### 5.6.117 Evaluate $\lim\limits_{x\rightarrow \infty} \left[\frac 1 x \cdot \frac{a^x-1}{a-1} \right]^{\frac 1 x}$ where $a>0, a \neq 1$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/5-6-117.png)

## 5.7 Inverse Trigonometric Functions:  Differentiation
### Definition of Inverse Trigonometric Functions
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/5-Definition%20of%20Inverse%20Trigonometric%20Functions.png)
### Graph of Inverse Trigonometric Functions
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/5-Graphs%20of%20Six%20Inverse%20Trigonometric%20Functions.png)
### Derivatives of Inverse Trigonometric Functions
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-5.18.png)
### 5.7.27 Evaluating  an  Expression without using a calculator.  
### (Hint: Sketch a right triangle)
### (a) $\cot \left[\arcsin(-\frac 1 2) \right]$ &emsp; (b) $\csc \left[\arctan(-\frac{5}{12}) \right]$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/5-7-27.png)
### 5.7.35 Simplifying an Expression Using a Right Triangle, write the expression in algebraic form. 
### (Hint: Sketch a right triangle)  
### $\csc \left(\arctan \frac{x}{\sqrt 2} \right)$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/5-7-35.png)

## 5.8 Inverse Trigonometric Functions: Integration
### 5.8.67 **Area**  
### (a) Sketch the region whose area is represented by $\int_0^1 \arcsin x dx$.  
### (b) Use the integration capabilities of a graphing utility to approximate the area.  
### (c) Find the exact area analytically.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/5-8-67.png)

## 5.9 Hyperbolic Functions
### Definition, Graphs and Properties
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/5-Definition%20of%20Hyperbolic%20Functions.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/5-Graphs%20of%20Six%20Hyperbolic%20Functions.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/5-Hyperbolic%20Identities.png)
### Derivatives and Integrals
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-5.20.png)
### Inverse Hyperbolic Functions
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-5.21.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/5-Graphs%20of%20Six%20Inverse%20Hyperbolic%20Functions.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-5.22.png)

# 6. Differential Equations
## 6.1 Slope Fields and Euler's Method
### Euler's Method
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/6-Euler's%20Method.png)

## 6.2 Growth and Decay
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/6-Exponential%20Growth%20and%20Decay.png)

## 6.3 Separation of Variables and the Logistic Equation
### Logistic Differential Equation
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/6-Logistic%20Differential%20Equation.png)
### Deriving the General Solution for Logistic Differential Equation
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/6-Deriving%20the%20General%20Solution%20for%20Logistic%20Differential%20Equation.png)
### 6.3.65 **Finding a Derivative** &emsp; Show that if $y=\frac{1}{1+be^{-kt}}$ then $\frac{dy}{dt}=ky(1-y)$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/6-3-65.png)
### 6.3.66 **Point  of  Inflection** &emsp; For any logistic equation, show that the point of inflection occurs at $y=\frac L 2$ when the solution starts below the carrying capacity $L$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/6-3-66.png)
### 6.3.85 **True or False** &emsp; The families $x^2+y^2=2Cy$ and $x^2+y^2=2Kx$ are mutually orthogonal.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/6-3-85.png)
### 6.3.86 A not uncommon calculus mistake is to believe that the product rule for derivatives says that $(fg)'=f'g'$. If $f(x)=e^{x^2}$ determine, with proof, whether there exists an open interval $(a, b)$ and a nonzero function g defined on $(a, b)$ such that this wrong product rule is true for $x4 in $(a, b)$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/6-3-86.png)

## 6.4 First-Order Linear Differential Equation
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-6.2.png)
### 6-4-42 **Integrating Factor** &emsp; Explain why you can omit the constant of integration when finding an integrating factor.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/6-4-42.png)
### **Solving a Bernoulli Differential Equation** &emsp; The Bernoulli equation is a well-known nonlinear equation of the form $y'+P(x)y=Q(x)y^n$ that can be reduced to a linear form by a substitution.  
### The general solution of a Bernoulli equation is $y^{1-n} e^{\int (1-n)P(x)dx}=\int (1-n)Q(x)e^{\int (1-n)P(x)dx}dx+C$.
### 6-4-60 $xy'+y=x^2 \sqrt{y}, x>0$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/6-4-60.png)
### 6-PS-4 **Error Using Product Rule** &emsp; Although it is true for some functions $f$ and $g$, a common mistake in calculus is to believe that the Product Rule for derivatives is $(fg)'=f'g'$.  
### (a) Given $g(x)=x$, find $f$ such that $(fg)'=f'g'$.  
### (b) Given an arbitrary function g, find a function f such that $(fg)'=f'g'$.  
### (c) Describe what happens if $g(x)=e^x$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/6-PS-4.png)
### 6-PS-8 **Rewriting the Logistic Equation** &emsp; Show that the logistic equation $y=\frac{L}{1+be^{-kt}}$ can be written as $y=\frac{1}{2} L \left[1+\tanh(\frac{1}{2}k(t-\frac{\ln b}{k})) \right]$.  
### What can you conclude about the graph of the logistic equation?
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/6-PS-8.png)


# 7. Applications of Integration
## 7.1 Area of a Region Between Two Curves
### 7.1.82 **Area** &emsp; Let $a>0$ and $b>0$. Show that the area of the ellipse $\frac{x^2}{a^2}+\frac{y^2}{b^2}=1$ is $\pi ab$(see figure).
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-1-82.png)
### 7.1.87 The horizontal line intersects the curve in the first quadrant as shown in the figure. Find so that the areas of the two shaded regions are equal.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-1-87.png)

## 7.2 Volume:The Disk Method
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-Disk%20Method.png)
### The Washer Method
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-Washer%20Method.png)
### 7.2.75 **Using Cross Sections** &emsp; Find the volume of the solid ofintersection (the solid common to both) of the two right circular cylinders of radius whose axes meet at right angles(see figure).
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-2-75-Figure.png)
### The cross sections are squares. By symmetry, you can set up an integral for an eighth of the volume and multiply by 8.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-2-75.png)
### 7.2.76 Using Cross Sections The solid shown in the figure has cross sections bounded by the graph of $|a|^a+|b|^a=1$, where $1 \leq a \leq 2$.  
### (a) Describe the cross section when $a=1$ and $a=2$.  
### (b) Describe a procedure for approximating the volume of the solid.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-2-76-Figure.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-2-76.png)

## 7.3 Volume: The Shell Method
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-Shell%20Method-1.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-Shell%20Method-2.png)
### Comparison of Disk and Shell Methods
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-Comparison%20of%20Disk%20and%20Shell%20Methods.png)
### **Choosing a Method** &emsp; Use the disk method or the  shell method to find the volumes of the solids generated by revolving the region bounded by the graphs of the equations about the x-axis. 
### 7.3.32 &emsp; $x^{\frac 2 3}+y^{\frac 2 3}=a^{\frac 2 3}, a>0$ (hypocycloid)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-3-32.png)
### **Comparing Integrals** &emsp; In Exercises 39 and 40, give a geometric  argument that explains why the integrals have equal values.  
### 7.3.39 $\pi \int_1^5 (x-1)dx=2\pi \int_0^2 y[5-(y^2-1) ]dy$  
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-3-39.png)
### 7.3.40 $\pi \int_0^2 [16-(2y)^2 ] dx=2\pi \int_0^4 x(\frac{x}{2})dx$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-3-40.png)

## 7.4 Arc Length and Surfaces of Revolution
### Arc Length
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-Arc%20Length.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-Definition%20of%20Arc%20Length.png)
### Area of a Surface of Revolution
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-Surface%20of%20Revolution-1.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-Surface%20of%20Revolution-2.png)
### 7.4.34 **Astroid** &emsp; Find the total length of the graph of the astroid $x^{\frac 2 3}+y^{\frac 2 3}=4$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-4-34.png)

## 7.6 Moments, Centers of Mass, and Centroids
### Common Measurement of Mass and Force
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-Common%20Measurements%20of%20Mass%20and%20Force.png)
### Moment of m about a point
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-Moment%20about%20a%20Point.png)
### Moments and Center of Mass: One-Dimensional System
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-Moment%20and%20Center%20of%20Mass-1.png)
### Moment of a Force
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-Moment%20of%20a%20Force.png)
### Center of Mass in a Two-Dimensional System
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-Moment%20and%20Center%20of%20Mass-2.png)
### Center of Mass of a Planar Lamina
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-Moment%20and%20Center%20of%20Mass-3.png)
### Theorem of Pappus
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-7.1.png)

## 7.7 Fluid Pressure and Fluid Force
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/7-Force%20Exerted%20by%20a%20Fluid.png)


# 8. Integration Techniques and Improper Integrals
## 8.1 Basic Integration Rules
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-Fitting%20Integrands%20to%20Basic%20Integration%20Rules.png)
### 8.1.104 Evaluate $\int_2^4 \frac{\sqrt{ln(9-x)}dx}{\sqrt{ln(9-x)}+\sqrt{ln(x+3)}}$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-1-104.png)
### 区间再现
> This document discusses the case of $\int_a^b f(x)dx$ where $f(x)+f(a+b-x) is a constant$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-1-%E5%8C%BA%E9%97%B4%E5%86%8D%E7%8E%B0.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-1-%E5%8C%BA%E9%97%B4%E5%86%8D%E7%8E%B0-figure.png)
### 公式推广
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-1-%E5%8C%BA%E9%97%B4%E5%86%8D%E7%8E%B0%E6%8E%A8%E5%B9%BF%E5%85%AC%E5%BC%8F.png)
### 8.1.105 Evaluate $\int_{-1}^1\ \frac{dx}{(e^x+1)(x^2+1)}$.
> Let $f(x)=\frac 1 {x^2+1}, g(x)=\frac 1 {e^x+1}$  
> $\because f(x)=f(0-x), g(x)+g(0-x)=1$  
> $\therefore \int_{-1}^1\ \frac{dx}{(e^x+1)(x^2+1)}=\frac 1 2 \int_{-1}^1\ \frac{dx}{x^2+1}=\frac 1 2 \arctan |_{-1}^1=\frac{\pi} 4$

## 8.2 Integration by Parts
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-8.1.png)
### How to choose $u$ and $dv$ ?
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-Integration%20by%20Parts.png)
### Tabular Integration by Parts
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-Tabular%20Integration%20by%20Parts.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-Tabular%20Integration%20by%20Parts%20Example.png)
### Tabular Method for Miscellaneous Indefinite Integrals
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-Tabular%20Method%20for%20Miscellaneous%20Indefinite%20Integrals.png)
### 8.2.100 Find a real number c and a positive number L for which $\lim\limits_{r\rightarrow \infty} \frac{r^c \int_0^{\frac{\pi}{2}}x^r \sin x dx}{\int_0^{\frac{\pi}{2}}x^r \cos x dx}=L$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-2-100-1.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-2-100-2.png)

## 8.3 Trigonometric Integrals
### Integrals Involving Powers of Sine and Cosine
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-Integrals%20Involving%20Powers%20of%20Sine%20and%20Cosine.png)
### Wallis's Formulas
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-Wallis's%20Formulas.png)
### Product-to-Sum Formulas
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-Product-to-Sum%20Formulas.png)
### 8.3.81 Prove $\int \cos^mx \sin^nxdx=-\frac{\cos^{m+1}x \sin^{n-1}x}{m+n}+\frac{n-1}{m+n}\int \cos^mx \sin^{n-2}xdx$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-3-81.png)
### 8.3.88 **Orthogonal Functions** &emsp; The inner product of two functions $f$ and $g$ on $[a, b]$ is given by $<f, g>=\int_a^b f(x)g(x)dx$. Two distinct functions f and g are said to be orthogonal if $<f, g>=0$. Show that the following set of functions is orthogonal on $[-\pi, \pi ]$.  
### $\{\sin x, \sin 2x, \sin 3x, ..., \cos x, \cos 2x, \cos 3x, ...\}$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-3-88.png)
### 8.3.89 **Fourier Series** &emsp; The following sum is a finite Fourier series. $f(x)=\sum\limits_{i=1}^N a_i \sin ix$.  
### (a) Use Exercise 88 to show that the $nth$ coefficient $a_n$ is given by $a_n=\frac{1}{\pi} \int_{-\pi}^{\pi} f(x) \sin nx dx$.  
### (b) Let f(x)=x. Find $a_1, a_2$ and $a_3$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-3-89.png)

## 8.4 Trigonometric Substitution
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-Trigonometric%20Substitution.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-8.2.png)
### 8.4.69 Evaluate $\int_0^1 \frac{ln(x+1)}{x^2+1} dx$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-4-69-1.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-4-69-2.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-4-69-3.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-4-69-4.png)

## 8.5 Partial Fractions
### Partial Fractions Decomposition
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-Partial%20Fractions%20Decomposition.png)
### Heaviside's Method
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-Heaviside's%20Method-0.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-Heaviside's%20Method-1.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-Heaviside's%20Method-2.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-Heaviside's%20Method-3.png)
### 8.5.19 Use partial fractions to find the indefinite integral $\int \frac{x^2+5}{x^3-x^2+x+3} dx$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-5-19.png)
### 8.5.51 Using two methods Evaluate $\int_0^1 \frac{x}{1+x^4} dx$ wo different ways, one of which is partial fractions.
> Solution 1: Let $x^2=t\ or\ \tan t$.  
> Solution 2: 
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-5-51.png)
### 8.5.52 Prove $\frac{22}{7}-\pi=\int_0^1 \frac{x^4(1-x)^4}{1+x^2}dx$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-5-52.png)
### 8.5.53 Let $p(x)$ be a nonzero polynomial of degree less than 1992 having no nonconstant factor in common with $x^3-x$. Let $\frac{d^{1992}}{dx^{1992}} \left(\frac{P(x)}{x^3-x} \right)=\frac{f(x)}{g(x)}$ for polynomials $f(x)$ and $g(x)$. Find the smallest possible degree of $f(x)$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-5-53.png)

## 8.6 Numerical Integration
### The Trapezoidal Rule
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-Trapezoidal%20Rule.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-8.3.png)
### Simpson's Rule
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-8.4.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-8.5.png)
### Error Analysis
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-8.6.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-Error%20Analysis%20of%20the%20Trapezoidal%20Rule.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-Error%20Analysis%20of%20the%20Midpoint%20Rule.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-Error%20Analysis%20of%20the%20Simpson's%20Rule.png)
### 万能公式
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-%E4%B8%87%E8%83%BD%E5%85%AC%E5%BC%8F.png)
### 8-7-47 Proof Prove that you can find a polynomial $p(x)=Ax^2+Bx+C$ that passes through any three points $(x_1, y_1), (x_2, y_2)$, and $(x_3, y_3)$, where the $x_i$'s are distinct.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-7-47.png)
### 8.7.73 Evaluate $\int_0^{\frac{\pi}{2}} \frac{dx}{1+(\tan x)^{\sqrt 2}}$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-7-73.png)

## 8.8 Improper Integrals
### Definition of Improper Integrals with Infinite Integration Limits
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-Definition%20of%20Improper%20Integrals%20with%20Infinite%20Integration%20Limits.png)
### Definition of Improper Integrals with Infinite Discontinuities
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-Definition%20of%20Improper%20Integrals%20with%20Infinite%20Discontinuities.png)
### A Special Type of Improper Integral
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-8.7.png)
### 8.8.50 Finding Values Determine all values of for $p$ which the improper integral converges.  
### $\int_0^1 \frac{1}{x^p} dx$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-8-50.png)
### 8.8.51 **Mathematical Induction** &emsp; Use mathematical induction to verify that the following integral converges for any positive integer n.  
### $\int_0^{\infty} x^n e^{-x} dx$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-8-51.png)
### 8.8.52 **Comparison Test for Improper Integrals** &emsp; In some cases, it is impossible to find the exact value of an improper integral, but it is important to determine whether the integral converges or diverges. Suppose the functions f and g are continuous and $0≤g(x)≤f(x)$ on the interval $[a, ∞)$.   
### It can be shown that if $∫_a^{\infty} f(x) dx$ converges, then $\int_a^{\infty} g(x) dx$ also converges,  
### and if $∫_a^{\infty} g(x) dx$ diverges, then $∫_a^{\infty} f(x) dx$ also diverges. This is known as the Comparison Test for improper integrals.  
### (a) Use the Comparison Test to determine whether $\int_1^{\infty} e^{−x^2} dx$ converges or diverges. (Hint: Use the fact that $e^{−x^2}≤e^{−x}$ for $x≥1$)  
### (b) Use the Comparison Test to determine whether $\int_1^{\infty} \frac{1}{1+x^5} dx$ converges or diverges. (Hint: Use the fact $\frac{1}{1+x^5} \leq \frac{1}{x^5}$ for $x \geq 1$)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-8-52.png)
### **Probability** 
> A nonnegative function is called a probability density function if $\int_{-\infty}^{\infty} f(t) dt = 1$.  
> The probability that lies between and is given by $P(a \leq x \leq b)=\int_a^b f(t)dt$.  
> The expected value of is given by $E(x)=\int_{-\infty}^{\infty} tf(t)dt$.  
### 8.8.73 (a) Show that the nonnegative function is a probability density function, and (b) find $P(0≤x≤6)$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-8-73.png)
### 8.8.88 **Exploration** &emsp; Consider the integral $\int_0^{\pi/2} \frac{4}{1+(\tan x)^n} dx$ where $n$ is a positive integer.  
### (a) Is the integral improper? Explain.  
### (b) Use a graphing utility to graph the integrand for $n=2, 4, 8, and 12$.  
### (c) Use the graphs to approximate the integral as $n \rightarrow \infty$.
### (d) Use a computer algebra system to evaluate the integral for the values of $n$ in part (b). Make a conjecture about the value of the integral for any positive integer $n$. Compare your results with your answer in part (c).
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-8-88.png)
> For part (c), here is the detailed answer:  
> Solution 1: Let $I=\lim\limits_{n \rightarrow \infty} \int_0^{\frac{\pi}{2}} \frac{4}{1+(\tan x)^n} dx$, 根据区间再现公式,  
> $I=\frac 1 2 (\lim\limits_{n \rightarrow \infty} \int_0^{\frac{\pi}{2}} \frac{4}{1+(\tan x)^n} dx + \lim\limits_{n \rightarrow \infty} \int_0^{\frac{\pi}{2}} \frac{4}{1+(\tan (\frac{\pi}{2}-x))^n} dx)=2(\lim\limits_{n \rightarrow \infty} \int_0^{\frac{\pi}{2}} (\frac{1}{1+(\tan x)^n}+\frac{(\tan x)^n}{1+(\tan x)^n}) dx)=\pi$  
> Solution 2: $\lim\limits_{n \rightarrow \infty} \int_0^{\frac{\pi}{2}} \frac{4}{1+(\tan x)^n} dx=\lim\limits_{n \rightarrow \infty} \int_0^{\frac{\pi}{4}} \frac{4}{1+(\tan x)^n}dx+\lim\limits_{n \rightarrow \infty} \int_{\frac{\pi}{4}}^{\frac{\pi}{2}} \frac{4}{1+(\tan x)^n}dx$  
> According to Mean Value Theorem of Integrals, $\exists c_1 \in (0, \frac{\pi}{4})), c_2 \in (\frac{\pi}{4}, \frac{\pi}{2})$, such that $0<\tan c_1 < 1, \tan c_2 > 1$
> $\lim\limits_{n \rightarrow \infty} \int_0^{\frac{\pi}{4}} \frac{4}{1+(\tan x)^n}dx+\lim\limits_{n \rightarrow \infty} \int_{\frac{\pi}{4}}^{\frac{\pi}{2}} \frac{4}{1+(\tan x)^n}dx=\lim\limits_{n \rightarrow \infty} \frac{\pi}{4} \frac{4}{1+(\tan c_1)^n}+\lim\limits_{n \rightarrow \infty} \frac{\pi}{4} \frac{4}{1+(\tan c_2)^n}=\frac{\pi}{4} \frac{4}{1+0}+0=\pi$
### **Laplace Transforms** &emsp; Let $f(t)$ be a function defined for all positive values of $t$. The Laplace Transform of $f(t)$ is defined by $F(s)=\int_0^{\infty} e^{-st}f(t)dt$ when the improper integral exists. Laplace Transforms are used to solve differential equations. In Exercises 91–98, find the Laplace Transform of the function.  
### 8.8.91 $f(t)=1$  
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-8-91.png)
### 8.8.92 $f(t)=t$  
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-8-92.png)
### 8.8.93 $f(t)=t^2$  
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-8-93.png)
### 8.8.94 $f(t)=e^{at}$  
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-8-94.png)
### 8.8.95 $f(t)=\cos(at)$  
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-8-95.png)
### 8.8.96 $f(t)=\sin(at)$  
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-8-96.png)
### 8.8.97 $f(t)=\cosh(at)$  
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-8-97.png)
### 8.8.98 $f(t)=\sinh(at)$  
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-8-98.png)
### The  Gamma  Function The Gamma Function $\Gamma(n)$ is defined by $\Gamma(n)=\int_0^{\infty} x^{n-1}e^{-x}dx,\ n>0$.  
### (a) Find $\Gamma(1), \Gamma(2), and \Gamma(3)$.  
### (b) Use integration by parts to show that $\Gamma(n+1)=n\Gamma(n)$.  
### (c) Write $\Gamma(n)$ using factorial notation where n is a positive integer.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-8-99.png)
### 8.PS.1 **Wallis's Formulas**  
> (a) Evaluate the integrals $\int_{-1}^1 (1-x^2)dx$ and $\int_{-1}^1 (1-x^2)^2dx$.  
> (b) Use Wallis's Formulas to prove that $\int_{-1}^1 (1-x^2)^n dx$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-PS-1.png)
### 8.PS.2 **Proof**
> (a) Evaluate the integrals $\int_0^1 \ln x dx$ and $\int_0^1 (\ln x)^2 dx$.  
> (b) Prove that $\int_0^1 (\ln x)^n dx=(-1)^n n!$ for positive integers $n$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-PS-2.png)
### 8-PS-7 **Centroid** &emsp; Find the centroid of the region bounded by the x-axis and the curve $y=e^{−c^2x^2}$, where $c$ is a positive constant (see figure). (Hint: Show that $\int_0^{\infty} e^{−c^2x^2}dx=\frac 1 c \int_0^{\infty} e^{−x^2}dx$)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-PS-7-1.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-PS-7-2.png)
### 8-PS-8 Prove the following generalization of the Mean Value Theorem. If $f$ is twice differentiable on the closed interval $[a, b]$, then $f(b)-f(a)=f'(a)(b-a)-\int_a^b f''(t)(t-b)dt$.
> Proof: $\int_a^b f''(t)(t-b)dt=(t-b)f'(t)|_a^b-f(t)|_a^b=-(a-b)f'(a)-(f(b)-f(a))$
### 8-PS-9 **Inverse Function and Area**
> (a) Let $y=f^{-1}(x)$ be the inverse function of f. Use integration by parts to derive the formula $\int f^{-1}(x)dx=xf^{-1}(x)-\int f(y)dy$.  
> (b) Use the formula in part (a) to find the integral $\int \arcsin x dx$.  
> (c) Use the formula in part (a) to find the area under the graph of $y=\ln x, 1 \leq x \leq e$(see figure).
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-PS-9-1.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-PS-9-2.png)
### 8-PS-11 **Partial Fraction Decomposition** &emsp; Suppose the denominator of a rational function can be factored into distinct linear factors $D(x)=(x-c_1)(x-c_2)...(x-c_n)$ for a positive integer $n$ and distinct real numbers $c_1, c_2, ..., c_n$. If $N$ is a polynomial of degree less than $n$, show that $\frac{N(x)}{D(x)}=\frac{P_1}{x-c_1}+\frac{P_2}{x-c_2}+...+\frac{P_n}{x-c_n}$ where $P_k=\frac{N(c_k)}{D'(c_k)}$ for $k=1, 2, ..., n$. Note that this is the partial fraction decomposition of $\frac{N(x)}{D(x)}$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-PS-11.png)
### 8-PS-16 Suppose that $f(a)=f(b)=g(a)=g(b)=0$ and the second derivatives of $f$ and $g$ are continuous on the closed interval $[a, b]$. Prove that $\int_a^b f(x)g''(x)dx=\int_a^b f''(x)g(x)dx$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-PS-16.png)
### 8-PS-17 Suppose that $f(a)=f(b)=0$ and the second derivatives of $f$ exist on the closed interval $[a, b]$. Prove that $\int_a^b (x-a)(x-b)f''(x)dx=2\int_a^b f(x)dx$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/8-PS-17.png)


# 9 Infinite Series
## 9.1 Sequences
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-9.1.png)
### Absolute Value Theorem
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-9.4.png)
### Bounded monotonic Sequences
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-9.5.png)
### 9.1.83 **Using a Sequence** &emsp; Consider the sequence $\sqrt2, \sqrt{2+\sqrt2}, \sqrt{2+\sqrt{2+\sqrt2}}, ...$, find $\lim\limits_{n\rightarrow \infty} a_n$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-1-83.png)
### 9.1.84 **Using a Sequence** &emsp; Consider the sequence where $a_a=\sqrt{k}, a_{n+1}=\sqrt{k+a_n}$, and $k>0$. Show that is increasing and bounded, find $\lim\limits_{n\rightarrow \infty} a_n$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-1-84.png)
### 9-1-85 **Squeeze Theorem**  
### (a) Show that $\int_1^n \ln x dx < \ln(n!)$ for $n \geq 2$.  
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-1-85-1.png)
### (b) Draw a graph similar to the one above that shows $\ln(n!)<\int_1^{n+1} \ln x dx$.  
### (c) Use the results of parts (a) and (b) to show that $\frac{n^n}{e^{n-1}}<n!<\frac{(n+1)^{n+1}}{e^n}$, for $n>1$.  
### (d) Use the Squeeze Theorem for Sequences and the result of part (c) to show that $\lim\limits_{n\rightarrow \infty} \frac{^n \sqrt{n!}}{n}=\frac 1 e$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-1-85-2.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-1-85-3.png)
### 9-1-87 Use the definition of the limit of a sequence to prove that $\lim\limits_{n\rightarrow \infty} r^n=0$ for $-1 < r < 1$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-1-87.png)
### 9-1-90 Let $\{x_n\}, n\geq0$, be a sequence of nonzero real numbers such that $x_n^2-x_{n-1}x_{n+1}=1$ for $n=1, 2, 3, ...$. Prove there exists a real number $a$ such that $x_{n+1}=ax_n-x_{n-1}$ for all $n\geq1$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-1-90.png)
### 9-1-91 Let $T_0=2, T_1=3, T_2=6$, and for $n\geq3$, $T_n=(n+4)T_{n-1}-4nT_{n-2}+(4n-8)T_{n-3}$. The first few terms are $2, 3, 6, 14, 40, 152, 784, 5168, 40576$. Find, with proof, a formula for $T_n$ of the form $T_n=A_n+B_n$, where $\{A_n\}$ and $\{B_n\}$ are well-known sequences.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-1-91.png)

## 9.2 Infinite Series
### Geometric Series
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-2-Geometric%20Series.png)
### nth-Term Test for Divergence
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-2-nth-Term%20Test%20for%20Divergence.png)
### Vieta's Formulas
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-2-Vieta's%20formulas.png)
### Euler's Series
> The sum of the squares of the reciprocals of the integers $\sum\limits_{k=1}^{\infty} \frac{1}{k^2} = 1+\frac 1 4+\frac 1 9+\frac 1 {16}+...=\frac{\pi^2}6$  
> Proof 1: Trigonometry and Algebra
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-2-Euler's%20Series-1.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-2-Euler's%20Series-2.png)
> Proof 2: Odd terms, Geometric Series, and a Double Integral
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-2-Euler's%20Series-3.png)
> References
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-2-Euler's%20Series%20References.png)
### 9-2-38 Finding the Sum of a Convergent Series $\sum\limits_{n=1}^{\infty} \frac 1 {9n^2+3n-2}$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-2-38.png)
### 9-2-98 **Proof** &emsp; Given two infinite series $\sum a_n$ and $\sum b_n$ such that $\sum a_n$ converges and $\sum b_n$ diverges, prove that $\sum (a_n+b_n)$ diverges.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-2-98.png)
### 9-2-102 Convergence with Pictures
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-2-102-1.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-2-102-2.png)
### 9-2-103 Express $\sum\limits_{}^{} \frac{6^k}{(3^{k+1}-2^{k+1})(3^k-2^k)}$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-2-103.png)
### 9-2-104 Let $f(n)$ be the sum of the first n terms of the sequence $0, 1, 1, 2, 2, 3, 3, 4, .  .  . $, where the nth term is given by 
$$
a_n=
\begin{cases}
\frac n 2, & \text{if n is even}\\
\frac {n-1} 2, & \text{if n is odd}
\end{cases}
$$
### Show that if $x$ and $y$ are positive integers and $x>y$ then $xy=f(x+y)−f(x−y)$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-2-104.png)

## 9.3 The Integral Test and p-Series
### The Integral Test
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-9.10.png)
### Convergence of p-Series
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-9.11.png)
### 9-3-42 **Using a Function** &emsp; Let $f$ be a positive, continuous, and decreasing function for $x≥1$, such that $a_n=f(n)$. Use a graph to rank the following quantities in decreasing order. Explain your reasoning.  
### (a) $\sum\limits_{n=2}^7 a_n$ &emsp; (b) $\int_1^7 f(x) dx$ &emsp; (c) $\sum\limits_{n=1}^6 a_n$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-3-42.png)
### 9-3-45 **Using a Series** Use a graph to show that the inequality is true. What can you conclude about the convergence or divergence of the series? Explain.  
### (a) $\sum\limits_{n=1}^{\infty} \frac1{\sqrt n}>\int_1^{\infty} \frac1{\sqrt x}dx$ &emsp; (b) $\sum\limits_{n=2}^{\infty} \frac1{n^2}>\int_1^{\infty} \frac1{x^2}dx$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-3-45.png)
### 9-3-66 Find the sum of the series $\sum\limits_{n=2}^{\infty} \ln(1-\frac1{n^2})$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-3-66.png)

## 9.4 Comparisons of Series
### Direct Comparison Test
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-9.12.png)
### A generalization of the comparison test
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-4-A%20generalization%20of%20the%20comparison%20test.png)
### Limit Comparison Test
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-9.13.png)
### 9.4.59 Prove that if the nonnegative series $\sum\limits_{n=1}^{\infty} a_n$ and $\sum\limits_{n=1}^{\infty} b_n$ converge, then so does the series $\sum\limits_{n=1}^{\infty} a_n b_n$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-4-59.png)
### 9-4-63 **Proof** &emsp; Suppose that $\sum a_n$ and $\sum b_n$ are series with positive terms. Prove that if $\lim\limits_{n\rightarrow \infty} \frac{a_n}{b_n}=0$ and $\sum\limits_{n=1}^{\infty} b_n$ converges, $\sum\limits_{n=1}^{\infty} a_n$ also converges.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-4-63.png)
### 9-4-64 **Proof** &emsp; Suppose that $\sum a_n$ and $\sum b_n$ are series with positive terms. Prove that if $\lim\limits_{n\rightarrow \infty} \frac{a_n}{b_n}=\infty$ and $\sum\limits_{n=1}^{\infty} b_n$ diverges, $\sum\limits_{n=1}^{\infty} a_n$ also diverges.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-4-64.png)
### 9-4-67 ** Proof** &emsp; Suppose that $\sum a_n$ is a series with positive terms. Prove that if $\sum a_n$ converges, then $\sum \sin a_n$ also converges.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-4-67.png)
### 9-4-69 **Comparing Series** &emsp; Show that $\sum\limits_{n=1}^{\infty} \frac{\ln n}{n\sqrt n}$ converges by comparison with $\sum\limits_{n=1}^{\infty} \frac1{n^{\frac 5 4}}$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-4-69.png)
### 9-4-71 Is the infinite series $\sum\limits_{n=1}^{\infty} \frac1{n^{\frac{n+1}{n}}}$ convergent? Prove your statement.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-4-71.png)
### 9-4-72 Prove that if $\sum a_n$ is a convergent series of positive real numbers, then so is $\sum\limits_{n=1}^{\infty} a_n^{\frac{n}{n+1}}$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-4-72.png)

## Alternating Series
### Alternating Series Test
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-9.14.png)
### Alternating Series remainder
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-9.15.png)
> Proof:  
$$
\begin{aligned}
\because R_N &=S-S_N=\sum\limits_{n=1}^{\infty}(-1)^{n-1}a_n-\sum\limits_{n=1}^{N}(-1)^{n-1}a_n \\
& =(-1)^N a_{N+1}+(-1)^{N+1} a_{N+2}+(-1)^{N+2}a_{N+3}+... \\
& =(-1)^N(a_{N+1}-a_{N+2}+a_{N+3}-...) \\
\therefore |R_N| & = a_{N+1}-a_{N+2}+a_{N+3}-... \\
& = a_{N+1}-(a_{N+2}-a_{N+3})-(a_{N+4}-a_{N+5})... \\
& \leq a_{N+1} \\
\therefore |R_N| & = |S-S_N| \leq a_{N+1}
\end{aligned}
$$
### Absolute and Conditional Convergence
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-9.16.png)
### Rearrangement of Series
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-5-Rearrangement%20of%20Series.png)
### Riemann’s Rearrangement Theorem
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-5-Riemann%E2%80%99s%20Rearrangement%20Theorem.png)
### 9-5-27 Determine the convergence or divergence of $\sum\limits_{n=1}^{\infty} \frac{(-1)^{n+1}n!}{1\cdot 3\cdot 5...(2n-1)}$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-5-27.png)
### 9-5-28 Determine the convergence or divergence of $\sum\limits_{n=1}^{\infty} \frac{(-1^){n+1}1\cdot 3\cdot 5...(2n-1)}{1\cdot 4\cdot 7...(3n-2)}$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-5-28.png)
### 9-5-30 Determine the convergence or divergence of $\sum\limits_{n=1}^{\infty} \frac{2(-1)^{n+1}}{e^n+e^{-n}}$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-5-30.png)
### 9-5-49 Determine whether the series $\sum\limits_{n=1}^{\infty} \frac{(-1)^n}{n\ln n}$ converges absolutely or conditionally, or diverges.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-5-49.png)
### 9-5-65 Prove that if $\sum |a_n|$ converges, then $\sum a_n^2$ converges.Is the converse  true? If not, give an example that shows it is false.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-5-65.png)
### 9-5-82 Assume as known the (true) fact that the alternating harmonic series  
### (1) $1-\frac12+\frac13-\frac14+\frac15-\frac16+\frac17-\frac18+...$  
### is convergent, and denote its sum by $s$. Rearrange the series (1) as follows:  
### (2) $1-\frac12+\frac3+\frac15-\frac14+\frac17+\frac19-\frac16+\frac1{11}+\frac1{12}-...$  
### Assume as known the (true) fact that the series (2) is alsoconvergent, and denote its sum by $S$. Denote by $s_k, S_k$ the kth partial sum of the series (1) and (2), respectively. Prove the following statements.  
### (i) $S_{3n}=s_{4n}+\frac12s_{2n}$, &emsp; (ii) $S\neq s$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-5-82.png)

## 9.6 The Ratio and Root Tests
### The Ratio Test
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-9.17.png)
### The Root Test
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-9.18.png)
### N! and The Root Test
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-6-N!%20and%20The%20Root%20Test.png)
### Strategies for Testing Series
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-6-Guidelines%20for%20Testing%20a%20Series.png)
### SUMMARY OF TESTS FOR SERIES
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-5-Summary%20of%20Tests%20for%20Series.png)
### 9-6-98 rove Theorem 9.18. (Hint for Property 1: If the limit equals $r<1$, choose a real number $R$ such that $r<R<1$. By the definitions of the limit, there exists some $N>0$ such that $^n\sqrt{|a_n|}<R$ for $n>N$.)
### 9-6-107 Show that if the series $a_1+a_2+a_3+...+a_n+...$ converges, then the series $\frac{a_1}n+\frac{a_2}n+\frac{a_3}n+...+\frac{a_n}n+...$ converges also.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-6-107.png)

## 9.7 Taylor Polynomials and Approximations
### Taylor and Maclaurin Polynomials
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-7-Taylor%20and%20Maclaurin%20Polynomials.png)
### Remainder of a Taylor Polynomial
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-9.19.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-7-Proof%20of%20Taylor%20Theorem.png)
### 9-7-70 Prove that if $f$ is an odd function, then its nth Maclaurin polynomial contains only terms with odd powers of $x$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-7-70.png)
### 9-7-71 Prove that if $f$ is an even function, then its nth Maclaurin polynomial contains only terms with even powers of $x$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-7-71.png)
### 9-7-72 Let $P_n(x)$ be the nth Taylor polynomial for $f$ at $c$.  
### Prove that $P_n(c)=f(c)$ and $P^{(k)}(c)=f^{(k)}(c)$ for $1 \leq k \leq n$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-7-72.png)
### 9-7-73 Consider a function $f$ with continuous first and second derivatives at $x = c$.  
### Prove that if $f$ has a relativemaximum at $x = c$, then the second Taylor polynomial centered at $x = c$ also has a relative maximum at $x = c$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-7-73.png)

## 9.8 Power Series
### Definition of Power Series
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-8-Definition%20of%20Power%20Series.png)
### Radius and Interval of Convergence
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-9.20.png)
### Endpoint Convergence
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-8-Endpoint%20Convergence.png)
### Differentiation and Integration of Power Series
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-9.21.png)
### 9-8-34 find the interval of convergence of $\sum\limits_{n=1}^{\infty} \frac{n!(x+1)^n}{1\cdot3\cdot5...(2n-1)}$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-8-34.png)
### 9-8-65 **Bessel Function** &emsp; The Bessel function of order 0 is $J_0(x)=\sum\limits_{k=0}^{\infty} \frac{(-1)^k x^{2k}}{2^{2k}(k!)^2}$.  
### (a) Show that the series converges for all $x$.  
### (b) Show that the series is a solution of the differential equation $x^2 J_0''+x J_0'+x^2 J_0=0$.  
### (c) Use a graphing utility to graph the polynomial composed of the first four terms of $J_0$.  
### (d) Approximate $\int_0^1 J_0 dx$ accurate to two decimal places.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-8-65.png)
### 9-8-66 **Bessel Function** &emsp; The Bessel function of order 0 is $J_0(x)=x\sum\limits_{k=0}^{\infty} \frac{(-1)^k x^{2k}}{2^{2k+1}k!(k+1)!}$.  
### (a) Show that the series converges for all $x$.  
### (b) Show that the series is a solution of the differential equation $x^2 J_1''+x J_1'+(x^2-1) J_1=0$.  
### (c) Use a graphing utility to graph the polynomial composed of the first four terms of $J_1$.  
### (d) Use $J_0$ from Exercise 65 to show that $J_0'(x) = -J_1(x)$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-8-66.png)
### 9-8-79 **Using a Power Series** &emsp; Let $f(x)=\sum_{n=0}^{\infty} c_n x^n$, where $c_{n+3}=c_n$ for $n \geq 0$.  
### (a) Find the interval of convergence of the series.
### (b) Find an explicit formula for $f(x)$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-8-79.png)

## 9.9
### Geometric Power Series
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-9-Geometric%20Power%20Series.png)
### Finding a Geometric Power Series Centered at 0
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-9-Finding%20a%20Geometric%20Power%20Series%20Centered%20at%200.png)
### Operations with Power Series
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-9-Operations%20with%20Power%20Series.png)
### Finding a Power Series by Integration
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-9-Finding%20a%20Power%20Series%20by%20Integration%201.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-9-Finding%20a%20Power%20Series%20by%20Integration%202.png)
### Approximating $\pi$ with a Series
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-9-Approximating%20pi%20with%20a%20Series.png)
### 9-9-43 Prove that $\arctan x + \arctan y = \arctan \frac{x+y}{1-xy}$ for $xy \neq 1$ provided the value of the left side of the equation is between $-\frac{\pi}{2}$ and $\frac{\pi}{2}$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-9-43.png)

## 9.10 Taylor and Maclaurin Series
### The Form of a Convergent Power Series
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-9.22.png)
### Definition of Taylor and Maclaurin Series
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-10-Definition%20of%20Taylor%20and%20Maclaurin%20Series.png)
### Convergence of Taylor Series
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-9.23.png)
### Binomial Series
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-10-Binomial%20Series.png)
### Power Series for Elementary Function
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-10-Power%20Series%20for%20Elementary%20Function.png)
### Use the definition of Taylor series to find the Taylor series, centered at $c$, for the functions below.
### 9-10-7 $f(x)=\cos x$, &emsp; $c=\frac{\pi}4$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-10-7.png)
> $(-1)^{\frac{n(n-1)}2}=1, 1, -1, -1, 1, 1, -1, -1, 1, 1, ...$
### 9-10-15 $f(x)=\sec x$, &emsp; $c=0(first\ three\ nonzero\ term)$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-10-15.png)
### 9-10-15 $f(x)=\tan x$, &emsp; $c=0(first\ three\ nonzero\ term)$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-10-16.png)
### 9-10-91 Prove that e is irrational. [Hint: Assume that $e=\frac p q$ is rational ($p$ and $q$ are integers) and consider $e=1+1+\frac1{2!}+\frac1{3!}+...+\frac1{n!}+...$.]
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-10-91.png)
### 9-10-92 **Using Fibonacci Numbers** &emsp; Show that the Maclaurin series for the function $g(x)=\frac{x}{1-x-x^2}$ is $\sum\limits_{n=0}^{\infty} F_nx^n$ where $F_n$ is the nth Fibonacci number with $F_1=F_2=1$ and $F_n=F_{n-2}+F_{n-1}$, for $n \geq 3$.  
### (Hint: write $\frac{x}{1-x-x^2}=a_0+a_1x+a_2x^2+...$ and ltiply each side of this equation by $1-x-x^2$.)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-10-92.png)
### 9-10-93 Assume that $|f(x)| \leq 1$ and $|f''(x)|\leq1$ for all $x$ on an interval of length at least 2. Show that $|f'(x)|\leq2$ on the interval.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-10-93.png)

## Review
### 9-R-53 Use the Direct Comparison Test or the Limit Comparison Test to determine the convergence or divergence of the series $\sum\limits_{n=1}^{\infty} \frac{1\cdot3\cdot5...\cdot(2n-1)}{2\cdot4\cdot6...\cdot(2n)}$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/9-R-53.png)


# 10 Conics, Parametric Equations, and Polar Coordinates
## 10.1 Conics and Calculus
### parabolas
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-1-Parabolas.png)
### Reflective Property of a Parabola
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-10.2.png)
### Standard Equation of an Ellipse
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-10.3.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-10.3-2.jpg)
> Let $x'=x+h, y'=y+k$, such that $\frac{(x'-h)^2}{a^2}+\frac{(y'-k)^2}{b^2}=1$
### Reflective Property of an Ellipse
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-10.4.png)
### Definition of Eccentricity of an Ellipse
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-1-Definition%20of%20Eccentricity%20of%20an%20Ellipse.png)
### Eccentricities of the Planetary Orbits
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-1-Eccentricities%20of%20Planetary%20Orbits.png)
### Hyperbolas
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-10.5.png)
### 10-1-64 Prove that if any two tangent lines to a parabola intersect at right angles, then their point of intersection must lie on the directrix.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-1-64.png)
### 10-1-80 Prove Theorem 10.4 by showing that the tangent line to an ellipse at a point P makes equal angles with lines through $P$ and the foci (see figure).  
### [Hint: (1) Find the slope of the tangent line at $P$, (2) find the slopes of the lines through $P$ and each focus, and (3) use the formula for the tangent of the angle $\theta$ between two lines with slopes $m_1$ and $m_2, \tan \theta = |\frac{m_1-m_2}{1+m_1 m_2}|.]$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-1-80.png)
### 10-1-82 **Hyperbola** &emsp; Consider a hyperbola centered at the origin with a horizontal transverse axis. Use the definition of a hyperbola to derive its standard for $\frac{x^2}{a^2}-\frac{y^2}{b^2}=1$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-1-82.png)
### 10-1-86 Prove that the graph of the equation $Ax^2+Cy^2+Dx+Ey+F=0$ is one of the following (except in degenerate cases).  
### (a) Circle &emsp; (when A=C)  
### (b) Parabola &emsp; (when A=0 or C=0, but not both)  
### (c) Ellipse &emsp; (when AC>0)  
### (d) Hyperbola &emsp; (when AC<0)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-1-86.png)
### 10-1-93 For a point P on an ellipse, let d be the distance from the center of the ellipse to the line tangent to the ellipse at P. Prove that $(PF_1)(PF_2)d^2$ is constant as P varies on the ellipse, where $PF_1$ and $PF_2$ are the distances from P to the foci $F_1$ and $F_2$ of the ellipse.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-1-93.png)
### 10-1-94 Find the minimum value of $(u-v)^2+(\sqrt{2-u^2}-\frac9v)^2$ for $0<u<\sqrt2$ and $v>0$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-1-94.png)

## 10.2 Plane Curves and Parametric Equations
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-2-Definition%20of%20a%20Plane%20Curve.png)
### Parametric Equations for a Cycloid
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-2-Parametric%20Equations%20for%20a%20Cycloid.png)
### Definition of a Smooth Curve
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-2-Definition%20of%20a%20Smooth%20Curve.png)

## 10.3 Parametric Equations and Calculus
### Parametric Form of the Derivative
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-10.7.png)
### Arc Length in Parametric Form
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-10.8.png)
### Area of a Surface of Revolution
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-10.9.png)
### 10-3-93 **Involute of a Circle** &emsp; The involute of a circle is described by the endpoint P of a string that is held taut as it is unwound from a spool that does not turn (see figure). Show that a parametric representation of the involute is $x=r(\cos \theta+\theta \sin \theta)$ and $y=r(\sin \theta-\theta \cos \theta)$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-3-93.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-3-93%2694-figure.png)
### 10-3.94 **Involute of a Circle** &emsp; The figure shows a piece of string tied to a circle with a radius of one unit. The string is just long enough to reach the opposite side of the circle. Find the area that is covered when the string is unwound counterclockwise.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-3-94.png)

## 10.4 Polar Coordinates and Polar Graphs
### Polar Coordinates
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-4-Polar%20Coordinates.png)
### Coordinate Conversion
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-10.10.png)
### Slope in Polar Form
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-10.11.png)
### Tangent Lines at the Pole
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-10.12.png)
### Special Polar Graphs
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-4-Special%20Polar%20Graphs.png)
### 10-4-101 ** Rotated Curve** &emsp; Verify that if the curve whose polar equation is $r=f(\theta)$ is rotated about the pole through an angle $\phi$, then an equation for the rotated curve is $r=f(\theta-\phi)$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-4-101.png)
### 10-4-106 Prove that the tangent of the angle $\psi(0\leq\psi\leq\frac{\pi}2)$ between the radial line and the tangent line at the point $(r, \theta)$ on the graph of $r=f(\theta)$(see figure) is given by $\tan \psi=|\frac{r}{dr/d\theta}|$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-4-106.png)

## 10.5 Area and Arc Length in Polar Coordinates
### Area of a Polar Region
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-10.13.png)
### Arc Length in Polar Form
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-10.14.png)
### Area of a Surface of Revolution
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-10.15.png)
### 10-5-51 **Conjecture** &emsp; Find the area of the region enclosed by $r=a\cos(n\theta)$ for n=1, 2, 3, ... Use the results to make a conjecture about the area enclosed by the function when $n$ is even and when $n$ is odd.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-5-51.png)

## 10.6 Polar Equations of Conics and Kepler's Laws
### Classification of Conics by Eccentricity
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-10.16.png)
### Polar Equations of Conics
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-10.17.png)
### 10-6-49 **Ellipse** &emsp; Show that the polar equation for $\frac{x^2}{a^2}+\frac{y^2}{b^2}=1$ is $r^2=\frac{b^2}{1-e^2\cos^2\theta}$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-6-49.png)
### 10-6-50 **Hyperbola** &emsp; Show that the polar equation for $\frac{x^2}{a^2}-\frac{y^2}{b^2}=1$ is $r^2=\frac{-b^2}{1-e^2\cos^2\theta}$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-6-50.png)
### 10-6-60 **Planetary Motion** &emsp; The planets travel in elliptical orbits with the sun as a focus, as shown in the figure.  
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-6-60-figure.png)
### (a) Show that the polar equation of the orbit is given by $r=\frac{(1-e^2)a}{1-e\cos\theta}$ where $e$ is the eccentricity.  
### (b) Show that the minimum distance (perihelion) from the sun to the planet is $r=a(1-e)$ and the maximum distance (aphelion) is $r=a(1+e)$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/10-6-60.png)


# 11 Vectors and the Geometry of Space
## 11.1 Vectors in the Plane
### 11-1-98 Prove that the vector $\vec w=|\vec u|\vec v+|\vec v|\vec u $ bisects the angle between $\vec u$ and $\vec v$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/11-1-98.png)
### 11-1-100  A coast artillery gun can fire at any angle of elevation between $30\degree$ and $90\degree$ in a fixed vertical plane. If air resistance is neglected and the muzzle velocity is constant (= $v_0$), determine the set H of points in the plane and above the horizontal which can be hit.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/11-1-100.png)

## 11.4 The Cross Product of Two Vectors in Space
### The Cross Product
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/11-4-The%20Cross%20Product.png)
### Algebraic Properties of the Cross Product
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-11.7.png)
### Geometric Properties of the Cross Product
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-11.8.png)
### The Triple Scalar Product
![avatar}](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-11.9.png)
### Proof:
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-11.9-proof.png)
### Geometric Property of the Triple Scalar Product
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-11.10.png)
### 11-4-39 **Comparing Dot Products** &emsp; Identify the dot products that are equal. Explain your reasoning. (Assume $\vec u$, $\vec v$, and $\vec w$ are nonzero vectors.)  
### (a) $\vec u \cdot (\vec v \times \vec w)$ &emsp; &emsp; (b) $(\vec v \times \vec w)\cdot \vec u$  
### (c) $(\vec u \times \vec v)\cdot \vec w$ &emsp; &emsp; (d) $(\vec u \times -\vec w)\cdot\vec v$  
### (e) $\vec u \cdot (\vec w \times \vec v)$ &emsp; &emsp; (f) $\vec w \cdot(\vec u \times \vec v)$  
### (g) $(-\vec u \times \vec v)\cdot \vec w$ &emsp;  (d) $(\vec w \times \vec u)\cdot\vec v$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/11-4-39.png)

## 11.5 Lines and Planes in Space
### Parametric Equations of a Line in Space
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-11.11.png)
### Standard Equation of a Plane in Space
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-11.12.png)
### Special Cases of a Plane in Space
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/11-5-Special%20Case%20of%20a%20Plane%20in%20Space.png)
### Distance Between a Point and a Plane
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-11.13.png)
### Finding the Distance Between a Point and a Plane
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/11-5-Finding%20the%20Distance%20Between%20a%20Point%20and%20a%20Plane.png)
### Distance Between a Point and a Line in Space
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-11.14.png)

## 11.6 Surfaces in Space
### Cylindrical Surfaces
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/11-6-Cylindrical%20Surfaces.png)
### Quadric Surfaces
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/11-6-Quadric%20Surfaces-1.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/11-6-Quadric%20Surfaces-2.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/11-6-Quadric%20Surfaces-3.png)
### Surfaces of Revolution
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/11-6-Surfaces%20of%20Revolution.png)
### 11-6-49 **Using a Hyperbolic Paraboloid** &emsp; Determine the intersection of the hyperbolic paraboloid $z=\frac{y^2}{b^2}-\frac{x^2}{a^2}$ with the plane $bx+ay-z=0$(Assume a, b > 0).
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/11-6-49.png)

## 11.7 Cylindrical and Spherical Coordinates
### The Cylindrical Coordinate System
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/11-7-The%20Cylindrical%20Coordinate%20System.png)
### Spherical Coordinates
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/11-7-Spherical%20Coordinates.png)
### 11-PS-7 **Volume**  
### (a) Find the volume of the solid bounded below by the paraboloid $z=x^2+y^2$ and above the plane $z=1$.  
### (b) Find the volume of the solid bounded below by the elliptic paraboloid $z=\frac{x^2}{a^2}+\frac{y^2}{b^2}$ and above by the plane $z=k$, where $k>0$.  
### (c) Show that the volume of the solid in part (b) is equal to one-half the product of the area of the base times the altitude, as shown in the figure.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/11-PS-7-Figure.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/11-PS-7.png)
### 11-PS-8 **Volume**  
### (a) Use the disk method to find the volume of the sphere $x^2+y^2+z^2=r^2$.  
### (b) Find the volume of the ellipsoid $\frac{x^2}{a^2}+\frac{y^2}{b^2}+\frac{z^2}{c^2}=1$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/11-PS-8.png)

# 12 Vector -Valued Functions
## 12.1 Vector-Valued Functions
### Definition of Vector-Valued Function
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-1-Definition%20of%20Vector-Valued%20Function.png)
### Definition of the Limit of a Vector-Valued Function
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-1-Definition%20of%20the%20Limit%20of%20a%20Vector-Valued%20Function.png)
### Definition of Continuity of a Vector-Valued Function
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-1-Definition%20of%20Continuity%20of%20a%20Vector-Valued%20Function.png)
### 12-1-83 **Proof** &emsp; Let $r(t)$ and $u(t)$ be vector-valued functions whose limits exist as $t\rightarrow c$. Prove that $\lim\limits_{t\rightarrow c}[\vec r(t)\times\vec u(t)]=\lim\limits_{t\rightarrow c}\vec r(t)\times\lim\limits_{t\rightarrow c}\vec u(t)$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-1-83.png)
### 12-1-84 **Proof** &emsp; Let $r(t)$ and $u(t)$ be vector-valued functions whose limits exist as $t\rightarrow c$. Prove that $\lim\limits_{t\rightarrow c}[\vec r(t)\cdot\vec u(t)]=\lim\limits_{t\rightarrow c}\vec r(t)\cdot\lim\limits_{t\rightarrow c}\vec u(t)$.

## 12.2 Differentiation and Integration of Vector-Valued Functions
### Differentiation of Vector-Valued Functions
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-12.1.png)
### Properties of the Derivative
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-12.2.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-12.2.1.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-12.2.2.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-12.2.3.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-12.2.4.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-12.2.5.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-12.2.6.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-12.2.7.png)
### Integration of Vector-Valued Functions
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-2-Integration%20of%20Vector-Valued%20Functions.png)
### The Antiderivative of a Vector -Valued Function
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-2-The%20Antiderivative%20of%20a%20Vector%20-Valued%20Function.png)
### **Proof** &emsp; In Exercises 66–67, prove the property. In each case, assume $r$, $u$, and $v$ are differentiable vector-valued functions of $t$ in space, $w$ is a differentiable real-valued function of $t$, and $c$ is a scalar.  
### 12-2-66 $\frac{d}{dt}[\vec r(t)\times\vec r'(t)]=\vec r(t)\times\vec r''(t)$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-2-66.png)
### 12-2-67 $\frac{d}{dt}{\vec r(t)\cdot[\vec u(t)\times\vec v(t)]}=\vec r'(t)\cdot[\vec u(t)\times\vec v(t)]+\vec r(t)\cdot[\vec u'(t)\times\vec v(t)]+\vec r(t)\cdot[\vec u(t)\times\vec v'(t)]$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-2-67.png)

## 12.3 Velocity and Acceleration
### Definitions of Velocity and Acceleration
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-3-Definitions%20of%20Velocity%20and%20Acceleration.png)
### Derivation of the Position Vector for a Projectile
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-3-Derivation%20of%20the%20Position%20Vector%20for%20a%20Projectile.png)
### Position Vector for a Projectile
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-12.3.png)
### 12-3-59 Prove that when an object is traveling at a constant speed, its velocity and acceleration vectors are orthogonal.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-3-59.png)
### 12-3-60 Prove that an object moving in a straight line at a constant speed has an acceleration of 0.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-3-60.png)

## 12.4 Tangent Vectors and Normal Vectors
### Definition of Unit Tangent Vector
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-4-Definition%20of%20Unit%20Tangent%20Vector.png)
### Definition of Principal Unit Normal Vector
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-4-Definition%20of%20Principal%20Unit%20Normal%20Vector.png)
### Alternative Formula for the Principal Unit Normal Vector  
### $$N=\frac{(\vec v\cdot\vec v)\vec a-(\vec v\cdot\vec a)\vec v}{|(\vec v\cdot\vec v)\vec a-(\vec v\cdot\vec a)\vec v|}$$
### Find the Principal Unit Normal Vector
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-4-Find%20the%20Principal%20Unit%20Normal%20Vector.png)
### Acceleration Vector
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-12.4.png)
### Tangential and Normal Components of Acceleration
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-12.5.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-4-74.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-4-75.png)
### 12-4-72 Prove that the principal unit normal vector N points toward the concave side of a plane curve.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-4-72.png)
### 12-4-73 Prove that the vector $T′(t)$ is 0 for an object moving in a straight line.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-4-73.png)

## 12.5 Arc Length and Curvature
### Arc Length
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-12.6.png)
### Definition of Arc Length Function
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-5-Definition%20of%20Arc%20Length%20Function.png)
### Arc Length Parameter
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-12.7.png)
### Curvature
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-5-Curvature.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-12.8.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-12.8-proof.png)
### Curvature in Rectangular Coordinates
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-12.9.png)
### Acceleration, Speed, and Curvature
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-12.10.png)
### SUMMARY OF VELOCITY, ACCELERATION, AND CURVATURE
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/12-5-SUMMARY%20OF%20VELOCITY%2C%20ACCELERATION%2C%20AND%20CURVATURE.png)


# 13 Functions of Several Variables
## 13.1 Introduction to Functions of Several Variables
### Definition of a Function of Two Variables
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-1-Definition%20of%20a%20Function%20of%20Two%20Variables.png)
### 13-1-95 Let $f: R^2\rightarrow R$ be a function such that $f(x, y)+f(y, z)+f(z, x)=0$ for all real numbers $x, y$ and $z$. Prove that there exists a function $g: R\rightarrow R$ such that $f(x,y) = g(x) - g(y)$ for all real numbers $x$ and $y$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-1-95.png)

## 13.2 Limits and Continuity
### Neighborhoods in the Plane
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-2-Neighborhoods%20in%20the%20Plane.png)
### Limit of a Function of Two Variables
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-2-Limit%20of%20a%20Function%20of%20Two%20Variables.png)
### Continuity of a Function of Two Variables
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-2-Continuity%20of%20a%20Function%20of%20Two%20Variables.png)
### Continuous Functions of Two Variables
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-13.1.png)
### Continuity of a Composite Function
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-13.2.png)
### Continuity of a Function of Three Variables
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-2-Continuity%20of%20a%20Function%20of%20Three%20Variables.png)
### 13-2-86 Prove that if $f$ is continuous and $f(a, b)<0$, then there exists a $δ-$neighborhood about $(a, b)$ such that $f(x, y)<0$ for every point $(x, y)$ in the neighborhood.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-2-86.png)

## 13.3 Partial Derivatives
### Partial Derivatives of a Function of Two Variables
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-3-Partial%20Derivatives%20of%20a%20Function%20of%20Two%20Variables.png)
### Notation for First Partial Derivatives
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-3-Notation%20for%20First%20Partial%20Derivatives.png)
### Geometric Interpretation of the Partial Derivatives
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-3-Geometric%20Interpretation%20of%20the%20Partial%20Derivatives.png)
### Higher-Order Partial Derivatives
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-3-Higher-Order%20Partial%20Derivatives.png)
### Equality of Mixed Partial Derivatives
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-13.3.png)

## 13.4 Differentials
### Total Differential
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-4-Total%20Differential.png)
### Differentiability
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-4-Differentiability.png)
### Sufficient Condition for Differentiability
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-13.4.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-13.4-2.png)
Proof: Let $S$ be the surface defined by $z=f(x, y)$ \\
Let $A, B$ and $C$ be points on surface $S$ as shown \\
$$
\begin{aligned}
\Delta z & = f(x+\Delta x, y+\Delta y)-f(x, y) \\
& = [f(x+\Delta x, y+\Delta y) - f(x+\Delta x, y)] + [f(x+\Delta x, y) - f(x, y)]
\end{aligned}
$$
> By the Mean Value Theorem, there is a value $x_1$ between $x$ and $\Delta x$ such that  
> $\Delta z_1 = f(x+\Delta x, y) - f(x, y) = f_x(x_1, y) \Delta x$  
> Similarly, there exists $y_1$ between $y$ and $\Delta y$ such that  
> $\Delta z_2 = f(x+\Delta x, y+\Delta y) - f(x+\Delta x, y) = f_y(x+\Delta x, y_1) \Delta y$  
> Hence, $\Delta z = \Delta z_1 + \Delta z_2 = f_x(x_1, y) \Delta x + f_y(x+\Delta x, y_1) \Delta y$  
> Let $\epsilon_1$ and $\epsilon_2$ be defined as $\epsilon_1 = f_x(x_1, y) - f_x(x, y), \epsilon_2=f_y(x+\Delta x, y_1) - f_y(x, y)$  
> Finally, $\Delta z = \Delta z_1 + \Delta z_2 = [\epsilon_1 + f_x(x, y)]\Delta x + [\epsilon_2+f_y(x, y)]\Delta y = f_x(x, y)\Delta x + f_y(x, y)\Delta y + \epsilon_1 \Delta x + \epsilon_2 \Delta y$  
> Since $\epsilon_1 \rightarrow 0$ and $\epsilon_2 \rightarrow 0$ as $\Delta x \rightarrow 0$ and $\Delta y \rightarrow 0$  
> By definition, $f$ is differentiable.
### Approximation by Differentials
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-4-Approximation%20by%20Differentials.png)
### Differentiability Implies Continuity
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-13.5.png)

## 13.5 Chain Rules for Functions of Several Variables
### Chain Rule:  One Independent Variable
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-13.6.png)
> Proof: $f$ is differentiable, which implies that $\Delta w = \frac{\partial w}{\partial x} \Delta x + \frac{\partial w}{\partial y} \Delta y + \epsilon_1 \Delta x + \epsilon_2 \Delta y$ where $\epsilon_1\rightarrow 0$ and $\epsilon_2\rightarrow 0$ as $(\Delta x, \Delta y)\rightarrow (0, 0)$.  
> So, for $\Delta\neq 0$, $\frac{\Delta w}{\Delta t} = \frac{\partial w}{\partial x} \frac{\Delta x}{\Delta t} + \frac{\partial w}{\partial y} \frac{\Delta y}{\Delta t} + \epsilon_1 \frac{\Delta x}{\Delta t} + \epsilon_2 \frac{\Delta y}{\Delta t}$.  
> Hence, $\frac{dw}{dt} = \lim\limits_{\Delta t\rightarrow 0}\frac{\Delta w}{\Delta t} = \frac{\partial w}{\partial x} \frac{dx}{dt} + \frac{\partial w}{\partial y} \frac{dy}{dt} + O(\frac{dx}{dt}) + O(\frac{dy}{dt}) = \frac{\partial w}{\partial x} \frac{dx}{dt} + \frac{\partial w}{\partial y} \frac{dy}{dt}$.
### Chain Rule: Two Independent Variables
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-13.7.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-13.7-Extension.png)
### Chain Rule:  Implicit Differentiation
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-13.8.png)
### 13-5-53 **Cauchy-Riemann Equations** &emsp; Given the functions $u(x, y)$ and $v(x, y)$, verify that the Cauchy-Riemann equations  
### $\frac{\partial u}{\partial x} = \frac{\partial v}{\partial y}$ and $\frac{\partial u}{\partial y} = -\frac{\partial v}{\partial x}$ can be written in polar coordinate form as $\frac{\partial u}{\partial r} = \frac{1}{\partial r} \cdot \frac{\partial v}{\partial \theta}$ and $\frac{\partial v}{\partial r} = -\frac{1}{\partial r} \cdot \frac{\partial u}{\partial \theta}$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-5-53.png)
### 13-5-55 **Homogeneous Function** &emsp; Show that if $f(x, y)$ is homogeneous of degree $n$, then $xf_x(x, y) + yf_y(x, y) = nf(x, y)$.  
### [Hint: Let $g(t)=f(tx, ty)=t^nf(x, y)$. Find $g′(t)$ and then let $t=1$.]
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-5-55.png)

## 13.6 Directional Derivatives and Gradients
### Directional Derivative
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-6-Directional%20Derivative.png)
### The Gradient of a Function of Two Variables
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-6-The%20Gradient%20of%20a%20Function%20of%20Two%20Variables.png)
### Alternative Form of the Directional Derivative
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-13.10.png)
### Properties of the Gradient
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-13.11.png)
### Gradient Is Normal to Level Curves
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-13.12.png)
### Directional Derivative and Gradient for Three Variables
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-6-Directional%20Derivative%20and%20Gradient%20for%20Three%20Variables.png)

## 13.7 Tangent Planes and Normal Lines
### Tangent Plane and Normal Line to a Surface
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-7-Tangent%20Plane%20and%20Normal%20Line%20to%20a%20Surface.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-7-Tangent%20Plane%20and%20Normal%20Line.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-7-To%20find%20an%20equation%20of%20the%20tangent%20plane.png)
### The Angle of Inclination of a Plane
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-7-The%20Angle%20of%20Inclination%20of%20a%20Plane.png)
### Gradient Is Normal to Level Surfaces
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-13.14.png)
> Proof: 
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-13.14-Proof.png)

## 13.8 Extrema of Functions of Two Variables
### Absolute Extrema and Relative Extrema
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-8-Absolute%20Extrema%20and%20Relative%20Extrema.png)
### Relative Extrema Occur Only at Critical Points
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-13.16.png)
### Second Partials Test
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-13.17.png)

## 13.9 Applications of Extrema
### Least Squares Regression Line
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-13.18.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-9-Simplification.png)

## 13.10 Lagrange Multipliers
### Lagrange’s Theorem
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-13.19.png)
### Method of Lagrange Multipliers
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/13-10-Method%20of%20Lagrange%20Multipliers.png)


# 14 Multiple Integration
## 14.1 Iterated Integrals and Area in the Plane
### Area of a Plane Region
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-1-Area%20of%20a%20Plane%20Region.png)

## 14.2 Double Integrals and Volume
### Double Integrals and Volume of a Solid Region
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-2-Double%20Integrals%20and%20Volume%20of%20a%20Solid%20Region.png)
### Approximating the Volume of a Solid
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-2-Example-1.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-2-Example-1-Extension.png)
### Definition of Double Integral
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-2-Definition%20of%20Double%20Integral.png)
### Evaluation of Double Integrals
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-2-Evaluation%20of%20Double%20Integrals.png)
### Fubini’s Theorem
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-14.2.png)
### Average Value of a Function Over a Region
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-2-Average%20Value%20of%20a%20Function%20Over%20a%20Region.png)
### 14-2-65 **Proof** &emsp; Let $f$ be a continuous function such that $0 \leq f(x, y) \leq 1$ over a region $R$ of area 1. Prove that $0 \leq \int_R\int f(x, y) \leq 1$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-2-65.png)
### 14-2-75 Evaluate $\int_0^a\int_0^be^{max\{b^2x^2, a^2y^2\}}dydx$, where $a$ and $b$ are positive.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-2-75.png)
### 14-2-76 Show that if $\lambda > \frac12$ there does not exist a real-valued function $u$ such that for all $x$ in the closed interval $0\leq x\leq1, u(x)=1+\lambda\int_x^1u(y)u(y-x)dy$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-2-76.png)

## 14.3 Change of Variables:  Polar Coordinates
### Double Integrals in Polar Coordinates
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-3-Double%20Integrals%20in%20Polar%20Coordinates.png)
### Change of Variables to Polar Form
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-14.3.png)
### 14-3-63 **Probability** &emsp; The value of the integral $I=\int_{-\infty}^{\infty}e^{\frac{-x^2}2}dx$ is required in the development of the normal probability density function.  
### (a) Use polar coordinates to evaluate the improper integral.  
### $I^2=\left(\int_{-\infty}^{\infty}e^{\frac{-x^2}2}dx\right)\left(\int_{-\infty}^{\infty}e^{\frac{-y^2}2}dy\right)=\int_{-\infty}^{\infty}\int_{-\infty}^{\infty}e^{\frac{-(x^2+y^2)}2}dA$  
### (b) Use the result of part (a) to determine $I$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-3-63.png)
### 14-3-68 **Area** &emsp; Show that the area $A$ of the polar sector $R$ (see figure) is $A=r\Delta r\Delta \theta$, where $r=\frac{r_1+r_2}2$ is the average radius of $R$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-3-68.png)

## 14.4 Center of Mass and Moments of Inertia
### Mass of a Planar Lamina of Variable Density
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-4-Mass%20of%20a%20Planar%20Lamina%20of%20Variable%20Density.png)
### Moments and Center of Mass
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-4-Moments%20and%20Center%20of%20Mass.png)
### Moments of Inertia
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-4-Moments%20of%20Inertia.png)
### Kinetic Energy
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-4-Kinetic%20Energy.png)
### 14-4-49 ** Proof Prove the following Theorem of Pappus: Let $R$ be a region in a plane and let $L$ be a line in the same plane such that $L$ does not intersect the interior of $R$. If $r$ is the distance between the centroid of $R$ and the line, then the volume $V$ of the solid of revolution formed by revolving $R$ about the line is $V=2\pi rA$, where $A$ is the area of $R$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-4-49.png)

## 14.5 Surface Area
### Definition of Surface Area
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-5-Surface%20Area.png)
### 14-5-37 Find the surface area of the solid of intersection of the cylinders $x^2+z^2=1$ and $y^2+z^2=1$(see figure).
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-5-37.png)
### 14-5-38 Show that the surface area of the cone $z=k\sqrt{x^2+y^2}, k>0$, that lies above the circular region $x^2+y^2\leq r^2$ in the $xy-$plane is $\pi r^2\sqrt{k^2+1}$(see figure).
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-5-38.png)

## 14.6 Triple Integrals and Applications
### Triple Integrals
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-6-Triple%20Integrals.png)
### Center of Mass and Moments of Inertia
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-6-Center%20of%20Mass%20and%20Moments%20of%20Inertia.png)
### 14-6-73 Evaluate $\lim\limits_{n\rightarrow\infty}\int_0^1\int_0^1···\int_0^1\cos^2{\frac{\pi}{2n}(x_1+x_2+...+x_n)}dx_1dx_2···dx_n$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-6-73.png)

## 14.7 Triple Integrals in Other Coordinates
### Triple Integrals in Cylindrical Coordinates
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-7-Triple%20Integrals%20in%20Cylindrical%20Coordinates.png)
### Triple Integrals in Spherical Coordinates
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-7-Triple%20Integrals%20in%20Spherical%20Coordinates.png)
### 14-7-47 Find the volume of the region of points (x, y, z) such that $(x^2+y^2+z^2+8)^2\leq 36(x^2+y^2)$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-7-47.png)

## 14.8 Change of Variables: Jacobians
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-8-Jacobians.png)
### Change of Variables for Double Integrals
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-14.5.png)
### 14-8-41 Let $A$ be the area of the region in the first quadrant bounded by the line $y=\frac12x$, the x-axis, and the ellipse $\frac19x^2+y^2=1$. Find the positive number $m$ such that $A$ is equal to the area of the region in the first quadrant bounded by the line $y=mx$, the y-axis, and the ellipse $\frac19x^2+y^2=1$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-8-41.png)

## Problem Solving
### 14-PS-1 **Volume** &emsp; Find the volume of the solid of intersection of the three cylinders $x^2+z^2=1, y^2+z^2=1$ and $x^2+y^2=1$(see figure).
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-PS-1.png)
### 14-PS-2 **Surface** &emsp; Area Let and be positive real numbers. The first octant of the plane $ax+by+cz=d$ is shown in the figure. Show that the surface area of this portion of the plane is equal to $\frac{A(R)}{c}\sqrt{a^2+b^2+c^2}$ where $A(R)$ is the area of the triangular region $R$ in the $xy-$plane, as shown in the figure.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-PS-2.png)
### 14-PS-4 Prove that $\lim\limits_{n\rightarrow\infty}\int_0^1\int_0^1x^ny^ndxdy=0$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-PS-4.png)
### 14-PS-5 **Deriving a Sum** &emsp; Derive Euler’s famous result that was mentioned in Section 9.3, $\sum\limits_{n=1}^{\infty}\frac1{n^2}=\frac{\pi^2}6$ by completing each step.  
### (a) Prove that $\int\frac{dv}{2-u^2+v^2}=\frac1{\sqrt{2-u^2}}\arctan\frac{v}{2-u^2}+C$.  
### (b) Prove that $I_1=\int_0^{\frac{\sqrt{2}}{2}}\int_{-u}^{u}\frac2{2-u^2+v^2}dvdu=\frac{\pi^2}{18}$ by using the substitution $u=\sqrt{2}\sin\theta$.
### (c) Prove that $I_2=\int_{\frac{\sqrt{2}}{2}}^{\sqrt{2}}\int_{u-\sqrt2}^{-u+\sqrt2}\frac2{2-u^2+v^2}dvdu=4\int_{\frac{\pi}6}^{\frac{\pi}2}\arctan\frac{1-\sin\theta}{\cos\theta}d\theta$ by using the substitution $u=\sqrt2\sin\theta$.  
### (d) Prove the trigonometric identity $\frac{1-\sin\theta}{\cos\theta}=\tan\left(\frac{\frac{\pi}2-\theta}{2}\right)$.  
### (e) Prove that $I_2=\int_{\frac{\sqrt{2}}{2}}^{\sqrt{2}}\int_{u-\sqrt2}^{-u+\sqrt2}\frac2{2-u^2+v^2}dvdu=\frac{\pi^2}9$.  
### (f) Use the formula for the sum of an infinite geometric series to verify that $\sum\limits_{n=1}^{\infty}\frac1{n^2}=\int_0^1\int_0^1\frac1{1-xy}dxdy$.  
### (g) Use the change of variables $u=\frac{x+y}{\sqrt2}$ and $v=\frac{y-x}{\sqrt2}$ to prove that $\sum\limits_{n=1}^{\infty}\frac1{n^2}=\int_0^1\int_0^1\frac1{1-xy}dxdy=I_1+I_2=\frac{\pi^2}{6}$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-PS-5.png)
### 14-PS-8 **Volume** &emsp; Show that the volume of a spherical block can be approximated by $\Delta V\approx \rho^2\sin\phi\Delta\rho\Delta\phi\Delta\theta$.
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/14-PS-8.png)


# 15 Vector Analysis
## 15.1 Vector Fields
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-1-Vector%20Fields.png)
### Inverse Square Field
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-1-Inverse%20Square%20Field.png)
### Conservative Vector Fields
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-1-Conservative%20Vector%20Fields.png)
### Test for Conservative Vector Field in the Plane
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-15.1.png)
### Curl of a Vector Field
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-1-Curl%20of%20a%20Vector%20Field.png)
### Test for Conservative Vector Field in Space
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-15.2.png)
### Divergence of a Vector Field
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-1-Divergence%20of%20a%20Vector%20Field.png)
### Divergence and Curl
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-15.3.png)
### 15-1-77 **Proof** In parts $(a)–(h)$, prove the property for vector fields $F$ and $G$ and scalar function $f$. (Assume that the required partial derivatives are continuous.)  
### (a) $curl(F+G)=curl F+curl G  
### (b) $curl(\nabla f)=\nabla\times(\nabla f)=0$  
### (c) $div(F+G)=div F + div G$  
### (d) $div(F\times G)=(curl F)\cdot G-F\cdot(curl G)$  
### (e) $\nabla\times[\nabla f+(\nabla\times F)]=\nabla\times(\nabla\times F)$  
### (f) $\nabla\times(fF)=f(\nabla\times F)+(\nabla f)\times F$  
### (g) $div(f F)=f div F+\nabla f\cdot F$  
### (h) $div(curl F)=0$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-1-77.png)

## 15.2 Line Integrals
### Piecewise Smooth Curves
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-2-Piecewise%20Smooth%20Curves.png)
### Line Integrals
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-2-Line%20Integrals.png)
### Line Integrals of Vector Fields
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-2-Line%20Integrals%20of%20Vector%20Fields.png)
### Line Integrals in Differential Form
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-2-Line%20Integrals%20in%20Differential%20Form.png)

## 15.3 Conservative Vector Fields and Independence of Path
### Fundamental Theorem of Line Integrals
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-15.5.png)
### Independence of Path
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-15.6.png)
### Equivalent Conditions
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-15.7.png)
### Conservation of Energy
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-3-Conservation%20of%20Energy.png)

## 15.4 Green’s Theorem
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-15.8.png)
### Line Integral for Area
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Theorem-15.9.png)
### Alternative Forms of Green’s Theorem
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-4-Alternative%20Forms%20of%20Green%E2%80%99s%20Theorem.png)

## 15.5 Parametric Surfaces
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-5-Parametric%20Surfaces.png)
### Normal Vectors and Tangent Planes
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-5-Normal%20Vectors%20and%20Tangent%20Planes.png)
### surface of revolution
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-5-Surface%20of%20revolution.png)
### 15-5-58 **Surface Area** &emsp; Let $f$ be a nonnegative function such that $f'$ is continuous over the interval $[a, b]$. Let $S$ be the surface of revolution formed by revolving the graph of $f$, where $a\leq \leq b$, about the $x-$axis. Let $x=u, y=f(u)\cos v$ and $z=f(u)\sin v$, where $a\leq u\leq b$ and $0\leq v \leq 2\pi$. Then, $S$ is represented parametrically by $r(u, v)=u\vec i+f(u)\cos v\vec j+f(u)\sin v\vec k$. Show that the following formulas are equivalent.  
### Surface area = $2\pi\int_a^b f(x)\sqrt{1+[f'(x)]^2}dx$  
### Surface area = $\int_D\int |\vec r_u\times\vec r_v|dA$
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-5-58.png)

## 15.6 Surface Integrals
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-6-Surface%20Integrals.png)
### Parametric Surfaces and Surface Integrals
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-6-Parametric%20Surfaces%20and%20Surface%20Integrals.png)
### Orientation of a Surface
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-6-Orientation%20of%20a%20Surface.png)
### Flux Integrals
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-6-Flux%20Integrals.png)
### Gauss’s Law
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-6-Gauss%E2%80%99s%20Law.png)
### SUMMARY OF LINE AND SURFACE INTEGRALS
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-6-SUMMARY%20OF%20LINE%20AND%20SURFACE%20INTEGRALS.png)

## 15.7 Divergence Theorem
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-7-Divergence%20Theorem.png)
### The Finite Unions of Simple Solid Regions
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-7-The%20Finite%20Unions%20of%20Simple%20Solid%20Regions.png)
### Flux and the Divergence Theorem
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-7-Flux%20and%20the%20Divergence%20Theorem.png)

## 15.8 Stokes’s Theorem
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-8-Stokes%E2%80%99s%20Theorem.png)
### Physical Interpretation of Curl
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-8-Physical%20Interpretation%20of%20Curl.png)
### SUMMARY OF INTEGRATION FORMULAS
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/15-8-SUMMARY%20OF%20INTEGRATION%20FORMULAS.png)






## Integration Tables
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Integration-Tables-1.png) 
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Integration-Tables-2.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Integration-Tables-3.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Integration-Tables-4.png)
![avatar](Images/Ron%20Larson%20and%20Bruce%20Edwards/Integration-Tables-5.png)
