#lang racket

; normal-order
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
    (remainder (remainder 206 40) (remainder 40 (remainder 206 40)))               ; remainder + 4
    (gcd (remainder (remainder 40 (remainder 206 40)) (remainder (remainder 206 40) (remainder 40 (remainder 206 40))))
         (remainder (remainder (remainder 206 40) (remainder 40 (remainder 206 40))) (remainder (remainder 40 (remainder 206 40)) (remainder (remainder 206 40) (remainder 40 (remainder 206 40)))))))
