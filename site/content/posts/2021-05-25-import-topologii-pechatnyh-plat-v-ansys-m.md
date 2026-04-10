---
author: MagicDPD
date: 2021-05-25 17:01:47+00:00
layout: post
link_previews:
- description: Please subscribe to our new Channel. New videos will be posted herehttps://www.youtube.com/channel/UC34GHDwqDux32A2GZ_MDIMASometimes
    modeling dozens of layer...
  image: https://i.ytimg.com/vi/EBpKi7Oq6dw/maxresdefault.jpg
  title: 'Ansys Mechanical: Shell trace mapping'
  url: https://www.youtube.com/watch?v=EBpKi7Oq6dw
source: vk
tags:
- odb
- lsdyna
- em
- ansys
- tracemapping
- mechanical
title: Импорт топологии печатных плат в Ansys Mechanical и LS-DYNA
---

https://www.youtube.com/watch?v=EBpKi7Oq6dw




Демонстрация активно развиваемой функции trace mapping из Ansys Mechanical, которая пригодится при механических и тепловых расчетах печатных плат. Итак, trace mapping позволяет импортировать структуру печатной платы из ODB++. Далее эта структура передается в препроцессор, где отображается геометрической положение того или иного материала в пространстве. После того как материалу или "сущности" из ODB++ выставляются соответствие его механический эквивалент (грубо говоря - дорожка должны быть медные) препроцессор "намазывает" эти свойства на модель состоящую из слоистых оболочек. Не надо прорисовывать многие сотни, если не тысячи объектов, не надо портить геометрию и усложнять работу сеточного генератора, не надо возиться с solid моделью платы - все данные переносятся автоматом на уровне сетки. Если же сетку надо будет перестроить, то и данные из ODB++ будут автоматически применены к новым элементам. Кстати, в актуальной версии 2021R1, trace mapping работает и для Workbench LS-DYNA, а значит одна модель печатной платы может быть использована и для расчета тепла, и для расчёта прочности и для случая удара.

#ansys #em #lsdyna #mechanical #odb #tracemapping
https://tinyurl.com/ygnyywsn

[Ansys Mechanical: Shell trace mapping](https://www.youtube.com/watch?v=EBpKi7Oq6dw)
https://tinyurl.com/ygnyywsn
