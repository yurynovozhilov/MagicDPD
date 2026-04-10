---
layout: post
title: "HexGen и Hex2Spline: ALLHEX и IGA сетки для LS-DYNA"
date: 2021-09-17T13:01:45+00:00
author: "MagicDPD"
source: vk
tags:
  - bext
  - iga
  - open_source
  - polycube
  - ls
  - ansys
  - all
---

Коллеги, на мой взгляд, сегодня просто огненный контент. Представляю вам два открытых набора консольных утилит, HexGen и Hex2Spline, разработанные группой профессора Юнцзе Джессики Чжан (Yongjie Jessica Zhang) в Университете Карнеги-Меллон (Carnegie Mellon University). Что бы лучше понимать, эта группа очень тесно связана со всем, что сейчас делается в области IGA для LS-DYNA и Corefrom.







Рассматриваемый комплект утилит позволяет на основе произвольной геометрии строить ALL-HEX неструктурированную сетку при помощи реализации алгоритма поликуба - это делает HexGen. А уже на основе полученной сетки Hex2Spline строить модель для IGA расчета, извлекая данные сплайнов Безье и записывая их в формат BEXT, напрямую читаемый LS-DYNA и визуализируемый в LS-PrePost.







Что особенно приятно, так это степень проработки вопроса. В репозитории проекта вы найдете не только все сходные коды утилит и собранные бинарники по Windows - вы найдете подробные инструкции по пересборке утилит. Естественно, в репозитории есть и тренировочные примеры с итогами правильной работы софта. А еще есть сопроводительная научная статья, в которой вы найдете подробные инструкции как пользоваться всеми утилитами и как настраивать их работу для разных геометрических моделей.



Научная статья: https://arxiv.org/abs/2011.14213



Репозиторий проекта: https://github.com/yu-yuxuan/HexGen_Hex2Spline



Страничка группы профессора Джессики Чжан в Университете Карнеги-Меллон:  https://www.meche.engineering.cmu.edu/directory/bios/zhang-yongjie.html

#all-hex #ansys #bext #iga #ls-dyna #ls-prepost #open_source #polycube
https://tinyurl.com/ydnqewkz

[HexGen and Hex2Spline: Polycube-based Hexahedral Mesh Generation...](https://arxiv.org/abs/2011.14213)
https://github.com/yu-yuxuan/HexGen_Hex2Spline
https://www.meche.engineering.cmu.edu/directory/bios/zhang-yongjie.html
https://tinyurl.com/ydnqewkz
