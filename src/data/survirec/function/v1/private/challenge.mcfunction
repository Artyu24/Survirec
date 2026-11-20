# execute as @p run function #survirec:v1/challenge {with:{id:"a",time:5,group:"salle1",sync:0,tp_back:1}}
$data merge storage survirec:cin {id:"$(id)",time:$(time),group:"$(group)",sync:$(sync),tp_back:$(tp_back)}
function survirec:v1/private/c/start
