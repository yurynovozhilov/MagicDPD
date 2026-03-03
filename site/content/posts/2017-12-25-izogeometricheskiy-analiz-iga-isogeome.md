---
layout: post
title: "Изогеометрический анализ (#IGA, isogeometric analysis) - это"
date: 2017-12-25T17:11:21+00:00
author: "GlukRazor"
source: vk
original_url: https://vk.com/wall-97265142_676
tags:
  - implicit
  - explicit
---

Если кратко, то благодаря использованию особых функций форм и гладкой аппроксимации геометрия решение задачи также получается более гладким, хотя это сказывается на ресурсоемкости задачи.

И да, конечно же этот метод уже реализован в LS-DYNA (смотри *ELEMENT_SOLID_NURBS_PATCH + *SECTION_SOLID ELFORM=201), а специфические сетки умеет строить бесплатный LSPP (смотри FEM>Element and Mesh>NURBS 3D Editing). Метод применим как для #explicit, так и для #implicit расчетов и даже для поиска собственных частот.

http://ift.tt/2DcECzoMediaMedia💾 03_Montanari_University_of_Oxford.pdf

http://ift.tt/2DbfSrp
