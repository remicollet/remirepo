#!/usr/bin/php
<?php

include "tcpdf.php";

function help() {
	echo "usage ".$_SERVER['argv'][0]." [ options ] fontfile [ fontfile ... ]\n";

	echo "\noptions:\n";
	echo "\t-t\n\t--type      TrueTypeUnicode, TrueType, Type1, CID0JP = CID-0 Japanese, CID0KR = CID-0 Korean, CID0CS = CID-0 Chinese Simplified, CID0CT\n";
	echo "\t-o\n\t--out       Output path\n";
	echo "\t-l\n\t--link      Create link to original font (not a copy)\n";
}

$fontfiles = array();
$type      = '';
$out       = K_PATH_FONTS;
$enc       = '';
$flags     = 32;
$platid    = 3;
$encid     = 1;
$addcbbox  = false;
$link      = false;
 
$args = $_SERVER['argv'];
array_shift($args);

while (count($args)) {
	$arg = array_shift($args);
	switch ($arg) {
		case "-h":
		case "--help":
			help();
			exit(0);
			break;

		case "-t":
		case "--type":
			if (count($args)) {
				$type = array_shift($args);
			} else {
				die("Missing value for --type\n");
			}
			break;

		case '-o':
		case '--out':
			if (count($args)) {
				$out = realpath(array_shift($args)).'/';
			} else {
				die("Missing value for --out\n");
			}
			break;

		case '-l':
		case '--link':
			$link = true;
			break;

		default:
			if ($arg[0]=='-') {
				die("unkown option $arg\n");
			}
			$fontfiles[] = $arg;
	}
}
if (!is_dir($out) || !is_writable($out)) {
	die("Can't write to $out\n");
}
echo "Output dir set to $out\n";
if (count($fontfiles)) {
	foreach ($fontfiles as $fontfile) {
		$fontname = TCPDF_FONTS::addTTFfont($fontfile, $type, $enc, $flags, $out, $platid, $encid, $addcbbox, true);
		echo "$fontfile added as $fontname\n";
	}
} else {
	die("Missing fontfile (try --help for usage)\n");
}
