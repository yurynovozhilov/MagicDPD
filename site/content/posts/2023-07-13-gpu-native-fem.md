---
date: 2023-07-13 15:01:32+00:00
link_previews:
- description: Explore a wide array of DPU- and GPU-accelerated applications, tools,
    and services.
  image: https://www.nvidia.com/content/dam/en-zz/Solutions/homepage/v2/mfg/nvidia-og-image-1200x630.jpg
  title: NVIDIA Accelerated Application Catalog
  url: https://www.nvidia.com/en-us/gpu-accelerated-applications/?filter=eyJJbmR1c3RyeVNlZ21lbnQiOlsiSFBDIC8gU3VwZXJjb21wdXRpbmciXSwid29ya2xvYWRzIjpbIlNpbXVsYXRpb24gLyBNb2RlbGluZyAvIERlc2lnbiJdfQ==
original_url: https://t.me/MagicDPD/2470
source: tg
title: GPU native FEM
---

Я бы хотел сегодня с вам порассуждать, и послушать ваши комментарии. Наверно мало кто будет спорить, что GPU-native решaтeли выполняют расчеты на порядки быстрее, чем традиционный код, исполняемый на CPU. Также, моделирование на основе методов частиц (DEM, SPH, MPS, MPM, LBM) кажется достаточно просто реализуется на GPU. По крайней мере, большинство кодов с такой направленностью неистово взлетают, когда могут дотянуться до видеокарты от NVIDIA.

Сейчас мы видим, что GPU-native решетили понемногу приходят в мир большого промышленного CFD. В прошлом году Ansys Fluent стал первым тяжелым CFD кодом, который получил GPU-native решатель. В этом году что-то похожее выкатил Star-CCM+. 

Но у меня есть вопрос. А что у нас с задачами прочности? Уже на протяжении наверно 5 лет единственным GPU-native прочностным решателем остается Ansys Discovery Live (он же одновременно был и самым первым GPU-native CFD решателем на рынке). Discovery Live безусловно знаковый продукт, который пока так никто и не смог скопировать. 

Но, серьезно, где конкурирующие промышленный FEM коды с GPU-native подходом? Почему мир тяжелого FEM моделирования замер на GPU-offload. Более того, в основном реализована поддержка только прямых решателей СЛАУ, а реализация ускорения итеративных решателей все еще является чем-то особенным. 

Какие есть у вас идеи?

https://www.nvidia.com/en-us/gpu-accelerated-applications/?filter=eyJJbmR1c3RyeVNlZ21lbnQiOlsiSFBDIC8gU3VwZXJjb21wdXRpbmciXSwid29ya2xvYWRzIjpbIlNpbXVsYXRpb24gLyBNb2RlbGluZyAvIERlc2lnbiJdfQ==
