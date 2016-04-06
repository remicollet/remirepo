<?php
/* Autoloader for hoa/regex and its dependencies */

$vendor = '/usr/share/php';

// Dependencies
foreach ([
	$vendor . '/Hoa/Consistency/autoload.php'    => true,
	$vendor . '/Hoa/Exception/autoload.php'      => true,
	$vendor . '/Hoa/Math/autoload.php'      => true,
	$vendor . '/Hoa/Protocol/autoload.php'      => true,
	$vendor . '/Hoa/Ustring/autoload.php'      => true,
	$vendor . '/Hoa/Visitor/autoload.php'      => true,
	] as $dep => $mandatory) {
	if ($mandatory || file_exists($dep)) require_once($dep);
}

$fedoraHoaLoader->addNamespace('Hoa\\Regex\\', __DIR__, true);

