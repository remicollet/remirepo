<?php
/* Autoloader for hoa/cli and its dependencies */

$vendor = '/usr/share/php';

// Dependencies
foreach ([
	$vendor . '/Hoa/Consistency/autoload.php'    => true,
	$vendor . '/Hoa/Console/autoload.php'        => true,
	$vendor . '/Hoa/Dispatcher/autoload.php'     => true,
	$vendor . '/Hoa/Exception/autoload.php'      => true,
	$vendor . '/Hoa/Protocol/autoload.php'       => true,
	$vendor . '/Hoa/Router/autoload.php'         => true,
	] as $dep => $mandatory) {
	if ($mandatory || file_exists($dep)) require_once($dep);
}

$fedoraHoaLoader->addNamespace('Hoa\\Cli\\', __DIR__, true);

