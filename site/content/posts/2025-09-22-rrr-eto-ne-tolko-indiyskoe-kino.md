---
layout: post
title: "RRR - это не только индийское кино"
date: 2025-09-22T14:20:15+00:00
author: "Yury Novozhilov"
source: vk
images:
  - url: "/assets/images/3020.jpg"
---

В LS-DYNA R16 появилась новая модель материала *MAT_RRR_POLYMER/*MAT_317 разработанная вместе с IKEA. С одной стороны, модель показывает хорошую точность при наличии экспериментальных данных (надо идентифицировать 24 параметра!!!) и превосходить даже TNM. Она и работает раза в 3 быстрее.

Однако, модель отходит от использования градиентов деформации и полной формулировки, отказывается от наложения термодинамических ограничений" и порой может давать "замечательные" результаты:
- Нарушение второго закона термодинамики (! как в индийском кино !)
- Отсутствие гарантий положительности диссипации энергии
- Возможность предсказания нефизичного поведения при определенных условиях нагружения

Короче, если у вас есть своя лаба для экспериментов, то дерзайте. А если нет - то лучше не надо.

https://lsdyna.ansys.com/wp-content/uploads/2023/12/A-pragmatic-approach-to-modeling-of-nonlinear-rheological-networks-for-polymers-Thomas-Borrvall-Ansys.pdf

https://lsdyna.ansys.com/wp-content/uploads/2023/12/A-pragmatic-approach-to-modeling-of-nonlinear-rheological-networks-for-polymers-Thomas-Borrvall-Ansys.pdf
