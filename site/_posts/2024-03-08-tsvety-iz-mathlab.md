---
layout: post
title: "Цветы из Mathlab"
date: 2024-03-08T14:01:12+00:00
author: "Yury Novozhilov"
source: vk
original_url: https://vk.com/wall-97265142_2664
images:
  - url: "/assets/images/2664.jpg"
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
