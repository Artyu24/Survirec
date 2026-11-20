data modify storage survirec:bk ex set value []
execute if score #nop survirec.v matches 1 run data modify storage survirec:bk ex append value "open=true"
execute if score #nop survirec.v matches 0 run data modify storage survirec:bk ex append value "open=false"
execute if score #bpw survirec.v matches 1 run data modify storage survirec:bk ex append value "powered=true"
execute if score #bpw survirec.v matches 0 run data modify storage survirec:bk ex append value "powered=false"
