<?php
/* Autoloader for hoa/visitor and its dependencies */

$vendor = '/usr/share/php';

// Dependencies
foreach ([
	$vendor . '/Hoa/Consistency/autoload.php'    => true,
	] as $dep => $mandatory) {
	if ($mandatory || file_exists($dep)) require_once($dep);
}

$fedoraHoaLoader->addNamespace('Hoa\\Visitor\\', __DIR__, true);

