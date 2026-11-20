# positionné sur un bloc : survirec:bk r.id (vide si inconnu), pl (propriétés), drapeaux #bfc #bhl #bpt #bop #bpw
data modify storage survirec:bk r set value {id:"",leaf:""}
data modify storage survirec:bk pl set value []
scoreboard players set #bop survirec.v 0
scoreboard players set #bpw survirec.v 0
scoreboard players set #bhl survirec.v 0
scoreboard players set #bpt survirec.v 0
scoreboard players set #bfc survirec.v 0
scoreboard players set #bfa survirec.v 0
function survirec:v1/private/bk/t/n1
execute if data storage survirec:bk r{id:""} run return fail
function survirec:v1/private/bk/props with storage survirec:bk r
