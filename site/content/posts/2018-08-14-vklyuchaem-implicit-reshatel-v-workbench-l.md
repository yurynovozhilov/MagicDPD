---
layout: post
title: "Включаем Implicit решатель в Workbench LS-DYNA"
date: 2018-08-14T18:01:23+00:00
author: "GlukRazor"
source: vk
tags:
  - Implicit
  - ANSYS
  - SommandSnipet
  - Workbench
  - ARUP
  - LSDYNA
  - Longread
  - ACT
images:
  - url: "/assets/images/1070.jpg"
---

Если очень надо, то можно и Workbench LS-DYNA  заставить работать в Implicit режиме. При этом выводятся очень симпатичные невязки. Хотя графики на первых порах были бы приятнее.
Далее код командного объекта, что включает хороший нелинейный расчет. Будьте очень аккуратны при копировании: даже несмотря на freeformat стиль записи, есть вероятность, что web форматирование может повредить командный блок. Лучше сначала проверьте его в LS-PrePost. Командный объект подготвлен на основе материалов ARUP, найденных в сети в 2017 году.

*CONTROL_ACCURACY
$
$ OSU – 2nd order objective stress update
$ = 0 -> Off (default)
$ = 1 -> On
$
$ INN – Invariant node numbering
$ = 2 -> On for shell and thick shell elements (default for implicit)
$
$ IACC – Implicit accuracy flag, turns on some specific accuracy considerations in implicit analysis at an extra CPU cost.
$ = 0 -> Off (default)
$ = 1 -> On
$
1,2,0,1
*CONTROL_IMPLICIT_AUTO
$
$ IAUTO – Automatic time step control
$ = 0 -> constant time step size (default)
$ = 1 -> automatically adjusted timestep size
$
$ DTMIN – Minimum allowable timestep size (default = DT0/1000)
$ Simulation stops with error termination, if time step falls below DTMIN
$
$ DTMAX – Maximum allowable timestep (default = DT0*10)
$
1,11,5,0.0002,0.02
*CONTROL_IMPLICIT_GENERAL
$
$ IMFLAG – Implicit/ Explicit analysis type flag
$ = 1 -> Implicit analysis
$
$ DT0 – Initial time step size for implicit
$ (default – none)
$
$ IMFORM:= Element formulation switching flag
$ EQ.1: switch to fully integrated formulation for implicit springback
$ EQ.2: retain original element formulation (default).
;
1,0.02,1,1,2
*CONTROL_IMPLICIT_SOLUTION
$
$ NSOLVR – Solution method for implicit analysis
$ = 2 -> Nonlinear with BFGS updates (obsolete)
$ = 12 -> (new default from 9.0.1) Nonlinear with BFGS updates
$ + optional arc length
$ + different line search and integration schemes compared to solver 2.
$
$ DCTOL – Displacement relative convergence tolerance (default = 0.001)
$
$ ECTOL – Energy relative convergence tolerance (default = 0.01)
$
$ NLPRINT – Nonlinear solver print flag
$ = 3 -> print iteration, norm and line search info.
$
$ D3ITCTL – Controls D3ITER database (default = 0)
$
12,11,15,0.001,0.01,1e+010,0.9,1e-010
2,1,1,3,2
0,,,1,2
4,2
*DATABASE_EXTENT_BINARY
$
$ RESPLT – Output of translational and rotational residual forces to d3plot & d3iter.
$ = 1 -> Output residual
$
,,,1,1,1,1,1
,,,1,1,1,2
,,,,2,,,
,1

#ACT #ANSYS #ARUP #Implicit #Longread #LSDYNA #SommandSnipet #Workbench
http://bit.ly/2OwQJgD

http://bit.ly/2OwQJgD
