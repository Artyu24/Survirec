# Équipement imposé depuis le command block : si un champ est rempli, l'équipement enregistré ne change plus après le départ
execute unless data storage survirec:in a{head:""} run data modify storage survirec:in s set value {slot:"armor.head"}
execute unless data storage survirec:in a{head:""} run data modify storage survirec:in s.item set from storage survirec:in a.head
execute unless data storage survirec:in a{head:""} run function survirec:v1/private/p/slot with storage survirec:in s
execute unless data storage survirec:in a{head:""} run scoreboard players set @s survirec.ov 1
execute unless data storage survirec:in a{chest:""} run data modify storage survirec:in s set value {slot:"armor.chest"}
execute unless data storage survirec:in a{chest:""} run data modify storage survirec:in s.item set from storage survirec:in a.chest
execute unless data storage survirec:in a{chest:""} run function survirec:v1/private/p/slot with storage survirec:in s
execute unless data storage survirec:in a{chest:""} run scoreboard players set @s survirec.ov 1
execute unless data storage survirec:in a{legs:""} run data modify storage survirec:in s set value {slot:"armor.legs"}
execute unless data storage survirec:in a{legs:""} run data modify storage survirec:in s.item set from storage survirec:in a.legs
execute unless data storage survirec:in a{legs:""} run function survirec:v1/private/p/slot with storage survirec:in s
execute unless data storage survirec:in a{legs:""} run scoreboard players set @s survirec.ov 1
execute unless data storage survirec:in a{feet:""} run data modify storage survirec:in s set value {slot:"armor.feet"}
execute unless data storage survirec:in a{feet:""} run data modify storage survirec:in s.item set from storage survirec:in a.feet
execute unless data storage survirec:in a{feet:""} run function survirec:v1/private/p/slot with storage survirec:in s
execute unless data storage survirec:in a{feet:""} run scoreboard players set @s survirec.ov 1
execute unless data storage survirec:in a{mainhand:""} run data modify storage survirec:in s set value {slot:"weapon.mainhand"}
execute unless data storage survirec:in a{mainhand:""} run data modify storage survirec:in s.item set from storage survirec:in a.mainhand
execute unless data storage survirec:in a{mainhand:""} run function survirec:v1/private/p/slot with storage survirec:in s
execute unless data storage survirec:in a{mainhand:""} run scoreboard players set @s survirec.ov 1
execute unless data storage survirec:in a{offhand:""} run data modify storage survirec:in s set value {slot:"weapon.offhand"}
execute unless data storage survirec:in a{offhand:""} run data modify storage survirec:in s.item set from storage survirec:in a.offhand
execute unless data storage survirec:in a{offhand:""} run function survirec:v1/private/p/slot with storage survirec:in s
execute unless data storage survirec:in a{offhand:""} run scoreboard players set @s survirec.ov 1
