---
title: "Учeт присоединенной массы при поиске собственных частот через BEM"
date: 2025-10-07T15:05:42+00:00
source: tg
original_url: "https://t.me/MagicDPD/3031"
---

В дайне уже пару лет как есть странное но прикольное. Подход BOUNDARY_FLUIDM в LS-DYNA использует граничный интегральный метод (BEM - Boundary Element Method) для моделирования эффектов присоединенной массы несжимаемой невязкой жидкости при поиске собственных частот.
BEM не требует создания сетки для жидкости, в данной постановке не сильно увеличивает размерность, не нарушает симметрию матрицы жескткости (в отличии от классического подхода с FLUID29/FLUID30/FLUID220/FLUID221 в APLD), позволяя легко использовать результаты в последующих расчетах (например, SSD).

Что скажут господа кораблестроители?

https://lsdyna.ansys.com/wp-content/uploads/2023/12/Fluid-added-mass-modeling-in-LS-DYNA-and-its-application-in-structural-vibration-Yun-Huang-Ansys.pdf
https://www.dynalook.com/conferences/17th-international-ls-dyna-conference-2024/nvh-implicit/huang_ansys.pdf
https://www.dynalook.com/conferences/14th-european-ls-dyna-conference-2023/nvh-implicit/huang_ansys.pdf
