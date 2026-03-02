---
layout: post
title: "MS RDP и OpenGL"
date: 2016-09-16T17:00:11+00:00
author: "GlukRazor"
source: vk
original_url: https://vk.com/wall-97265142_110
tags:
  - RDP
  - NVIDIA
  - Windows
  - OpenGL
  - ANSYS
---

http://www.nvidia.com/download/driverResults.aspx/79105/en-us

На днях один из моих коллег пожаловался мне, что у него через #RDP совершенно не тормозит работа с тяжелой моделью в #ANSYS. Я всегда держал в голове, что через RDP всегда получается плохо работать с #OpenGL. Каково же было мое удивление, когда я увидел по данным тестов поддержку OpenGL 4.4! И никаких тормозов!

Секрет оказался прост: оказывается для профессиональный видеокарт #NVIDIA давно (начиная с версии драйвера 341.05) включила поддержку OpenGL 4+ при работе через RDP. A #Windows 10 обеспечил сжатие потока хорошим видеокодеком.

Так что всем бегом за профессиональными видеокартами.

http://www.nvidia.com/download/driverResults.aspx/79105/en-us
