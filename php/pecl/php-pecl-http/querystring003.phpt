--TEST--
querystring offset set
--SKIPIF--
<?php
include "skipif.inc";
?>
--FILE--
<?php

echo "Test\n";

$qs = new http\QueryString("foo=bar&bar=baz");
echo $qs,"\n";
$qs["foo"] = "baz";
echo $qs,"\n";
?>
===DONE===
--EXPECT--
Test
foo=bar&bar=baz
foo=baz&bar=baz
===DONE===
