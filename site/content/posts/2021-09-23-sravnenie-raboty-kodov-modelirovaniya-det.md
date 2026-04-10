---
author: MagicDPD
date: 2021-09-23 15:01:35+00:00
layout: post
link_previews:
- description: In this short article we compare blastFoam simulation results with
    other software and semi-empirical methods to provide confidence in the code
  image: https://media.licdn.com/dms/image/v2/C5612AQGTUKuchP8KDw/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1631495855454?e=2147483647&v=beta&t=yzEAZNOQoCKJ8sJkcmC7mKjZNJEgU59Ntx7qoAMkeV4
  title: blastFoam | Comparison of explosive airblast calculators
  url: https://www.linkedin.com/pulse/blastfoam-comparison-explosive-airblast-/?trackingId=Uq%2B3MZmoMgkb3xIYeAHk9A%3D%3D
source: vk
tags:
- blastfoam
- blast
- open_source
- openfoam
- autodyn
- europlexus
- ansys
- ls
- cht
- sandia
title: Сравнение работы кодов моделирования детонации ВВ
---

Разработчики blastFoam, открытого CFD кода на базе openFoam, специализирующегося на задачах детонации ВВ и распространении ударных волны в воздухе, опубликовали любопытное сравнение. Они смоделировали детонацию сферического заряда тротила в воздухе в бесконечном домене - довольно простая постановка с хорошо известными аналитическими решениями.







Моделирование они выполнили в:



Ansys Autodyn - код, разработанный когда-то, поглощённой компанией Century Dynamics - заточен под решение задач ОПКAnsys LS-DYNA - код, разработанный, поглощённой компанией LSTC - заточен под решение сильно связанных высоконелинейных задачEUROPLEXUS - или EpX, полуоткрытьй код для моделирования быстропротекающих процессов от французской промышленности, работает на основе моделей, подготовленных для Code_Aster.  CHT - код для моделирования быстропротекающих процессов от Сандийских национальных лабораторийblastFoam, который я уже представил



Во всех кодах использовалось уравнение состояния JWL. На мой взгляд, справились все коды примерно одинаково, и, не зная особенностей постановки задачи, времени, затраченного на решение, трудно выбрать лидера.







Надо просто иметь в виду, что какие-то из этих кодов могут решать только задачи детонации ВВ с различными уравнениями состояния, некоторые могут применяться для моделирования широкого круга динамических задач, а кто-то может замахнуться и на междисциплинарные расчеты. Так что выбирайте подходящие вам инструменты которым вас могут научить на понятном вам языке.



Ссылка на оригинальный пост: www.linkedin.com/pulse/blastfoam-comparison-explosive-airblast-/

#ansys #autodyn #blast #blastfoam #cht #europlexus #ls-dyna #open_source #openfoam #sandia
https://tinyurl.com/yzxkzr4r

[blastFoam | Comparison of explosive airblast calculators](https://www.linkedin.com/pulse/blastfoam-comparison-explosive-airblast-/?trackingId=Uq%2B3MZmoMgkb3xIYeAHk9A%3D%3D)
https://tinyurl.com/yzxkzr4r
