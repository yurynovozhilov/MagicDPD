---
author: GlukRazor
date: 2016-04-19 07:02:16+00:00
layout: post
link_previews:
- description: 'You could download input deck here: https://vk.com/wall-97265142_1584'
  image: https://i.ytimg.com/vi/VI7Gd3Zo5iU/hqdefault.jpg
  title: Water Column Collapse in LS-DYNA ICFD
  url: https://www.youtube.com/watch?v=VI7Gd3Zo5iU
source: vk
tags:
- CFD
- MPP
- ICFD
- LSDYNA
- freesurface
title: 'Я наконец смог посчитать #CFD задачу со свободной поверхностью в #LSDYNA #ICFD.'
---

Использовал слегка модифицированную постановку Sunao Tokura из стати "Validation of Fluid Analysis Capabilities in LS-DYNA Based on Experimental Result". Получилось неплохо. Есть несколько тонкостей:
- на задачах со свободной поверхностью пристеночные слои глючат
- граничные условия прилипания в такой задаче тоже не очень адекватны для грубой сетки
- расчет идет быстро и стабильно, заметно быстрее чем ALE
- второй фазой может быть только вакуум - никакой поддержки полноценной многофазности пока нет
- кажется, что решатель не очень любит регулярную треугольную сетку на стенках домена.

И да, вам потребуется LS-DYNA #MPP, если хотите использовать более 1 ядра на расчет. Для этого пригодится такая командная строка (я использовал LS-DYNA R8.1:

"%AWP_ROOT170%\commonfiles\MPI\Platform\9.1.3.1\winx64\bin\mpirun.exe" -v -np 4 mppdyna.exe i=water_column_collapse_main.k

[Water Column Collapse in LS-DYNA ICFD](https://www.youtube.com/watch?v=VI7Gd3Zo5iU)
