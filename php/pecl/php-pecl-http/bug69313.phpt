--TEST--
Bug #69313 (http\Client doesn't send GET body)
--SKIPIF--
<?php
include "./skipif.inc";
skip_client_test();
?>
--FILE--
<?php


include "helper/server.inc";

echo "Test\n";

server("proxy.inc", function($port, $stdin, $stdout, $stderr) {
	$request = new http\Client\Request("GET", "http://localhost:$port/");
	$request->setHeader("Content-Type", "text/plain");
	$request->getBody()->append("foo");
	$client = new http\Client();
	$client->enqueue($request);
	$client->send();
	echo $client->getResponse();
});

?>

Done
--EXPECTF--
Test
HTTP/1.1 200 OK
Accept-Ranges: bytes
Etag: "%s"
X-Original-Transfer-Encoding: chunked
Content-Length: %d

GET / HTTP/1.1
User-Agent: %s
Host: localhost:%d
Accept: */*
Content-Type: text/plain
Content-Length: 3
X-Original-Content-Length: 3

foo
Done
