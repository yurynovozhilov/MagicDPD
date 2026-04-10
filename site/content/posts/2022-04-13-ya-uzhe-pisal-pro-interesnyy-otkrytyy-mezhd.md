---
author: MagicDPD
date: 2022-04-13 17:00:14+00:00
images:
- url: /assets/images/2216.jpg
layout: post
link_previews:
- description: 'In this webinar, Coreform will introduce two MOOSE-related projects
    they have been working on for the past few years: adding isogeometric analysis
    (IGA) to M...'
  image: https://i.ytimg.com/vi/UmS-pAuBnEU/maxresdefault.jpg
  title: Improving MOOSE workflows through Coreform Cubit
  url: https://www.youtube.com/watch?v=UmS-pAuBnEU
source: vk
tags:
- IGA
- MOOSE
- Coreform
- Cubit
- opensource
title: Я уже писал про интересный открытый междисциплинарный решатель "Лось" (#MOOSE
  или Multiphysics Object-Oriented Simulation Environment).
---

Так вот, в нем теперь есть поддержка #IGA, и это все стало возможным благодаря совместному проекту с командой  #Coreform #Cubit.

Для тех, кто еще не знает, что такое IGA, то данный подход подразумевает использование одной и той же гладкой сплайновой основы для определения геометрии и моделирования. Это дает более точные результаты, особенно на сравнительно грубых сетках: геометрия оказывается точно описанной при любом качестве сетки, оболочечные элементы могут сгибаться не только в узлах, а иногда нам требуется меньше степеней свободы для получения точного результата расчета. А еще там есть моя мечта - техника погружденных Solid IGA элементов, которая может навсегда решить проблемы с генерацией сложных сеток.

#opensource https://youtu.be/UmS-pAuBnEU

[Improving MOOSE workflows through Coreform Cubit](https://youtu.be/UmS-pAuBnEU)
