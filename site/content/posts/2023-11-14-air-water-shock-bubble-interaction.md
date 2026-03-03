---
layout: post
title: "Air-water shock bubble interaction"
date: 2023-11-14T16:00:40+00:00
author: "Yury Novozhilov"
source: vk
original_url: https://vk.com/wall-97265142_2578
---

Air-water shock bubble interaction

blastFoam показали решение классической задачи взаипосдествия ударной волны, распространяющейся в воде, с подводным воздушным пузырем.
- Ударная волна имеет число Маха 1,422 и движется в воде.
Послеударная область первоначально находится в состоянии покоя и включает воздушный пузырь радиусом 0,2 м.
- Результаты сравниваются с оригинальными результатами, полученными в работах Shyue 1999 и Zheng 2008. (ссылки см. ниже)
- Расчет занимает около 10 мин. на четырехъядерном настольном компьютере при эталонном разрешении (например, 24x20 ячеек с максимальным уровнем детализации 4)

Прямая ссылка на модель: https://github.com/synthetik-technologies/blastfoam/tree/master/validation/blastFoam/airWaterShockBubble

Литература:
[1] Zheng, H.W., C. Shu, and Y.T. Chew. “An Object-Oriented and Quadrilateral-Mesh Based Solution Adaptive Algorithm for Compressible Multi-Fluid Flows.” Journal of Computational Physics 227, no. 14 (July 2008): 6895–6921. https://doi.org/10.1016/j.jcp.2008.03....

[2] Shyue, K.-M., 1999. A Fluid-Mixture Type Algorithm for Compressible Multicomponent Flow with van der Waals Equation of State. Journal of Computational Physics 156, 43–88. https://doi.org/10.1006/jcph.1999.6349

https://www.youtube.com/watch?v=aZOAHYUs2HM
