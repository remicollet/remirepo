<?php
/* Autoloader for hoa/realdom and its dependencies */

$vendor = '/usr/share/php';

// Dependencies
foreach ([
	$vendor . '/Hoa/Compiler/autoload.php'       => true,
	$vendor . '/Hoa/Consistency/autoload.php'    => true,
	$vendor . '/Hoa/Exception/autoload.php'      => true,
	$vendor . '/Hoa/File/autoload.php'           => true,
	$vendor . '/Hoa/Iterator/autoload.php'       => true,
	$vendor . '/Hoa/Math/autoload.php'           => true,
	$vendor . '/Hoa/Praspel/autoload.php'        => true,
	$vendor . '/Hoa/Regex/autoload.php'          => true,
	$vendor . '/Hoa/Ustring/autoload.php'        => true,
	$vendor . '/Hoa/Visitor/autoload.php'        => true,
	] as $dep => $mandatory) {
	if ($mandatory || file_exists($dep)) require_once($dep);
}

$fedoraHoaLoader->addNamespace('Hoa\\Realdom\\', __DIR__, true);

