---
title: "Homework 6"
author: 
    - Vikram Bhagavatula
date: Feb 18, 2022
documentclass: article
---
\newpage

# Code
```{.python include="./src/hw6.py"}
```

\newpage
# Harris Corner Detector

For each of the images, a $k=0.05$ for the CRF was used, and the 300 best points (highest CRF) was plotted on the pictures.
Most of the corresponding points were detected in each of the images, with some issues for the points on the checkerboard
near the android (present in one image, absent in the other).

![Left image corners](./src/left-result.png)

![Right image corners](./src//right-result.png)



\newpage
# Gaussian and Laplacian Pyramids

![Gaussian Pyramid, Level 0](./src/level0.png)

![Gaussian Pyramid, Level 1](./src/level1.png){width=50%, height=50%}

![Gaussian Pyramid, Level 2](./src/level2.png){width=25%, height=25%}

![Gaussian Pyramid, Level 3](./src/level3.png){width=12.5%, height=12.5%}

![Laplacian Pyramid, Level 1](./src/lp1.png)

![Laplacian Pyramid, Level 2](./src/lp2.png){width=50%, height=50%}

![Laplacian Pyramid, Level 3](./src/lp3.png){width=25%, height=25%}

![Laplacian Pyramid, Level 4](./src/lp4.png){width=12.5%, height=12.5%}
