---
layout: post
title: "Работают ли бессрочные методы?"
date: 2016-10-02T12:00:54+00:00
author: "GlukRazor"
source: vk
original_url: https://vk.com/wall-97265142_129
tags:
  - EFG
  - SPH
  - ALE
  - FEM
  - LSDYNA
  - SPG
  - Lagrangian
---

Работают ли бессрочные методы?
http://www.dynalook.com/14th-international-ls-dyna-conference/constitutivemodeling/necking-and-failure-simulation-of-lead-material-using-ale-and-mesh-free-methods-in-ls-dyna-r

Небольшая статья с очередной конференции по #LSDYNA. В статье рассказывается о сравнении расчета с применением сеточных и бессрочных методов с экспериментом - разрывом металлического образца.
Постановки:
- #FEM #Lagrangian
- #FEM #ALE
- #SPH
- #EFG
- #SPG

Точную кривую не описал не один из методов. Точная форма получилась только у ALE. Хуже всех, естественно выступил SPH, с его численной нестабильностью при работе на растяжение. На мой вкус EFG дал самую хорошую кривую, но с формой беда.

Прям захотелось повторить численный эксперимент.
