# execute as @p run function survirec:challenge {id:"epreuve1",time:30}
$data merge storage survirec:c {id:"$(id)",time:$(time),group:"main"}
function survirec:c/start
