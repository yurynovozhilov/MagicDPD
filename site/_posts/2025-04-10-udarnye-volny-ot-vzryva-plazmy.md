---
layout: post
title: "Ударные волны от \"взрыва\" плазмы"
date: 2025-04-10T12:04:29+00:00
author: "Yury Novozhilov"
source: vk
original_url: https://vk.com/wall-97265142_2923
images:
  - url: "/assets/images/2923.jpg"
---

В связи с разгулом электрического транспорта я стал получать запросы по моделированию "взрыва" плазмы, вызванной дуговым разрядом в воздухе. Пришлось разобраться в тема. Оказывается, что в первом приближении это можно смоделировать на раз в обычной ALE постановке LS-DYNA. Заодно я теперь знаю, как и зачем применять *EOS_LINEAR_POLYNOMIAL_WITH_ENERGY_LEAK

А по ссылки две статьи, показывающие промышленное применение для электрогидравлической штамповки металла:
https://www.dynalook.com/conferences/13th-international-ls-dyna-conference/metal-forming/simulation-of-high-voltage-discharge-channel-in-waterat-electro-hydraulic-forming-using-ls-dyna-r
https://www.dynalook.com/conferences/12th-european-ls-dyna-conference-2019/forming/woo_pusan_national_university.pdf
