# état complet tel quel (ouvert / alimenté compris)
data modify storage survirec:bk ex set value []
execute if score #bop survirec.v matches 1 run data modify storage survirec:bk ex append value "open=true"
execute if score #bpw survirec.v matches 1 run data modify storage survirec:bk ex append value "powered=true"
function survirec:v1/private/bk/full
