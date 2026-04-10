---
layout: post
title: "MAT_GENERALIZED_PHASE_CHANGE"
date: 2019-06-25T17:00:25+00:00
author: "GlukRazor"
source: vk
images:
  - url: "/assets/images/1515.jpg"
---

Эта модель материала появилась в 11-ой версии LS-DYNA, и как-то долго оставалась незамеченной мной, а зря. Прежде всего модель позволяет отслеживать до 24-х фаз в металле, подвергающемуся тепловому воздействию (сварка, прокатка, штамповка, 3D печать и т.д.).







JMAK = Johnson-Mehl-Avrami-Kolmogorov







Но просто фазами тут все не ограничивается: надо смотреть на результаты, предоставляемые моделью. Немного поколдовав с картой DATABASE_EXTENT_BINARY, можно заказать для shell/solid вывод следующих дополнительных результатов.







Нет, вы это видите: распределение размера зерна, предела текучести, модуля упругости по объему тела!!!



Дополнительные статьи по теме:



https://www.dynalook.com/conferences/12th-european-ls-dyna-conference-2019/ls-dyna-on-demand/merten_dynamore.pdf/view



https://www.dynalook.com/conferences/12th-european-ls-dyna-conference-2019/ls-dyna-on-demand/merten_dynamore.pdf/view

https://www.dynalook.com/conferences/12th-european-ls-dyna-conference-2019/ls-dyna-on-demand/merten_dynamore.pdf/view
https://www.dynalook.com/conferences/12th-european-ls-dyna-conference-2019/ls-dyna-on-demand/merten_dynamore.pdf/view
