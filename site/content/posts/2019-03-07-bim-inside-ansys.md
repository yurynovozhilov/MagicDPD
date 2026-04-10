---
layout: post
title: "BIM inside ANSYS"
date: 2019-03-07T17:00:20+00:00
author: "GlukRazor"
source: vk
images:
  - url: "/assets/images/1381.jpg"
---

Данная разработка немецкого CADFEM позволяет снять один очень важный вопрос: как подружить BIM системы и CAE расчеты. Как это ни странно, модели из мира BIM (Building Information Modeling или Building Information Model, подробности тут: https://ru.wikipedia.org/wiki/BIM), обладающие как нужной расчетчикам, так и бесполезной для них информацией, очень непросто передать на расчет. Напрямую ни один BIM формат не читает даже всеядный SpaceClaim. Передача через сторонние форматы представляет собой игру в рулетку: непонятно какой формат сработает и сколько процентов модели потеряется.









Так вот, BIM inside ANSYS должен давать возможность напрямую зачитывать IFC модели (Industry Foundation Classes — промышленный стандарт BIM моделей, подробности тут https://ru.wikipedia.org/wiki/Industry_Foundation_Classes), выбирать, что из всех компонентов сборки надо, и передавать полученные компоненты на расчет. Ну что ж, буду тестировать.



Подробности по продукту на русском можно почитать тут:

https://ru.wikipedia.org/wiki/BIM
https://ru.wikipedia.org/wiki/Industry_Foundation_Classes
