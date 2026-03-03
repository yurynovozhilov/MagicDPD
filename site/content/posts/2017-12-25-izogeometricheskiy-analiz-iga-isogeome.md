---
layout: post
title: "Изогеометрический анализ (#IGA, isogeometric analysis) - это"
date: 2017-12-25T17:11:21+00:00
author: "GlukRazor"
source: vk
tags:
  - explicit
  - implicit
  - IGA
  - FEM
---

Изогеометрический анализ (#IGA, isogeometric analysis) - это один из перспективных методов выполнения расчетов для случаев, когда не происходит разрушения материала . Преимущества данного метода перед традиционным #FEM подробно пописаны а прилагаемой статье.

Если кратко, то благодаря использованию особых функций форм и гладкой аппроксимации геометрия решение задачи также получается более гладким, хотя это сказывается на ресурсоемкости задачи.

И да, конечно же этот метод уже реализован в LS-DYNA (смотри *ELEMENT_SOLID_NURBS_PATCH + *SECTION_SOLID ELFORM=201), а специфические сетки умеет строить бесплатный LSPP (смотри FEM>Element and Mesh>NURBS 3D Editing). Метод применим как для #explicit, так и для #implicit расчетов и даже для поиска собственных частот.

http://ift.tt/2DcECzoMediaMedia💾 03_Montanari_University_of_Oxford.pdf

http://ift.tt/2DbfSrp

http://ift.tt/2wHGYaz
http://ift.tt/2vBgpQ1
http://ift.tt/2zoReD2
http://ift.tt/2C1oh1f
http://ift.tt/2C2h6G0
http://ift.tt/2D8SBqb
http://ift.tt/2C1oiCl
ttp://ift.tt/2DbfSrp
