<?php
/* Autoloader for hoa/math and its dependencies */

$vendor = '/usr/share/php';

// Dependencies
foreach ([
	$vendor . '/Hoa/Compiler/autoload.php'       => true,
	$vendor . '/Hoa/Consistency/autoload.php'    => true,
	$vendor . '/Hoa/Exception/autoload.php'      => true,
	$vendor . '/Hoa/Iterator/autoload.php'       => true,
	$vendor . '/Hoa/Protocol/autoload.php'       => true,
	$vendor . '/Hoa/Zformat/autoload.php'        => true,
	] as $dep => $mandatory) {
	if ($mandatory || file_exists($dep)) require_once($dep);
}

$fedoraHoaLoader->addNamespace('Hoa\\Math\\', __DIR__, true);

