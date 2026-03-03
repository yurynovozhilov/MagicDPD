---
layout: post
title: "Чего я жду от LS-DYNA R17"
date: 2026-01-14T08:59:01+00:00
author: "Yury Novozhilov"
source: vk
---

Чего я жду от LS-DYNA R17

Вот топ 7(+1) фишек, которые мне прям нужны:
- Новые быстрые Modular Contact (хотя, я думаю, что в этом году их еще не доделают)
- User-Defined Failure в *MAT_ADD_EROSION которые можно задать через *DEFINE_FUNCTION (сейчас такое требует знаний фортрана и пресборки решателя)
- Полноценное расрапаллеливание ISPG (сейчас одна капля может обслуживаться только одним процессорным ядром)
- Начало поддержки GPU (сейчас есть только x86/ARM64 CPU) для ALE/SPG/SPH
- Immersed FSI внутри ICFD (сейчас есть только стандартный boundary fitted FSI)
- Сопряжение химического решателя с Dual CE/SE (сейчас есть связь только со старым CE/SE)
- CPG+DEM, особенно в приложении к выделении газа при горении аккумуляторных батарей

И, наконец, знаменитое ONE MORE THING: сферические и цилиндрические системы координат в решателе :)

Презентация с конференции с пруфами:
https://www.ansys.com/content/dam/events/2025/transportation-summit/presentations/day-1/track-5-crash/10-crash-madhukeshavamurthy-ls-dyna-recent-innovations-r17.pdf

https://www.ansys.com/content/dam/events/2025/transportation-summit/presentations/day-1/track-5-crash/10-crash-madhukeshavamurthy-ls-dyna-recent-innovations-r17.pdf
