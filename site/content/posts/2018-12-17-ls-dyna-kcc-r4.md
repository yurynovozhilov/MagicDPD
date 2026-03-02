---
title: "LS-DYNA KCC R4"
date: 2018-12-17T17:00:17+00:00
source: tg
original_url: "https://t.me/MagicDPD/1269"
images:
  - url: "/assets/images/1269.jpg"
---

Случайно наткнулся на материалы одной около военной конференции, где подробно рассматривали задачу пробивания неармированной бетонной плиты. Считали, как водится, в LS-DYNA. Но самое интересное тут в моделях материалов. При этом использовали такие важные бетонные модели как:

  
    
      
        
          Karagozian & Case Concrete Model, Release 3 (*MAT_CONCRETE_DAMAGE_REL3)
        
        
          Continuous Surface Cap Model (*MAT_CSCM)
        
        
          Riedel-Hiermaier-Thoma Model (*MAT_RHT)
        
        
          Winfrith Concrete Model (*MAT_WINFRITH_CONCRETE)
        
        
          Johnson-Holmquist Concrete Model (*MAT_JOHNSON_HOLMQUIST_CONCRETE)
        
        
          Karagozian & Case Concrete Model, Release 4
        
      
    
  


  
     
  





Тут конечно самое интересное, это 4-ая версия KCC модели, о которой рассказывает сотрудник компании Karagozian & Case. Мимо такого доклада не стоит проходить!




Для корректного расчета пробивания использовалось адаптивное переключение лагранжевого МКЭ в SPH по мере "смерти элементов", что является одним из передовых правильных подходов в задачах терминальной баллистики. 
Слайды презентации:
https://ndiastorage.blob.core.usgovcloudapi.net/ndia/2018/intexpsafety/Durant.pdf
Сопутствующая статья:
https://ndiastorage.blob.core.usgovcloudapi.net/ndia/2018/intexpsafety/DurantPaper.pdf
#Concrete #CSCM #DEFINEADAPTIVESOLIDTOSPH #KCC #RHT #SPH
http://bit.ly/2UOZ82Q
