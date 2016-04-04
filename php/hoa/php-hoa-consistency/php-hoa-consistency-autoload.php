<?php
/* Autoloader for hoa/consistency and its dependencies */

/* This will load the autoloader */
require_once __DIR__ . '/Prelude.php';

$vendor = '/usr/share/php';

// Use Hoa autoloader
if (!isset($fedoraHoaLoader) || !($fedoraHoaLoader instanceof \Hoa\Consistency\Autoloader)) {
	$fedoraHoaLoader = new \Hoa\Consistency\Autoloader();
	$fedoraHoaLoader->register();
	$fedoraHoaLoader->addNamespace('Hoa\\Consistency\\', __DIR__);
}

// Dependencies
foreach ([
	$vendor . '/Hoa/Exception/autoload.php'      => true,
	] as $dep => $mandatory) {
	if ($mandatory || file_exists($dep)) require_once($dep);
}

