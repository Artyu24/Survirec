$data modify storage survirec:lib recs.$(name) set from storage survirec:tmp rec
$data modify storage survirec:data seqs.$(name) set from storage survirec:tmp seq
$data remove storage survirec:lib names[{name:"$(name)"}]
$data modify storage survirec:lib names append value {name:"$(name)",pid:0}
