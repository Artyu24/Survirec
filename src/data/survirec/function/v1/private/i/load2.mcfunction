$data modify storage survirec:t row set from storage survirec:data seqs.$(name).d[$(s)]
execute store result score @s survirec.dx run data get storage survirec:t row[0]
execute store result score @s survirec.dy run data get storage survirec:t row[1]
execute store result score @s survirec.dz run data get storage survirec:t row[2]
execute store result score @s survirec.dyw run data get storage survirec:t row[3]
execute store result score @s survirec.dpt run data get storage survirec:t row[4]
execute store result score @s survirec.fn run data get storage survirec:t row[5]
scoreboard players operation #ost survirec.v = @s survirec.st
scoreboard players set @s survirec.st 0
execute if score @s survirec.dx matches 0 if score @s survirec.dy matches 0 if score @s survirec.dz matches 0 if score @s survirec.dyw matches 0 if score @s survirec.dpt matches 0 run scoreboard players set @s survirec.st 1
execute unless score @s survirec.st matches 1 run scoreboard players set @s survirec.pl 0
execute unless score #ost survirec.v matches 1 run scoreboard players set @s survirec.pl 0
scoreboard players set @s survirec.rb 0
execute if score @s survirec.fx matches 0 if score @s survirec.fn matches 2..7 unless score @s survirec.dyw matches 0 run scoreboard players set @s survirec.rb 1
execute if score @s survirec.fx matches 0 if score @s survirec.fn matches 2..7 unless score @s survirec.fn = @s survirec.fl run scoreboard players set @s survirec.rb 1
execute if score @s survirec.rb matches 1 run scoreboard players set @s survirec.pl 0
execute if score @s survirec.fx matches 0 unless score @s survirec.fn = @s survirec.fl run function survirec:v1/private/i/pose
