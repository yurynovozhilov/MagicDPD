---
author: GlukRazor
date: 2017-06-05 17:01:28+00:00
layout: post
link_previews:
- description: ''
  image: ''
  title: Home | GRS gGmbH
  url: http://www.grs.de/en
source: vk
tags:
- RHT
- ANYS
- concrete
- LSTC
- LSDYNA
- GRS
- AUTODYN
- RTH
- Explicit
title: Реализации модели RHT (RTH) в LS-DYNA и AUTODYN
---

http://www.dynalook.com/11th-european-ls-dyna-conference/concrete-penetration/comparison-of-the-rht-concrete-material-model-in-ls-dyna-and-ansys-autodyn/view

Модель материала для предсказания поведения высокопрочного и сверх высокопрочного бетона #RHT или #RTH является пожалуй одной из самых известных моделей в своей области. Она названа по инициалам ученых, разработавших ее: Riedel, Hiermaier и Thoma.

Данная модель реализована как в #LSTC #LSDYNA (*MAT_272), так и в #ANYS #AUTODYN (и в ANSYS #Explicit STR заодно ). Только если в LSD есть еще с десяток моделей-конкурентов, до в AD других моделей бетона нет.

Коллеги из немецкой организации #GRS (Gesellschaft für Anlagen- und Reaktorsicherheit (GRS) gGmbH, http://www.grs.de/en) в своей работе провели сравнительный анализ реализаций модели. Получились очень любопытные выводы. Обе реализации сеточнозависимы по показателю разрушения, в AUTODYN еще и некорректно считает трещенообразование при растягивающих нагрузках.

http://www.dynalook.com/11th-european-ls-dyna-conference/concrete-penetration/comparison-of-the-rht-concrete-material-model-in-ls-dyna-and-ansys-autodyn/view
http://www.grs.de/en
