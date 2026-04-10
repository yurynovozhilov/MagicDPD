---
author: GlukRazor
date: 2019-02-08 15:00:59+00:00
images:
- url: /assets/images/1347.jpg
layout: post
link_previews:
- description: Main setup:*SECTION_SOLID_SPG_TITLE$#,secid, elform,aet,1,47,0$#,dx,
    dy, dz, ispline, kernel, lscale, smstep, swtime1.5,1.5,1.5,0,1,0.0,10,0.0$#, idam,
    fs,st...
  image: https://i.ytimg.com/vi/13lmxtjfD3A/maxresdefault.jpg
  title: 'Metal cutting in LS-DYNA with SPG: Effective plastiс strain'
  url: https://www.youtube.com/watch?v=13lmxtjfD3A
- description: Effective plastiс strainMain setup:*SECTION_SOLID_SPG_TITLE$#,secid,
    elform,aet,1,47,0$#,dx, dy, dz, ispline, kernel, lscale, smstep, swtime1.5,1.5,1.5,0,1,0...
  image: https://i.ytimg.com/vi/AGYxE3FfRAE/maxresdefault.jpg
  title: 'Metal cutting in LS-DYNA with SPG: Deformation'
  url: https://www.youtube.com/watch?v=AGYxE3FfRAE
source: vk
title: Моделирование резки металла — стажировка
---

Я опять ищу учеников! На этот раз это не бетоны — это резка, вырубка, фрезеровка и сверление металла. Все это обычно называют distructive manufacturing. Мы будем учиться моделировать эти технологические процессы самыми передовыми бессеточными методами, заложенными в LS-DYNA.


Чтобы лучше понимать о каких задачах пойдет речь, я подготовил небольшое демо расчета резки в Smooth Particle Galerkin (SPG) постановке. Этот полностью бессеточный метод похож по духу на SPH, но лишен его недостатков. Метод отлично подходит для моделирования хрупкого и пластического разрушения, дробления, пробивания. При этом деформация тела никак не сказывается на стабильности схемы или просадке шага по времени. Дополнительные материалы по теме: https://magicdpd.ru/tag/spg/



https://youtu.be/13lmxtjfD3A







https://youtu.be/AGYxE3FfRAE



А вот это уже видеопример от LSTC. Рассматривается работа адаптивного алгоритма Element-Free Galerkin (EFG): несмотря на то, что метод

https://magicdpd.ru/tag/spg/
https://youtu.be/13lmxtjfD3A
https://youtu.be/AGYxE3FfRAE
