---
layout: post
title: "Моделирование роста трещин"
date: 2016-10-08T17:00:13+00:00
author: "GlukRazor"
source: vk
tags:
  - Abaqus
  - ANSYS
  - XFEM
  - Mechanical
  - LSDYNA
  - FEM
---

Моделирование роста трещин
https://www.youtube.com/watch?v=FaS-VvNLM3c

Есть такое интересное расширение #FEM - #XFEM называется. Все как в обычном сеточном методе, только поддерживаются разрывные функции формы, что позволяет простить трещины не сквозь сетку (не убивая/удаляя элементы). И тут пальма первенства у #Abaqus. Конечно XFEM был в #LSDYNA с 2006 года, конечно он есть #ANSYS #Mechanical с 2015 года... Но эти реализации чаще работают в постановках плоской теории упругости. А вот математика Abaqus позволяет использовать XFEM в 3D постановке.

Специально по теме небольшой учебный пример:
https://www.youtube.com/watch?v=FaS-VvNLM3c

[XFEM 3D](https://www.youtube.com/watch?v=FaS-VvNLM3c)
