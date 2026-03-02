---
date: 2024-03-22 14:02:08+00:00
link_previews:
- description: 'Transient Automotive Aerodynamic Study using LBM-based GPU-accelerated
    Pacefish CFD solverModel: DrivAer Car Shape AutoCFD4 config @ 140 kph | 87 mphCFD:
    670...'
  image: https://i.ytimg.com/vi/grKwuQMo4V0/maxresdefault.jpg?sqp=-oaymwEmCIAKENAF8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGBAgZShSMA8=&rs=AOn4CLCPQbOLadgQXlmETNq7B-Dc4Peu7Q
  title: Pacefish CFD runs AutoCFD4 setup at ~670 million cells for 4.7 real-time
    seconds.
  url: https://www.youtube.com/watch?v=grKwuQMo4V0
original_url: https://t.me/MagicDPD/2674
source: tg
title: Pacefish CFD
---

Очередная любопытная находка. Компания Numeric Systems GmbH пилит свой LBM решатель. Естественно, он GPU-native. Но это еще не все. Говорят, что у этого кода есть уникальная для LBM подхода фишка: он умеет как-то хитро использовать смесь из RANS и LES подходов к моделированию турбулентносит. Так, в основном объеме код считате согласно k-omega-SST модели, а у стенок применяется модель отсоединенных вихрей.  Короче, прошу помощи из зала, что бы оценить величие или ничтожность данного подхода. 

https://www.youtube.com/watch?v=grKwuQMo4V0
