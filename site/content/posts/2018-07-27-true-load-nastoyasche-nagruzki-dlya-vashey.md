---
author: GlukRazor
date: 2018-07-27 18:00:36+00:00
images:
- url: /assets/images/1041.jpg
layout: post
link_previews:
- description: Wolf Star Technologies True-Load is first to market Load Reconstruction
    Software that leverages parts and FEA models to create multi-channel load cells,
    optimize strain gauge placement, and improve the product design cycle.
  image: ''
  title: True-Load | Load Reconstruction Software | Wolf Star Technologies, LLC
  url: https://www.wolfstartech.com/true-load
source: vk
tags:
- DigitalTwin
- Fatigue
- TrueLoad
- WolfStarTechnologies
title: True-Load - настояще нагрузки для вашей КЭ модели
---

Как-то раз у меня уже проскакивала новость про True-Load, и их дружбу с ANSYS Workbench. Помнится тогда, мы так и не нашли правды: чем эта дружба так полезна для инженеров. Теперь настало время разобраться в True-Load, тем более, что мне на глаза попалась запись часового вебинара от создателя технологии.

Итак, True-Load (https://www.wolfstartech.com/true-load), разработка Wolf Star Technologies LLC, позволяет вам сформировать условия и историю нагружения конструкции, которые будут использоваться при расчете долговечности. Алгоритм работы True-Load таков:

Инженер строит КЭ модель
Инженер задает варианты граничных условий и нагрузок
Система раскладывает нагрузки на "базис" - единичные нагрузки по глобальным осям
Система строит матрицу отклика конструкции на базисные нагрузки в линейном приближении
На основе полученных даных система предлагает оптимальное расположение тензодатчиков как на КЭ модели, так и на реальном изделии
По данным с датчиков на реальной модели система восстанавливает реальную историю нагружения модели (ведь матрица отклика уже получена на шаге 4)
Полученные нагрузки прикладываются к КЭ модели

Проделав эту процедуру один раз, мы получаем материал для оптимизации усталостной долговечности конструкции в любом поддерживаемом программном обеспечении.
Особенно мне понравился 5-й шаг в рабочем процессе True-Load, когда система прямо в графике показывает вам где стоит устанавливать тензодатчики.

Естественно, надо понимать (и это говорит сам создатель ПО в вебинаре), вся схема работает, пока вы не выходите за рамки линейной модели, как и вся концепция усталостной долговечности.
А еще, эта штука может работать в рамках так модного сейчас промышленного интернета вещей, анализируя нагрузки на конструкции в реальном времени и проводя расчет долговечности для цифрового двойника.

P.S. Пост по теме в блока ANSYS: http://www.ansys-blog.com/true-load-software/

#DigitalTwin #Fatigue #TrueLoad #WolfStarTechnologies
http://bit.ly/2K0ZAEx

[True-Load | Load Reconstruction Software | Wolf Star Technologies, LLC](https://www.wolfstartech.com/true-load)
http://www.ansys-blog.com/true-load-software/
http://bit.ly/2K0ZAEx
