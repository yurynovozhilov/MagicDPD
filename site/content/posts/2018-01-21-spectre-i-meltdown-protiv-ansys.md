---
layout: post
title: "Spectre и Meltdown против ANSYS"
date: 2018-01-21T17:01:07+00:00
author: "GlukRazor"
source: vk
tags:
  - ANSYS
  - HPC
  - Mechanical
  - Meltdown
  - Spectre
  - padtinc
images:
  - url: "/assets/images/740.jpg"
---

В начале этого года прогремели новости об обнаружении уязвимостей практически во всех процессорах x86_64 и ARM. Уязвимости получили названия Spectre и Meltdown - у них даже есть свой сайт https://spectreattack.com (а у вас есть? :-)). Я не буду вдаваться в подробности работы уязвимостей, скажу только, что с их появлением можно забыть о концепции защищенной памяти процесса, которая декларировалась уже лет 10 - это огромная дыра в безопасности!

Для исправления уязвимостей были выпущены заплатки на уровне операционных систем, которые исправляют баг, но могут очень здорово просадить производительность системы: от 5 в зависимости от типа решаемой задачи. Перед всеми нами встала дилемма: работать безопасно или работать быстро? Но вот почти никто не стал проверять, насколько проседает производительность в задачах, которые интересны нам - в CAE.

Одними из немногих, кто провел реальные тесты и опубликовал их результаты, оказался коллектив PADT Inc. Коллеги взяли задачу Ball Grid Array из стандартного набора тестов производительности для  ANSYS Mechanical 18.2  Benchmark и выполнили расчет на двухпроцессорной рабочей станции:


CPU: INTEL XEON Gold 6130 CPU x2
RAM: 128GB DDR4-2667MHz (1Rx4) ECC REG DIMM
OS: Windows 10 Professional
MPI: INTEL MPI 5.0.1.3
GPU: NVIDIA QUADRO P4000
SSD: Samsung EVO 960 Pro NVMe M.2
HDD: Toshiba 2TB 7200 RPM SATA 3 Drive


Результаты получились примерно следующие:



Как можно видеть, производительность на данном тесте падает не более чем на 10%, а в некоторых случаях даже растет (что вообще-то очень странно). Для случая использования высокооптимизированного решателя ANSYS Mechanical исправления уязвимостей Spectre и Meltdown оказыват малое влияние на время расчета.

http://www.padtinc.com/blog/the-focus/spectre-side-channel-and-meltdown-how-will-living-in-this-new-reality-affect-the-world-of-numerical-simulation
#ANSYS #HPC #Mechanical #Meltdown #padtinc #Spectre
https://magicdpd.ru/?p=6002

https://spectreattack.com
5.0.1.3
http://www.padtinc.com/blog/the-focus/spectre-side-channel-and-meltdown-how-will-living-in-this-new-reality-affect-the-world-of-numerical-simulation
https://magicdpd.ru/?p=6002
