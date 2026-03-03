---
layout: post
title: "Что вы знаете о странных конечных элементах"
date: 2016-11-19T12:00:52+00:00
author: "GlukRazor"
source: vk
original_url: https://vk.com/wall-97265142_191
tags:
  - hourglass
  - explicit
  - implicit
  - LSDYNA
---

Что вы знаете о странных конечных элементах
http://www.dynalook.com/14th-international-ls-dyna-conference/simulation/recent-advances-on-higher-order-27-node-hexahedral-element-in-ls-dyna-r

Все привыкли к тому, что для #implicit расчетов механики оптимальны 20-ти узловые hex элементы, а для #explicit обычно используют 8-ми узловые hex с одной точкой интегрирования. А как вам идея использовать 27 узлов на один элемент?! Свежая статья о новом типе элементов для #LSDYNA, который не только позволяет получить очень хорошие показатели по точности для больших и малых деформаций, но еще и автоматически решает проблему песочных часов (#hourglass). Просто добавь 8 узлов на углах, 12 - на ребрах, 6 - в центрах граней и 1 - в геометрическом центре - получи *ELEMENT_SOLID_H27
