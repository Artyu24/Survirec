# groupe local : l'identifiant est résolu à l'apparition (p/gjoin), selon les entités du même groupe à proximité
data modify storage survirec:in cfg.grp set value -1
data modify storage survirec:in cfg.gl set from storage survirec:in cfg.loop
data modify storage survirec:in cfg.loop set value 0
