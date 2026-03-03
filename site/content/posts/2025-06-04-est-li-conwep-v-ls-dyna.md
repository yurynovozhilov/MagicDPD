---
layout: post
title: "Есть ли ConWep в LS-DYNA?"
date: 2025-06-04T11:04:18+00:00
author: "Yury Novozhilov"
source: vk
images:
  - url: "/assets/images/2957.jpg"
---

Есть ли ConWep в LS-DYNA?

С одной стороны, в сети есть опубликованный исходный код реализации *LOAD_BLAST для DYNA2D/3D (бабушки современной Ansys LS-DYNA) (https://apps.dtic.mil/sti/citations/ADA322344), с другой стороны, в документации прямым текстом написано "ConWep code is neither embedded in nor coupled with LS-DYNA ". Так в чем же дело? А дело просто в путанице с названиями и торговыми марками.

1.ConWep (Программа по последствиям применения обычных вооружений) — это эмпирическая модель, предназначенная для оценки воздействия воздушных взрывов обычных (неядерных) взрывчатых веществ
2.ConWep — это вычислительный код, разработанный Инженерным корпусом армии США, который использует кривую Фридлендера для аппроксимации внутренней экспериментальной базы данных (https://apps.dtic.mil/sti/citations/ADA195867).

Вот и получается, что  ConWep методика фактически есть в LS-DYNA, но это не  ConWep код от  US Army Corps of Engineer.

https://apps.dtic.mil/sti/citations/ADA322344
https://apps.dtic.mil/sti/citations/ADA195867
