---
layout: post
title: "Делаем 27-ми узловые элементы в LS-PrePost"
date: 2018-01-31T17:01:06+00:00
author: "GlukRazor"
source: vk
tags:
  - LS
  - H8TOH27
images:
  - url: "/assets/images/759.jpg"
---

Делаем 27-ми узловые элементы в LS-PrePost
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

https://www.youtube.com/watch?v=0U1rkt8MX6M
http://www.dynalook.com/14th-international-ls-dyna-conference/simulation/recent-advances-on-higher-order-27-node-hexahedral-element-in-ls-dyna-r
https://magicdpd.ru/?p=6087
