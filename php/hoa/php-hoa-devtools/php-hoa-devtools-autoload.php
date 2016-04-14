<?php
/* Autoloader for hoa/devtools and its dependencies */

$vendor = '/usr/share/php';

// Dependencies
foreach ([
	$vendor . '/Hoa/Cli/autoload.php'            => true,
	$vendor . '/Hoa/Consistency/autoload.php'    => true,
	$vendor . '/Hoa/File/autoload.php'           => true,
	$vendor . '/Hoa/Protocol/autoload.php'       => true,
	$vendor . '/Hoa/Router/autoload.php'         => true,
	$vendor . '/Hoa/Xyl/autoload.php'            => true,
	] as $dep => $mandatory) {
	if ($mandatory || file_exists($dep)) require_once($dep);
}

$fedoraHoaLoader->addNamespace('Hoa\\Devtools\\', __DIR__, true);

