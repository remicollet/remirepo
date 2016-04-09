<?php
/* Autoloader for hoa/stringbuffer and its dependencies */

$vendor = '/usr/share/php';

// Dependencies
foreach ([
	$vendor . '/Hoa/Consistency/autoload.php'    => true,
	$vendor . '/Hoa/Exception/autoload.php'      => true,
	$vendor . '/Hoa/Protocol/autoload.php'      => true,
	$vendor . '/Hoa/Stream/autoload.php'      => true,
	] as $dep => $mandatory) {
	if ($mandatory || file_exists($dep)) require_once($dep);
}

$fedoraHoaLoader->addNamespace('Hoa\\Stringbuffer\\', __DIR__, true);

