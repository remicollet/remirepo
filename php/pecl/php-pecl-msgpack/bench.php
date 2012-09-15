<?php

//ini_set('memory_limit' ,'128M');

$ary = get_loaded_extensions();
for($i=0; $i<pow(2, 9); $i++){
    $ary = array_merge($ary, range(0, 1024));
	$ary[] = md5("$i");
}

echo "count:".count($ary)."\n";

function getSize($ary)
{
    if (ini_get('mbstring.func_overload') & 2 && function_exists('mb_strlen')) {
        $size = mb_strlen($ary, 'ASCII');
    } else {
        $size = strlen($ary);
    }

    return $size;
}

echo "----\n";
echo "PHP\n";
$a = microtime(true);
$packed = serialize($ary);
$b = microtime(true);
echo ($refpck=($b-$a)) . " sec, " . ($refsize=getSize($packed)) . " bytes\n";

$a = microtime(true);
$pack = unserialize($packed);
$b = microtime(true);
echo ($refunp=($b-$a)) . " sec\n";


echo "----\n";
echo "IgBinary\n";
$a = microtime(true);
$packed = igbinary_serialize($ary);
$b = microtime(true);
echo ($t=($b-$a)) . " sec, " . round($t*100/$refpck) . "%, ". ($x=getSize($packed)) . " bytes, ".round($x*100/$refsize)."%\n";

$a = microtime(true);
$pack = igbinary_unserialize($packed);
$b = microtime(true);
echo ($t=($b-$a)) . " sec, " . round($t*100/$refunp) . "%\n";


echo "----\n";
echo "MessagePack\n";
$a = microtime(true);
$packed = msgpack_pack($ary);
$b = microtime(true);
echo ($t=($b-$a)) . " sec, " . round($t*100/$refpck) . "%, ". ($x=getSize($packed)) . " bytes, ".round($x*100/$refsize)."%\n";

$a = microtime(true);
$pack = msgpack_unpack($packed);
$b = microtime(true);
echo ($t=($b-$a)) . " sec, " . round($t*100/$refunp) . "%\n";


echo "----\n";
echo "JSON\n";
$a = microtime(true);
$jsoned = json_encode($ary);
$b = microtime(true);
echo ($t=($b-$a)) . " sec, " . round($t*100/$refpck) . "%, ". ($x=getSize($jsoned)) . " bytes, ".round($x*100/$refsize)."%\n";

$a = microtime(true);
$json = json_decode($jsoned);
$b = microtime(true);
echo ($t=($b-$a)) . " sec, " . round($t*100/$refunp) . "%\n";


?>
