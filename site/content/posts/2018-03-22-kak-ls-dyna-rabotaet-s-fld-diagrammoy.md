---
layout: post
title: "Как LS-DYNA работает с FLD диаграммой"
date: 2018-03-22T18:00:41+00:00
author: "GlukRazor"
source: vk
tags:
  - LSPrePost
  - LSTC
  - Forming
  - LSDYNA
  - FLD
images:
  - url: "/assets/images/866.jpg"
---

Диаграмма предельного формоизменения (FLD, Forming Limit Diagram) – метод, позволяющий предсказать разрушения листового материала при штамповке. Данные FLD являются неким стандартом описания материала для расчета штамповки, глубокой вытяжки и прочих способов обработки листового металла давлением.

Естественно, LSTC давно реализовали поддержку такого типа данных в LS-PrePost (http://www.lstc.com/lspp/content/pages/1/fld/fld.shtml), однако, в прошлом году они сделали кое-что еще более интересное прямо на уровне LS-DYNA. Так были внесены две новые карты, упрощающие работу: *DEFINE_CURVE_FLD_FROM_TRIAXIAL_LIMIT и *DEFINE_CURVE_TRIAXIAL_LIMIT_FROM_FLD. Как нетрудно понять по их названиям, теперь решатель сам может конвертировать полученные на вход данные в нужный для расчета формат. Данные будут переданы в модели материалов *MAT_037_NLP_FAILURE или *MAT_260B, в универсальную модель разрушения *MAT_ADD_EROSION или в карту типа *CONTROL_FORMING_ ONESTEP.
Подробности с примерами работы доступны в статье по ссылке:
http://www.lstc.com/sites/default/files/marketing/new_features/08_Conversion%20between%20FLD%20and%20Stress%20Triaxial%20Limit%20Curve.pdf

#FLD #Forming #LSDYNA #LSPrePost #LSTC
https://goo.gl/1yoywt

http://www.lstc.com/lspp/content/pages/1/fld/fld.shtml
http://www.lstc.com/sites/default/files/marketing/new_features/08_Conversion%20between%20FLD%20and%20Stress%20Triaxial%20Limit%20Curve.pdf
https://goo.gl/1yoywt
