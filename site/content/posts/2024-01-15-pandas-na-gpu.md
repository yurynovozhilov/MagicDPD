---
layout: post
title: "Pandas на GPU"
date: 2024-01-15T15:00:42+00:00
author: "Yury Novozhilov"
source: vk
---

Pandas на GPU

Pandas я люблю еще с тех пор, как мне надо было делать обработку спектров отклика рассчитанных LS-DYNA для оборудования АЭС, в которую бил самолет. Вот тут сеть рассказзал мне про интересную библиотеку cuDF.

cuDF - это библиотека GPU DataFrame для загрузки, объединения, фильтрации и других манипуляций с данными. cuDF использует libcudf, молниеносно быструю библиотеку датафреймов C++/CUDA и столбчатый формат Apache Arrow, чтобы предоставить API pandas с GPU-ускорением.

https://github.com/rapidsai/cudf

[GitHub - rapidsai/cudf: cuDF - GPU DataFrame Library](https://github.com/rapidsai/cudf)
