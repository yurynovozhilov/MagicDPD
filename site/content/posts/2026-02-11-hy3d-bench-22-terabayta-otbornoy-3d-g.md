---
author: Yury Novozhilov
date: 2026-02-11 09:54:10+00:00
images:
- url: /assets/images/3105.jpg
- url: /assets/images/3106.jpg
layout: post
link_previews:
- description: We’re on a journey to advance and democratize artificial intelligence
    through open source and open science.
  image: https://cdn-thumbnails.huggingface.co/social-thumbnails/datasets/tencent/HY3D-Bench.png
  title: tencent/HY3D-Bench · Datasets at Hugging Face
  url: https://huggingface.co/datasets/tencent/HY3D-Bench
source: vk
tags:
- Dataset
- AI
- ML
- HY3DBench
- Tencent
title: "\U0001F31F HY3D-Bench: 22 терабайта отборной 3D-геометрии."
---

Tencent Hunyuan вывалили в опенсорс монструозный пак HY3D-Bench на 22.5 ТБ и это подарок для всех, кто занимается 3D Gen и робототехникой.

Датасет разбит на 3 логических куска, каждый под свои задачи:

🟡Full-level Dataset (252K+ мешей, ~11 ТБ)
База с полностью замкнутой геометрией, без дырок и non-manifold артефактов, которыми обычно кишат сканы. Все нормализовано и готово к скармливанию в DiT или GAN. В комплекте идут сэмплы точек и мульти-вью рендеры.

🟡Part-level Dataset (240K+ объектов, ~5 ТБ)
Мёд для робототехников и тех, кто занимается geometric perception. Тут объекты с семантической сегментацией на части. Если учите сервоприводного друга манипуляциям или хотите генерить объекты кусками - вам сюда.

🟡Synthetic Dataset (125K+ объектов, ~6.5 ТБ)
Очевидная синтетика, чтобы закрыть редкие категории, которых нет в обычных датасетах. Охват - 1252 категории.

Ждем волну SOAT-level 3D-генераторов, дотюненных на этом наборе.


🟡Arxiv
🟡Датасет
🖥GitHub


@ai_machinelearning_big_data

https://huggingface.co/datasets/tencent/HY3D-Bench
https://arxiv.org/pdf/2602.03907
https://huggingface.co/datasets/tencent/HY3D-Bench
https://github.com/Tencent-Hunyuan/HY3D-Bench
