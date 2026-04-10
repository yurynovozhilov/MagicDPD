---
layout: post
title: "NVIDIA DOCKER"
date: 2018-01-09T17:00:47+00:00
author: "GlukRazor"
source: vk
tags:
  - EGL
  - HPC
  - remoteviz
  - Praview
  - NVIDIA
  - cloud
  - GLX
  - Docker
images:
  - url: "/assets/images/709.jpg"
---

NVIDIA на конференции SC17 рассказала про свое новое видение того, как надо делать удаленную визуализацию на суперкомпьютерах. И тут разговор идет не просто о DCV или VirtualGL - тут рассматривается полностью новая концепция систем для визуализации действительно больших данных.

Для этих целей NVIDIA планирует использовать пары Docker контейнеров, подготовленных для нужного вам приложения (сейчас уже есть для Praview). Серверный конетйнер будет работать напрямую с EGL API (https://en.wikipedia.org/wiki/EGL_(API) и никаких тебе иксов), а клиентская часть - с GLX (https://en.wikipedia.org/wiki/GLX)

https://www.youtube.com/watch?v=z7nNmyKvMu4
#cloud #Docker #EGL #GLX #HPC #NVIDIA #Praview #remoteviz
https://magicdpd.ru/?p=5861

https://en.wikipedia.org/wiki/EGL_(API)
https://en.wikipedia.org/wiki/GLX
https://www.youtube.com/watch?v=z7nNmyKvMu4
https://magicdpd.ru/?p=5861
