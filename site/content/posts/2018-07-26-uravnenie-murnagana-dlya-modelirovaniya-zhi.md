---
layout: post
title: "Уравнение Мурнагана для моделирования жидкостей в SPH"
date: 2018-07-26T18:00:32+00:00
author: "GlukRazor"
source: vk
tags:
  - CFD
  - LSDYNA
  - FSI
  - ICFD
  - MURNAGHAN
  - SPH
images:
  - url: "/assets/images/1039.jpg"
---

В LS-DYNA R10 появилось новое уравнение состояния для моделирования жидкостей. Если раньше приходилось мучаться с уравнением состояния Грюнайзена, то теперь есть специальное уравнение состояния Мурнагана для слабосжимаемых жидкостей. У LSTC есть не только статья, рассказывающая о том, как работает данное уравнение, но и целый рабочий пример, скалиброванный на эксперименте и дающий достоверные результаты!

Таким образом, мы имеем EOS_MURNAGHAN, которое сопрягается с MAT_NULL и работает только для SECTION_SPH. Остается только задать вязкость жидкости через CONTROL_BULK_VISCOSITY и все готово. Полученное решение хорошо согласуется с экспериментами и расчетами в CFD решателе LS-DYNA ICFD.

Статья: https://www.dynalook.com/15th-international-ls-dyna-conference/sph/fluid-flow-modeling-with-sph-in-ls-dyna-r
Тестовый пример: https://www.dynaexamples.com/sph/intermediate-examples/wavestructure

#CFD #FSI #ICFD #LSDYNA #MURNAGHAN #SPH
http://bit.ly/2K2RMSG

https://www.dynalook.com/15th-international-ls-dyna-conference/sph/fluid-flow-modeling-with-sph-in-ls-dyna-r
https://www.dynaexamples.com/sph/intermediate-examples/wavestructure
http://bit.ly/2K2RMSG
