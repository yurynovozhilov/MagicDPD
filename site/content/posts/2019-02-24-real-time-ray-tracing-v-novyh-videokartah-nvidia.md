---
date: 2019-02-24 17:00:19+00:00
images:
- url: /assets/images/1365.jpg
link_previews:
- description: 4A Games are bringing real-time Ray Tracing to Metro Exodus! At NVIDIA’s
    Gaming Celebration event in Cologne, it was revealed how 4A Games would use NVIDIA
    R...
  image: https://i.ytimg.com/vi/Ms7d-3Dprio/maxresdefault.jpg
  title: 'Metro Exodus: GeForce RTX Real-Time Ray Traced Global Illumination Demo'
  url: https://youtu.be/Ms7d-3Dprio
- description: 'NVIDIA DLSS technology is now available in Battlefield V, improving
    DXR Ray Tracing performance by up to 40%!Learn More: https://www.nvidia.com/en-us/geforce...'
  image: https://i.ytimg.com/vi/nshbUzdBlq8/maxresdefault.jpg
  title: 'Battlefield V: Now With NVIDIA DLSS – Up to 40% Performance Boost!'
  url: https://youtu.be/nshbUzdBlq8
original_url: https://t.me/MagicDPD/1365
source: tg
title: Real-Time Ray Tracing в новых видеокартах NVIDIA
---

NVIDIA в новом поколении видеокарты RTX показала очень крутую штуку: расчет распространения лучей света в реальном времени. Модуль для такого расчета делает игры еще зрелищнее. 



  https://youtu.be/Ms7d-3Dprio



Однако, если вы не геймер, а расчетчик, то покупать GeForce RTX серии 2080 вам не стоит. Ray Tracing модуль никак не поможет ускорить DEM, FEM или CFD расчеты ни в одном профессиональном CAE решателе, с которыми я имел дело (Тут я имею виду Rocky DEM и все возможне коды под крылом ANSYS, скроме Optis, так как про него пока мало знаний). Так что, вам пока придётся брать Tesla или Quadro с высокой производительностью в операциях двойной точности и большим объемом памяти.



  https://youtu.be/nshbUzdBlq8



А если хочется попробовать GeForce для ускорения расчетов, то можно провести эксперимент с установкой переменной окружения ANSGPU_OVERRIDE=1 — и тут опять круче 1080 вам ничего не нужно. Это решение официально не поддерживается, но на
