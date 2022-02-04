---
title: "Homework 3"
author: 
    - Vikram Bhagavatula
date: Jan 18, 2022
documentclass: article
---
\newpage

# Responses

## Part 1

@. The coordinates of the pixels in *I* and the corresponding coordinates in *S*:

$$
\begin{tabular}{llll}
Pixels in I & Pixels in S \\
\hline
 (995.34415584, 452.48701299) & (949.88961039, 379.75974026) \\
 (1177.16233766,  466.77272727) & (1166.77272727,  379.75974026) \\
 (1122.61688312,  827.81168831) & (1168.07142857,  779.75974026) \\
 (952.48701299, 775.86363636) & (952.48701299, 775.86363636) \\
\hline
\end{tabular}
$$


@. The computed homography matrix:

$$
H = 
\begin{bmatrix}
 4.85941    &  0.462755    & -2609.68  \\
 0.359903   &  3.02517     &  -752.982 \\
 0.00157388 & -3.34932*10^{-6} &     1     \\
\end{bmatrix}
$$

@. The synthesized new image:

![](./program/Result-pt1.png)

\newpage
@. The code for computing *H*:

```{.python include="./program/hw3.py" startLine=17 endLine=48}
```

\newpage
@. The code for synthesizing view *S* from *I*:

```{.python include="./program/hw3.py" startLine=63 endLine=89}
```

\newpage

## Part 2


Given the following images (first is the *left image*, the second is the *right image*):

![Left Image](./program/Source-pt2a-p1.png){width=350px}

![Right Image](./program/Target-pt2a-p1.png){width=350px}

@. Corresponding points, going from the left image to the right image:

$$
\begin{tabular}{ll}
Left Image & Right Image \\
\hline
 (995.61526521, 451.5774848)    & (1034.09530369,  448.77893655) \\
 (615.01270279, 677.56025624)   & (1147.43650794,  451.5774848, ) \\
 (1176.12162753,  467.66913726) & (1132.74412961,  671.26352267)  \\
 (1123.64884779,  833.57932135) & (1016.6043771,   658.67005553)  \\
 (946.64067078, 777.60835629)   & (742.3466483,  427.09018759)  \\
 (658.39020071, 429.88873584)   & (845.1932966,  433.38692116)  \\
 (759.83757488, 436.88510648)   & (827.00273296, 641.17912895)  \\
 (711.56261752, 706.9450129)  & (726.95463291, 628.58566181) \\
\hline
\end{tabular}
$$

The first group of points correspond to the points on the rightmost window, going counterclockwise and starting from the base of the window.
The second group of points correspond to the points to the left of the rightmost window, going counterclockwise and starting from the base of the window.

@. The *H* matrix for this pairing of images:

$$
H =
\begin{bmatrix}
 3.14393    & 0.467904    & -758.239 \\
 0.597277   & 1.80354     & -297.528 \\
 0.00136422 & 0.000314106 &    1     \\
\end{bmatrix}
$$

@. Applying the transformation *H* to the left image, we get:

![Result](./program/Result-pt2a-p1.png)



\newpage
Given the following images (first is the *left image*, the second is the *right image*):

![Left Image](./program/Source-pt2-p2.png){width=350px}

![Right Image](./program/Target-pt2-p2.png){width=350px}

@. Corresponding points, going from the left image to the right image:

$$
\begin{tabular}{llllllll}
Left Image & Right Image \\
\hline
 (1034.09530369,  445.9803883, ) & (995.61526521, 452.97675893)   \\
 (1148.136145,    452.97675893) & (1173.32307928,  469.76804845) \\
 (1132.04449254,  669.86424855) & (1123.64884779,  834.27895842) \\
 (1018.70328829,  659.3696926, ) & (948.0399449,  776.90871923)   \\
 (740.24773711, 427.09018759) & (660.4891119,  429.18909878) \\
 (841.69511129, 432.6872841, ) & (757.03902663, 436.88510648) \\
 (822.80491058, 640.47949189) & (712.96189164, 707.64464996) \\
 (728.35390704, 629.98493594) & (613.61342866, 675.46134505) \\
\hline
\end{tabular}
$$

The first group of points correspond to the points on the rightmost window, going clockwise and starting from the top of the window.
The second group of points correspond to the points to the left of the rightmost window, going clockwise and starting from the top of the window.

@. The *H* matrix for this pairing of images:
$$
H = 
\begin{tabular}{rrr}
\hline
  0.333592    & -0.166823    & 250.993 \\
 -0.180262    &  0.721422    & 103.284 \\
 -0.000413672 & -0.000107973 &   1     \\
\hline
\end{tabular}
$$

\newpage
@. Applying the transformation, we get:

![Result](./program/Result-pt2-p2.png)


\newpage
Given the following images (first is the *left image*, the second is the *right image*):

![Left Image](./program/Source-pt2-p3.png){width=350px}

![Right Image](./program/Target-pt2-p3.png){width=350px}

@. Corresponding points, going from the left image to the right image:

$$
\begin{tabular}{llll}
Left Image & Right Image \\
\hline
 (2433.62121212,  510.53030303) & (616.70238095,  97.78571429)   \\
 (3805.13636364,  571.59090909) & (834.26190476, 216.80357143)   \\
 (3866.1969697,  1139.92424242) & (849.61904762, 360.13690476)   \\
 (2400.74242424, 1078.86363636) & (619.26190476, 266.71428571)   \\
\hline
\end{tabular}
$$

The first group of points correspond to the points on the rightmost window, going clockwise and starting from the top of the window.
The second group of points correspond to the points to the left of the rightmost window, going clockwise and starting from the top of the window.


@. The *H* matrix for this pairing of images:

$$
\begin{bmatrix}
 0.468784    &  0.0228442   & -153.76  \\
 0.174208    &  0.486466    & -513.948 \\
 0.000255376 & -3.90818e-06 &    1     \\
\end{bmatrix}
$$

@. Applying the transformation, we get:

![Result](./program/Result-pt2-p3.png)


Given the following images (first is the *left image*, the second is the *right image*):

![Left Image](./program/Target-pt2-p3.png){width=350px}

![Right Image](./program/Source-pt2-p3.png){width=350px}

@. Corresponding points, going from the left image to the right image:

$$
\begin{tabular}{llll}
Left Image & Right Image \\
\hline
 (616.70238095, 101.625)      & (2438.31818182,  524.62121212) \\
 (835.54166667, 219.36309524) & (3795.74242424,  566.89393939) \\
 (849.61904762, 360.13690476) & (3875.59090909, 1111.74242424) \\
 (623.10119048, 265.43452381) & (2414.83333333, 1074.16666667) \\
\hline
\end{tabular}
$$

@. The *H* matrix for this pairing of images:

$$
H = 
\begin{bmatrix}
  2.82883     & -0.495605    &   53.6439 \\
 -1.39854     &  2.3338      & 1001.37   \\
 -0.000442775 & -9.96218e-05 &    1      \\
\end{bmatrix}
$$

@. Applying the transformation, we get:

![Result](./program/Result-pt2-p4.png)
