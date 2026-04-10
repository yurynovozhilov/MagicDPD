---
author: Yury Novozhilov
date: 2024-03-08 14:01:12+00:00
images:
- url: /assets/images/2664.jpg
layout: post
link_previews:
- description: "Use this MATLAB code to make a rose with the jet colormap \U0001F339
    \n\nn=800;\np=pi;\n[R,T]=ndgrid(linspace(0,1,n),linspace(-2,20*p,n));\nx=1-(.5)*((5/4)*(1-mod(3.6*T,2*p)/p).^2-.25).^2;\nU=2*exp(-T/(8*p));\nL=sin(U);\nJ=cos(U);\ny=1.99*(R.^2).*(1.2*R-1).^2.*L;\nK=x.*(R.*L+y.*J);\nX=K.*sin(T);\nY=K.*cos(T);\nZ=x.*(R.*J-y.*L);\nsurf(X,Y,Z,"
  image: https://media.licdn.com/dms/image/v2/D4E10AQGNv2Jc24-7wg/image-shrink_1280/image-shrink_1280/0/1706198401072?e=2147483647&v=beta&t=8zm6BeQ0ZoecJuSmQQq9RhZBTbCqbET1PdYZe6fYyqk
  title: "Use this MATLAB code to make a rose with the jet colormap \U0001F339… |
    MathWorks | 32 comments"
  url: https://www.linkedin.com/posts/the-mathworks_2_use-this-matlab-code-to-make-a-rose-with-activity-7156314780486541312-HZGY
source: vk
title: Цветы из Mathlab
---

n=800;
p=pi;
[R,T]=ndgrid(linspace(0,1,n),linspace(-2,20*p,n));
x=1-(.5)*((5/4)*(1-mod(3.6*T,2*p)/p).^2-.25).^2;
U=2*exp(-T/(8*p));
L=sin(U);
J=cos(U);
y=1.99*(R.^2).*(1.2*R-1).^2.*L;
K=x.*(R.*L+y.*J);
X=K.*sin(T);
Y=K.*cos(T);
Z=x.*(R.*J-y.*L);
surf(X,Y,Z,'LineStyle','none')
grid,axis off;
colormap(jet)

https://www.linkedin.com/posts/the-mathworks_2_use-this-matlab-code-to-make-a-rose-with-activity-7156314780486541312-HZGY

https://www.linkedin.com/posts/the-mathworks_2_use-this-matlab-code-to-make-a-rose-with-activity-7156314780486541312-HZGY
