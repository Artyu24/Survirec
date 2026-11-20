function survirec:v1/private/bk/read
execute if data storage survirec:bk r{id:""} run return 0
execute if block ~ ~ ~ #minecraft:buttons run return run function survirec:v1/private/i/u_button
execute if block ~ ~ ~ minecraft:lever run return run function survirec:v1/private/i/u_lever
execute if block ~ ~ ~ #survirec:doors_open run return run function survirec:v1/private/i/u_door
execute if block ~ ~ ~ #survirec:trapdoors_open run return run function survirec:v1/private/i/u_open
execute if block ~ ~ ~ #minecraft:fence_gates run return run function survirec:v1/private/i/u_open
