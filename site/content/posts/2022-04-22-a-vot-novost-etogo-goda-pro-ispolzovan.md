---
layout: post
title: "А вот новость этого года про использование #GPU для #CFD расчетов в #Fluent. В версии #Ansys 2022 R1 завезли beta версию, как я называю \"второго поколения\" CFD-GPU решателя, который получил название \"Ansys Multi-GPU Solver\". Данный решатель пока работает не для вех бесчисленных классов задач, решаемых Fluent. Но, вот для задач внешней аэродинамики, производительность решателя просто взлетает в космос!"
date: 2022-04-22T17:00:10+00:00
author: "MagicDPD"
source: vk
tags:
  - CFD
  - Intel
  - GPU
  - HPC
  - Xeon
  - NVIDIA
  - Ansys
  - Fluent
  - Gold
  - A100
images:
  - url: "/assets/images/2230.jpg"
  - url: "/assets/images/2231.jpg"
---

Одна карта #NVIDIA #A100 дает производительность, соизмеримую с 272 процессорными ядрами #Intel #Xeon #Gold 6242!

Новый решатель позволяет одновременно:
- снизить стоимость используемого железа до 7 раз
- снизить потребление электроэнергии вычислительной системой до 4 раза

А если учесть, что решатели Ansys традиционно лицензируется так, что стоимость задействования 1 процессорного ядра эквивалентна стоимости задействования 1 карты NVIDIA A100, то цена требуемых для #HPC расчетов лицензий с новым "Ansys Multi-GPU Solver" оказывается если не в сотни, то в десятки раз ниже! https://www.ansys.com/blog/unleashing-the-power-of-multiple-gpus-for-cfd-simulations

[Unleashing the Power of Multiple GPUs for CFD Simulations](https://www.ansys.com/blog/unleashing-the-power-of-multiple-gpus-for-cfd-simulations)
