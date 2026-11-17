# execute as @p run function survirec:challenge_g {id:"a",time:5,group:"salle1"}
$data merge storage survirec:c {id:"$(id)",time:$(time),group:"$(group)"}
function survirec:c/start
