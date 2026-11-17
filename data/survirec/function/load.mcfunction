# Objectifs
scoreboard objectives add survirec.v dummy
scoreboard objectives add survirec.id dummy
scoreboard objectives add survirec.run dummy
scoreboard objectives add survirec.seg dummy
scoreboard objectives add survirec.len dummy
scoreboard objectives add survirec.n100 dummy
scoreboard objectives add survirec.pr dummy
scoreboard objectives add survirec.spd dummy
scoreboard objectives add survirec.lp dummy
scoreboard objectives add survirec.ax dummy
scoreboard objectives add survirec.ay dummy
scoreboard objectives add survirec.az dummy
scoreboard objectives add survirec.yw0 dummy
scoreboard objectives add survirec.pt0 dummy
scoreboard objectives add survirec.bx dummy
scoreboard objectives add survirec.by dummy
scoreboard objectives add survirec.bz dummy
scoreboard objectives add survirec.byw dummy
scoreboard objectives add survirec.bpt dummy
scoreboard objectives add survirec.dx dummy
scoreboard objectives add survirec.dy dummy
scoreboard objectives add survirec.dz dummy
scoreboard objectives add survirec.dyw dummy
scoreboard objectives add survirec.dpt dummy
scoreboard objectives add survirec.fl dummy
scoreboard objectives add survirec.fn dummy
scoreboard objectives add survirec.fx dummy
scoreboard objectives add survirec.ek dummy
scoreboard objectives add survirec.ei dummy
scoreboard objectives add survirec.ov dummy
scoreboard objectives add survirec.snp dummy
scoreboard objectives add survirec.swp dummy
scoreboard objectives add survirec.glp dummy
scoreboard objectives add survirec.st dummy
scoreboard objectives add survirec.pl dummy
scoreboard objectives add survirec.near dummy
scoreboard objectives add survirec.rb dummy
scoreboard objectives add survirec.sn minecraft.custom:minecraft.sneak_time
scoreboard objectives add survirec.sw minecraft.custom:minecraft.swim_one_cm
scoreboard objectives add survirec.gl minecraft.custom:minecraft.aviate_one_cm
scoreboard objectives add survirec.use minecraft.used:minecraft.carrot_on_a_stick
scoreboard objectives add survirec.trg trigger
scoreboard players set #5 survirec.v 5
scoreboard players set #10 survirec.v 10
scoreboard players set #20 survirec.v 20
scoreboard players set #60 survirec.v 60
execute unless data storage survirec:cfg r run data modify storage survirec:cfg r set value 128
execute unless score #rec survirec.v = #rec survirec.v run scoreboard players set #rec survirec.v 0
execute unless score #id survirec.v = #id survirec.v run scoreboard players set #id survirec.v 0
execute unless score #gt survirec.v = #gt survirec.v run scoreboard players set #gt survirec.v 0
scoreboard objectives add survirec.hs dummy
scoreboard objectives add survirec.si dummy
scoreboard objectives add survirec.sk dummy
scoreboard objectives add survirec.pid dummy
execute unless score #pid survirec.v = #pid survirec.v run scoreboard players set #pid survirec.v 0
execute unless score #chal survirec.v = #chal survirec.v run scoreboard players set #chal survirec.v 0
scoreboard objectives add survirec.grp dummy
scoreboard objectives add survirec.rs dummy
execute unless score #pend survirec.v = #pend survirec.v run scoreboard players set #pend survirec.v 0
execute unless score #gid survirec.v = #gid survirec.v run scoreboard players set #gid survirec.v 0
scoreboard objectives add survirec.dv dummy
