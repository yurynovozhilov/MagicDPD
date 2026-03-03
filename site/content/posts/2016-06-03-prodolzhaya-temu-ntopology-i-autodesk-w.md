---
layout: post
title: "Продолжая тему #nTopology и #Autodesk #Within вспомним про м"
date: 2016-06-03T07:00:29+00:00
author: "GlukRazor"
source: vk
tags:
  - topology
  - Altair
  - optimization
  - nTopology
  - Within
  - Autodesk
  - OptiStruct
  - lattice
images:
  - url: "/assets/images/1727.jpg"
  - url: "/assets/images/1727.jpg"
---

Продолжая тему #nTopology и #Autodesk #Within вспомним про монстра оптимизации #Altair #OptiStruct. В 14-ой версии OptiStruct получил возможность создавать пористые конструкции на основе результатов топологической оптимизации (#lattice structures или lattice optimization).

Система работает так: проводится топологическая оптимизация и из ее результатов извлекается геометрия по изоповерхности псевдоплотности, скажем, 0.5. Далее все элементы с псевдоплотностью, скажем, от 0.5 до 0.8 заменяются пространственной сеткой из балочных элементов, толщины которых подбираются отдельно или на основе данных распределения псевдоплотности.

#Altair говорит, что пока этот подход имеет сильную сеточную зависимость. Надеюсь они ее скоро победят.

[OptiStruct Analysis and Optimization](http://www.altairhyperworks.com/product/OptiStruct/New-Features)
