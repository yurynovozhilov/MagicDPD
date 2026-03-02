---
date: 2018-01-31 17:01:05+00:00
images:
- url: /assets/images/757.jpg
link_previews:
- description: LS-DYNA now provide the high order element (H27) both for explicit
    and implicit method. This video show the way to generate the H27 element in LS-PrePost
  image: https://i.ytimg.com/vi/0U1rkt8MX6M/hqdefault.jpg
  title: How to generate the H27
  url: https://www.youtube.com/watch?v=0U1rkt8MX6M
original_url: https://t.me/MagicDPD/757
source: tg
title: Делаем 27-ми узловые элементы в LS-PrePost
---

Малюсенький видеоурок, показывающий как построить 27 узловые Solid элементы в LS-PrePost для дальнейшего расчета в LS-DYNA.

А для тех из вас, кому лень возиться с перестроением сетки, в LS-PrePost есть возможность заставить сам решатель в начале расчета перестроить обычные 8-ми узловые Solid элементы в новые 27-ми узловые, просто заменив заголовок карты *ELEMENT_SOLID на *ELEMENT_SOLID_H8TOH27.

https://www.youtube.com/watch?v=0U1rkt8MX6M

Напомню, что 27-ми узловые элементы в LS-DYNA обладают кучей полезных свойств, о которых я уже писал:


    Работа на скручивание
    Работа в один слой по толщине
    Учет больших деформаций
    Обработка больших искажений сетки
    Сжимаемые и несжимаемые материалы
    Отсутствие эффекта песочных часов
    Отсутствие паразитной жесткости на сдвиг или объемное сжатие


Подробности работы элементов и их тестирования можно найти в статье Recent Advances on Higher Order 27-node Hexahedral Element in LS-DYNA
 #H8TOH27 #LS-DYNA #LS-PrePost
https://magicdpd.ru/?p=6087
