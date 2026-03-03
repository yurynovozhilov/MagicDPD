---
layout: post
title: "Fluent LS-DYNA 2-way-FSI via SyC"
date: 2025-05-26T14:05:29+00:00
author: "Yury Novozhilov"
source: vk
---

Fluent LS-DYNA 2-way-FSI via SyC

Итак, зачем это надо, я не представляют. В моем мире есть связка Fluent+MAPLD для точных расчетов чего-то не слишком нелинейного. Есть еще связка LS-DYNA Implicit + LS-DYNA ICFD для чего-то очень нелинейного, но  без учета сжимаемость течения. Кто хочет по жестче, может сунуться в LS-DYNA Explicit + LS-DYNA CE/SE для сжимаемых многофазных химически активных потоков. Но зачем может понадобиться связывать флюху и lsd?

И тем не менее, такое есть. А в статье есть ссылки на бесплатно доступные преднастроенные примеры и документацию (есть даже для 2025r1). И да, все это работает через интерфейс официальный API System Coupling!

https://lsdyna.ansys.com/wp-content/uploads/2023/12/Co-simulation-in-LS-DYNA-FMU-and-SYC-Isheng-Yeh-Ansys-1.pdf

https://lsdyna.ansys.com/wp-content/uploads/2023/12/Co-simulation-in-LS-DYNA-FMU-and-SYC-Isheng-Yeh-Ansys-1.pdf
