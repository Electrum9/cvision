---
title: "Homework 5"
author: 
    - Vikram Bhagavatula
date: Feb 05, 2022
documentclass: article
---
\newpage

# Code

[Code repository (click on text)](https://github.com/Electrum9/cvision/tree/main/hw5/src).

```{.python include="./src/hw5.py"}
```


\newpage
# Responses

@. The fundamental matrix computed between the left and right image:

$$
\begin{bmatrix}
 9.45781783e-06 &  2.42273731e-05 & -1.10184261e-02 \\
-1.76093034e-05 &  8.61231351e-06 & -6.28255876e-03 \\
 7.12348483e-03 & -3.93744237e-04 &  1.00000000e+00 \\
\end{bmatrix}
$$

@. Example outputs:

![Checkerboard at (410, 199)](./src/checkerboard.png)

![Android at (191, 312)](./src/android.png)

\newpage
@. Homography

- Matrix:

$$
\begin{bmatrix}
0.448719   & 0.0377775   & 104.207  \\
0.0416049  & 0.835691    & -10.2412 \\
-0.00100847 & 0.000526905 &   1      \\
\end{bmatrix}
$$

- Points:

Left Points                         Right Points
---------------------------         -----------------------------
(147.09922457, 63.96668707)         (195.6452913, 55.25329048)
(182.26400367, 63.96668707)         (220.85190287, 59.92118151)
(413.4802061, 267.48673605)         (415.03616978, 320.07830834)
(438.68681767, 265.3083869)         (445.22186512, 327.85812672)
(220.85190287, 137.0969799)         (245.12493623, 133.67385981)
(251.34879094, 135.22982349)        (272.19870421, 139.27532905)
(353.42000816, 204.31461075)        (358.39909193, 231.077186)
(380.49377615, 201.51387614)        (392.63029283, 242.28012448)

- Examples:

![Original Image](./src/left.jpg)

![Target Image](./src/right.jpg)

![Generated Image](./src/better_homography_left_right.png)
