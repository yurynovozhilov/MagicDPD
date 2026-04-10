---
author: GlukRazor
date: 2016-04-26 08:00:41+00:00
layout: post
link_previews:
- description: 'FSI case for LS-DYNA ICFD and LS-DYNA Implicit coupling. Wave maker
    simulation.You could download input deck here: https://vk.com/wall-97265142_1604'
  image: https://i.ytimg.com/vi/w5ddrjcVbnM/maxresdefault.jpg
  title: Wave maker in LS-DYNA ICFD
  url: https://www.youtube.com/watch?v=w5ddrjcVbnM
source: vk
tags:
- Implicit
- CFD
- ICFD
- FSI
- LSD
- mdpd
- freesurface
title: 'Еще одни выходные - еще один этап самообучения по теме #CFD в LS-DYNA.'
---

На этот раз я решали простейшую задачу #FSI моделирующую работы некого волнопродуктора.

В бассейне со свободной поверхностью задается колебательное движение одной стенки. Стенка принимается недеформируемой, а жидкость - несжимаемой. При этом, так как сетка у меня все равно очень плохая, то на всех границах домена ставлю скольжение. Колебания стенки рассчитываются неявным решателем, что бы не мельчить шаг по времени.

P.S. Такой простой настройки FSI я еще не видел 😊

[Wave maker in LS-DYNA ICFD](https://www.youtube.com/watch?v=w5ddrjcVbnM)
