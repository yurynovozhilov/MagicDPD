---
layout: post
title: "OpenLSTO - открытый код оптимизации топологии"
date: 2019-01-10T17:01:23+00:00
author: "GlukRazor"
source: vk
original_url: https://vk.com/wall-97265142_1301
tags:
  - OpenLSTO
  - LevelSetMethod
  - Optimization
  - OpenSource
  - Topology
  - M2DO
images:
  - url: "/assets/images/1302.jpg"
---

Летом 2018 года команда&nbsp;M2DO (Multiscale Multiphysics Design Optimization Laboratory)&nbsp;Калифорнийского университета Сан-Диего представила новый код для решения задач топологической оптимизации&nbsp;OpenLSTO.&nbsp;




Результаты 3D оптимизации




Название кода расшифровывается как&nbsp; «open-source software for level set based structural topology optimization», что может быть переведено на русский язык как «программное обеспечение с открытым исходным кодом для топологической оптимизации с использованием метода фиксации уровня».


Взаимосвязь между функцией фиксации уровня (снизу) и получаемым контуром (сверху)



Подробнее про работу метода на русском можно почитать статью на Хабре:&nbsp;https://habr.com/post/332692/. Данный метод сейчас начинает очень активно применяться при решении задач оптимизации топологии, так как дает хорошие гладкие формы новой геометрии быстро и эффективно. И OpenLSTO, насколько я знаю, первая open source реализация такого подхода.



Результаты 2D оптимизации



Код, к сожалению, написан на C++. Без его знания вы хороших результатов не добьётесь, так как GUI у кода пока нет — есть только командная строка под *nix совместимыми операционными системами. Ну хоть результаты можно смотреть в ParaView.&nbsp;



Домашняя страница проекта:&nbsp;http://m2do.ucsd.edu/software/
Репозиторий GitHub:&nbsp;https://github.com/M2DOLab/OpenLSTO
Документация с учебными примерами:&nbsp;http://m2do.ucsd.edu/static/pdf/OpenLSTO-Tutorial-v1.0.pdf


#LevelSetMethod #M2DO #OpenSource #OpenLSTO #Optimization #Topology
http://bit.ly/2VLn1bU
