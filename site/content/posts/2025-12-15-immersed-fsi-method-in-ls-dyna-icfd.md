---
author: Yury Novozhilov
date: 2025-12-15 15:51:17+00:00
layout: post
link_previews:
- description: 'CFD of a 2026 Formula 1 (F1) car using ICFD LS-DYNA Solver.Making
    use of the new immersed technology in ICFD.Base Geometry: https://grabcad.com/library/f1-20...'
  image: https://i.ytimg.com/vi/kiHG2coygo0/maxresdefault.jpg?sqp=-oaymwEmCIAKENAF8quKqQMa8AEB-AGSCYAC0AWKAgwIABABGH8gIyhTMA8=&rs=AOn4CLACZcoRuEkj28Qs7aMWcc5P1G7k7g
  title: CFD of a 2026 Formula 1 (F1) car using ICFD LS-DYNA Solver.
  url: https://www.youtube.com/watch?v=kiHG2coygo0
source: vk
title: Immersed FSI method in LS-DYNA ICFD
---

В LS-DYNA сейчас идет активное развитие FSI на основе метода погруженной границы. Этот метод очень востребован именно для области "экстремального FSI" в котором работает дайна. Суть метода в том, что вам не надо явно разрешать интерфейс на уровне сетки. Все работает, как мы привыкли для ALE постановки. Кроме того, что модель становиться существенно проще в постановке мы получаем и другие бонусы: возможность не заморачиваться с сеткой в клапанах и пережимаемых каналах, работа с очень грязной геометрией, работа с эрозией материала.

Вот, например, демка с последней конференции: взяли произвольную модель с GrabCAD, построили на ней какую-то сетку, и просто засунули все это в виртуальную аэродинамическую трубу. Единственно ограничение сейчас заключается в том, что работает такой FSI только с оболочками.

https://youtu.be/kiHG2coygo0?si=6Nn6ha1rteMSXYZ5

[CFD of a 2026 Formula 1 (F1) car using ICFD LS-DYNA Solver.](https://youtu.be/kiHG2coygo0?si=6Nn6ha1rteMSXYZ5)
