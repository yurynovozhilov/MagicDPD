---
date: 2025-11-18 11:53:07+00:00
images:
- url: /assets/images/3062.jpg
link_previews:
- description: Accelerated computing and advanced simulation technologies are changing
    the game for the traditionally experiment-heavy power generation industry by offering
    unparalleled efficiency and precision. Full-scale industrial models with complex
    design feat...
  image: https://community.cadence.com/cfs-file/__key/communityserver-blogs-components-weblogfiles/00-00-00-01-43/0451.SolarTurbines.png
  title: Cadence, NVIDIA, and Solar Turbines Collaborate on AI Physics
  url: https://community.cadence.com/cadence_blogs_8/b/corporate-news/posts/cadence-nvidia-and-solar-turbines-collaborate-on-ai-physics
original_url: https://t.me/MagicDPD/3062
source: tg
title: 1 миллиард ячеек в CFD расчете на GPU за сутки
---

Cadence, NVIDIA, и Solar Turbines (часть Caterpillar) отчитались о том, что смогли за одни сутки обсчитать 1 миллиард ячеек используя CFD решатель Fidelity Charles Solver от Cadence. Charles Solver, как и все современные CFD решатели умеет в GPU-native. И для данного расчета они взяли сервера NVIDIA GB200 VL72 набитые карточками NVIDIA Blackwell B200 - все было 512 GPU (безумно много для CFD и смешно для AI). Всю это вычислительную силу заставили решать задачу турбулентного горения (flamelet progress variable, FPV). 

Вот мы и дожили, когда мы говорим не про десятки тысяч ядер CPU, а про сотни GPU. Даешь DNS на GPU!

Пресс релиз: https://community.cadence.com/cadence_blogs_8/b/corporate-news/posts/cadence-nvidia-and-solar-turbines-collaborate-on-ai-physics

Научная статья: https://doi.org/10.1115/GT2025-151173
