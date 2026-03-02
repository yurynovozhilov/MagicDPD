---
date: 2019-02-20 17:00:40+00:00
images:
- url: /assets/images/1361.jpg
link_previews:
- description: Icebreaker crossing a sheet of thick hard ice. Side view. Simulation
    run using DEMPack.
  image: https://i.ytimg.com/vi/hzYz4mtF7tI/hqdefault.jpg
  title: Icebreaker thick hard ice side view
  url: https://www.youtube.com/watch?v=hzYz4mtF7tI
- description: Ship model cruising over an ice layer. DEM results obtained with DEMPACK
  image: https://i.ytimg.com/vi/p_OM0lg1MtQ/maxresdefault.jpg
  title: Ships in ice 01
  url: https://www.youtube.com/watch?v=p_OM0lg1MtQ
- description: DEM results obtained with DEMPack
  image: https://i.ytimg.com/vi/VdZupL4bIU4/maxresdefault.jpg?sqp=-oaymwEmCIAKENAF8quKqQMa8AEB-AHyB4AC0AWKAgwIABABGFcgVyhlMA8=&rs=AOn4CLAijkNBUZTlr1kwAT6ajZ4cwpCLgw
  title: Icebreaker sailing completely surrounded by ice - Hard Ice
  url: https://www.youtube.com/watch?v=VdZupL4bIU4
original_url: https://t.me/MagicDPD/1361
source: tg
title: Ледокол против льда
---

https://www.youtube.com/watch?v=hzYz4mtF7tI



Одно время ко мне был просто вал запросов по моделированию льда и закритической прочности бортов судов ледового касса. Тогда я даже читал лекции по UMAT для LS-DYNA и приводил ссылки на готовые исходные коды для моделей льда. Однако тут на глаза мне попалась интересная серия видео, посвященная DEM подходу по моделированию разрушения льда ледоколом, и это очень интересный подход.



  https://www.youtube.com/watch?v=p_OM0lg1MtQ



В целом, мне уже встречались статьи, где разрушение льда считалось через разрушение когезивных контактов между КЭ кубиками, однако, использование DEM тут может дать более интересный результат.



  https://www.youtube.com/watch?v=VdZupL4bIU4



Конечно, математика разрушения связей в DEM сильно проще, чем прямое моделирование разрушения когезивных контактов, зато количество учитываемых DEM частиц в задаче легко может исчисляться миллионами. Тем более, что большинство DEM кодов (как, например, наш любимый Rocky
