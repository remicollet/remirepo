<?php

require '/usr/share/php/Hoa/Consistency/autoload.php';

$nss = [ 
	'Hoa\\Consistency\\',
	'Hoa\\Event\\',
	'Hoa\\Exception\\',
];
foreach ($nss as $ns) {
	echo "$ns: ";
	print_r($fedoraHoaLoader->getBaseDirectories($ns));
}
$classes = [
	'\\Hoa\\Consistency\\Xcallable',
	'\\Hoa\\Event\\Listener',
	'\\Hoa\\Exception\\Group',
];
foreach ($classes as $class) {
	if (class_exists($class)) {
		echo ".";
	} else {
		echo "\nMissing $class\n";
	}
}
echo "\nDone\n";

