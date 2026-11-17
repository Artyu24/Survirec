# Relance une séquence déjà chargée dans CE monde (sans les données)
$data modify storage survirec:in a set value {name:"$(name)",entity:"$(entity)",size:$(size),loop:$(loop),speed:$(speed),offset:$(offset),tag:"$(tag)",pose:"$(pose)",skin:"$(skin)",texture:"$(texture)",head:"$(head)",chest:"$(chest)",legs:"$(legs)",feet:"$(feet)",mainhand:"$(mainhand)",offhand:"$(offhand)"}
$execute positioned $(pos) run function survirec:p/spawn
