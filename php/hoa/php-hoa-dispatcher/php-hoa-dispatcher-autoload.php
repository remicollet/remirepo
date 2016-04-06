<?php
/* Autoloader for hoa/dispatcher and its dependencies */

$vendor = '/usr/share/php';

// Dependencies
foreach ([
	$vendor . '/Hoa/Consistency/autoload.php'    => true,
	$vendor . '/Hoa/Exception/autoload.php'      => true,
	$vendor . '/Hoa/Zformat/autoload.php'        => true,
	$vendor . '/Hoa/Router/autoload.php'         => false,
	$vendor . '/Hoa/View/autoload.php'           => false,
	] as $dep => $mandatory) {
	if ($mandatory || file_exists($dep)) require_once($dep);
}

$fedoraHoaLoader->addNamespace('Hoa\\Dispatcher\\', __DIR__, true);

