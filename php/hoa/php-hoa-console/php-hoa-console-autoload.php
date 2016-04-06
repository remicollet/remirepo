<?php
/* Autoloader for hoa/console and its dependencies */

$vendor = '/usr/share/php';

// Dependencies
foreach ([
	$vendor . '/Hoa/Consistency/autoload.php'    => true,
	$vendor . '/Hoa/Event/autoload.php'          => true,
	$vendor . '/Hoa/Exception/autoload.php'      => true,
	$vendor . '/Hoa/File/autoload.php'           => true,
	$vendor . '/Hoa/Protocol/autoload.php'       => true,
	$vendor . '/Hoa/Stream/autoload.php'         => true,
	$vendor . '/Hoa/Ustring/autoload.php'        => true,
	$vendor . '/Hoa/Dispatcher/autoload.php'     => false,
	$vendor . '/Hoa/Router/autoload.php'         => false,
	] as $dep => $mandatory) {
	if ($mandatory || file_exists($dep)) require_once($dep);
}

$fedoraHoaLoader->addNamespace('Hoa\\Console\\', __DIR__, true);

