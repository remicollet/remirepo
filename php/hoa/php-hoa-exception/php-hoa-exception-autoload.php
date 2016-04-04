<?php
/* Autoloader for hoa/event and its dependencies */

$vendor = '/usr/share/php';
// Use Symfony autoloader
if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once $vendor . '/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Hoa\\Exception\\', dirname(dirname(__DIR__)));

// Dependencies
foreach ([
	$vendor . '/Hoa/Consistency/autoload.php'    => true,
	$vendor . '/Hoa/Event/autoload.php'          => true,
	] as $dep => $mandatory) {
	if ($mandory || file_exists($dep) require_once($dep);
}

