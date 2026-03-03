---
layout: post
title: "Моделировать метод послойного наплавления или 3D печать (Fus"
date: 2017-08-11T17:01:44+00:00
author: "GlukRazor"
source: vk
tags:
  - ANSYS
  - APDL
  - Mechanical
  - SDCM
  - FDM
  - Python
  - ACT
  - STL
images:
  - url: "/assets/images/434.jpg"
---

Моделировать метод послойного наплавления или 3D печать (Fused depositing modeling, #FDM) можно в любом современном КЭ пакете: все как правило реализуется через технику рождения и смерти элементов под действием температурных полей. Однако коллеги из чешской компании  SVS FEM пошли дальше, много дальше. Они создали #ACT расширение для #ANSYS #Mechanical на основе #Python и #APDL, которое умеет читать информацию от 3D принтера по истории движения печатающей головки. В ходе расчета можно получить зависимости плотности, температуры и деформаций конструкции во времени.

Самое прикольное в работе ACT - это возможность визуализировать именно плотность (читай распределение) материала. Она получается гладкая, и ее можно экспортировать в виде #STL в #SDCM для дальнейшей работы.

https://www.youtube.com/watch?v=qai6CIpjOHM

[Structural-Thermal Simulation of FDM 3D Printing Process | ANSYS Mechanical | SVS FEM](https://www.youtube.com/watch?v=qai6CIpjOHM)
