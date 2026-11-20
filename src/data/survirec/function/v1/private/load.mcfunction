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
scoreboard players set #5 survirec.v 5
scoreboard players set #10 survirec.v 10
scoreboard players set #20 survirec.v 20
scoreboard players set #60 survirec.v 60
execute unless data storage survirec:cfg r run data modify storage survirec:cfg r set value 128
execute unless score #id survirec.v = #id survirec.v run scoreboard players set #id survirec.v 0
execute unless score #gt survirec.v = #gt survirec.v run scoreboard players set #gt survirec.v 0
scoreboard objectives add survirec.hs dummy
scoreboard objectives add survirec.rng dummy
scoreboard objectives add survirec.gloop dummy
scoreboard objectives add survirec.gs dummy
scoreboard players set #2 survirec.v 2
scoreboard objectives add survirec.si dummy
scoreboard objectives add survirec.sk dummy
scoreboard objectives add survirec.pid dummy
execute unless score #pid survirec.v = #pid survirec.v run scoreboard players set #pid survirec.v 0
scoreboard objectives add survirec.grp dummy
scoreboard objectives add survirec.rs dummy
execute unless score #pend survirec.v = #pend survirec.v run scoreboard players set #pend survirec.v 0
execute unless score #gid survirec.v = #gid survirec.v run scoreboard players set #gid survirec.v 0
scoreboard objectives add survirec.dv dummy

# état d'enregistrement, par joueur
scoreboard objectives add survirec.rpx dummy
scoreboard objectives add survirec.rpy dummy
scoreboard objectives add survirec.rpz dummy
scoreboard objectives add survirec.rpyw dummy
scoreboard objectives add survirec.rppt dummy
scoreboard objectives add survirec.rox dummy
scoreboard objectives add survirec.roy dummy
scoreboard objectives add survirec.roz dummy
scoreboard objectives add survirec.royw dummy
scoreboard objectives add survirec.ropt dummy
scoreboard objectives add survirec.rkf dummy
scoreboard objectives add survirec.rkt dummy
scoreboard objectives add survirec.rtk dummy
scoreboard objectives add survirec.rtime dummy
scoreboard objectives add survirec.revery dummy
scoreboard objectives add survirec.rlsw dummy
scoreboard objectives add survirec.rchal dummy
scoreboard objectives add survirec.rcdur dummy
scoreboard objectives add survirec.rwg dummy
scoreboard objectives add survirec.ratype dummy
scoreboard objectives add survirec.left minecraft.custom:minecraft.leave_game
function survirec:v1/private/menu/texture
# actions (enregistrement)
scoreboard objectives add survirec.rbx dummy
scoreboard objectives add survirec.rby dummy
scoreboard objectives add survirec.rbz dummy
scoreboard objectives add survirec.rlk dummy
scoreboard objectives add survirec.ruf dummy
scoreboard objectives add survirec.rplf dummy
scoreboard objectives add survirec.rux dummy
scoreboard objectives add survirec.ruy dummy
scoreboard objectives add survirec.ruz dummy
scoreboard objectives add survirec.rut dummy
scoreboard objectives add survirec.ratk dummy
# actions (rejeu)
scoreboard objectives add survirec.bbx dummy
scoreboard objectives add survirec.bby dummy
scoreboard objectives add survirec.bbz dummy
scoreboard objectives add survirec.ha dummy
scoreboard objectives add survirec.ai dummy
scoreboard objectives add survirec.ak dummy
scoreboard objectives add survirec.rst dummy
scoreboard objectives add survirec.hitp dummy
scoreboard objectives add survirec.rlt dummy
scoreboard players set #7 survirec.v 7
scoreboard players set #49 survirec.v 49
execute unless score #vs survirec.v = #vs survirec.v run scoreboard players set #vs survirec.v 0
# dimension de sauvegarde (copies des blocs modifiés par les entités)
execute in survirec:vault run forceload add 0 0 47 15
scoreboard players set #4 survirec.v 4
execute unless score #step survirec.v = #step survirec.v run scoreboard players set #step survirec.v 2
scoreboard players set #16 survirec.v 16
scoreboard players set #1536 survirec.v 1536
execute unless score #cs survirec.v = #cs survirec.v run scoreboard players set #cs survirec.v 0
scoreboard players set #m1 survirec.v -1
scoreboard objectives add survirec.rlkx dummy
scoreboard objectives add survirec.rlky dummy
scoreboard objectives add survirec.rlkz dummy
scoreboard objectives add survirec.rsb dummy
scoreboard objectives add survirec.cbx dummy
scoreboard objectives add survirec.cby dummy
scoreboard objectives add survirec.cbz dummy
scoreboard objectives add survirec.due dummy
execute unless score #npulse survirec.v = #npulse survirec.v run scoreboard players set #npulse survirec.v 0
