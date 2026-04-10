---
author: Yury Novozhilov
date: 2025-09-25 09:00:28+00:00
layout: post
link_previews:
- description: This work presents a novel three-dimensional Crack Element Method (CEM)
    designed to model transient dynamic crack propagation in quasi-brittle materials
    efficiently. CEM introduces an advanced element-splitting algorithm that enables
    element-wise crack growth, including crack branching. Based on the evolving topology
    of split elements, an original formulation for computing the fracture energy release
    rate in three dimensions is derived. A series of benchmark examples is conducted
    to demonstrate
  image: /static/browse/0.3.4/images/arxiv-logo-fb.png
  title: A GPU-Accelerated Three-Dimensional Crack Element Method for Transient Dynamic
    Fracture Simulation
  url: https://arxiv.org/abs/2508.04076
source: vk
title: A GPU-Accelerated Three-Dimensional Crack Element Method for Transient Dynamic
  Fracture Simulation
---

Если мне хочется почитать что-то интересное, то я захожу в Google Scholar профиль C.T.Wu. Доктор C.T.Wu выдающийся ученый, глава LST CMM Group (ученые, разрабатывающие все новые бессеточные алгоритмы и AI модели) и очень приятный в общении человек.

В этом году вышел препринт его новой работы:
- Авторы предлагают новый трёхмерный Crack Element Method (CEM) для моделирования нестационарного динамического разрушения в квазихрупких материалах.
- Метод включает алгоритм расщепления конечных элементов, позволяющий описывать рост трещин, их ветвление и сложные формы поверхности разрушения.
- Для аппроксимации перемещений в разрушенных элементах используется Edge-based Smoothed FEM (ES-FEM).
- Введена новая формулировка для вычисления скорости высвобождения энергии разрушения (fracture energy release rate) на основе изменяющейся топологии элементов.
- Все 3D-модели рассчитываются с GPU-ускорением, что обеспечивает высокую вычислительную эффективность и масштабируемость.

Итак, LSD + GPU + NL Craks with nodes splitting. Ждем!

https://arxiv.org/abs/2508.04076

[A GPU-Accelerated Three-Dimensional Crack Element Method for...](https://arxiv.org/abs/2508.04076)
