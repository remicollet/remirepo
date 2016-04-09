<?php
/* Autoloader for hoa/xml and its dependencies */

$vendor = '/usr/share/php';

// Dependencies
foreach ([
	$vendor . '/Hoa/Consistency/autoload.php'    => true,
	$vendor . '/Hoa/Compiler/autoload.php'       => true,
	$vendor . '/Hoa/Exception/autoload.php'      => true,
	$vendor . '/Hoa/File/autoload.php'           => true,
	$vendor . '/Hoa/Stream/autoload.php'         => true,
	$vendor . '/Hoa/Stringbuffer/autoload.php'   => true,
	] as $dep => $mandatory) {
	if ($mandatory || file_exists($dep)) require_once($dep);
}

$fedoraHoaLoader->addNamespace('Hoa\\Xml\\', __DIR__, true);

