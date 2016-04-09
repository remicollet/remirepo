<?php
/* Autoloader for hoa/xyl and its dependencies */

$vendor = '/usr/share/php';

// Dependencies
foreach ([
	$vendor . '/Hoa/Consistency/autoload.php'    => true,
	$vendor . '/Hoa/Event/autoload.php'          => true,
	$vendor . '/Hoa/Exception/autoload.php'      => true,
	$vendor . '/Hoa/File/autoload.php'           => true,
	$vendor . '/Hoa/Http/autoload.php'           => true,
	$vendor . '/Hoa/Locale/autoload.php'         => true,
	$vendor . '/Hoa/Praspel/autoload.php'        => true,
	$vendor . '/Hoa/Protocol/autoload.php'       => true,
	$vendor . '/Hoa/Realdom/autoload.php'        => true,
	$vendor . '/Hoa/Router/autoload.php'         => true,
	$vendor . '/Hoa/Stringbuffer/autoload.php'   => true,
	$vendor . '/Hoa/View/autoload.php'           => true,
	$vendor . '/Hoa/Xml/autoload.php'            => true,
	$vendor . '/Hoa/Zformat/autoload.php'        => true,
	] as $dep => $mandatory) {
	if ($mandatory || file_exists($dep)) require_once($dep);
}

$fedoraHoaLoader->addNamespace('Hoa\\Xyl\\', __DIR__, true);

