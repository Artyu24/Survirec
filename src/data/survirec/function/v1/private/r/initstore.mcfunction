$data modify storage survirec:rec p.p$(pid).meta set from storage survirec:tmp meta
$data modify storage survirec:rec p.p$(pid).d set value []
$data modify storage survirec:rec p.p$(pid).chunks set value []
$data modify storage survirec:rec p.p$(pid).e set value []
$data modify storage survirec:rec p.p$(pid).s set value []
$data remove storage survirec:rec p.p$(pid).eq
$data modify storage survirec:rec p.p$(pid).a set value []
$data modify storage survirec:rec p.p$(pid).wb set value []
