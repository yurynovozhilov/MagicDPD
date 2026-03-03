---
layout: post
title: "Моделирование армирования в бессеточных методах"
date: 2018-07-19T18:00:31+00:00
author: "GlukRazor"
source: vk
tags:
  - LSTC
  - SPH
  - Meshless
  - LSDYNA
  - Reinforcement
  - SPG
images:
  - url: "/assets/images/1023.jpg"
---

Моделирование армирования в бессеточных методах
Хочу обратить ваше внимание на статью "The Immersed Smoothed Particle Galerkin Method in LS-DYNA® for Material Failure Analysis of Fiber-Reinforced Solid Structures", опубликованную в рамках 15-ой международной пользовательской конференции LS-DYNA. В ней рассказывается про разработку новой карты *CONSTRAINED_IMMERSED_IN_SPG, которая позволяет автоматически встраивать армирование на основе beam элементов в матрицу, на основе SPG формулировки.

SPG - Smoothed Particle Galerkin Method - бессеточный метод, разработанный LSTC для моделирования процессов как хрупкого, так и пластического разрушения. Данный метод вобрал в себя все преимущества SPH, но лишился его недостатков - например, нестабильности при растяжении или невозможности работы с неявным решателем. Подробности по математике метода тут: https://www.dynalook.com/13th-international-ls-dyna-conference/fluid-structure-interaction/an-introduction-to-the-ls-dyna-r-smoothed-particle-galerkin-method-for-severe-deformation-and-failure-analyses-in-solids
Таким образом, *CONSTRAINED_IMMERSED_IN_SPG позволит нормально считать задачи пробивания в бессеточной постановке как только будет включен.

#LSDYNA #LSTC #Meshless #Reinforcement #SPG #SPH
http://bit.ly/2NrEzFg

https://www.dynalook.com/15th-international-ls-dyna-conference/spg/the-immersed-smoothed-particle-galerkin-method-in-ls-dyna-r-for-material-failure-analysis-of-fiber-reinforced-solid-structures
https://www.dynalook.com/13th-international-ls-dyna-conference/fluid-structure-interaction/an-introduction-to-the-ls-dyna-r-smoothed-particle-galerkin-method-for-severe-deformation-and-failure-analyses-in-solids
http://bit.ly/2NrEzFg
