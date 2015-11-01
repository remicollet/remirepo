<?php
$vendor = '/usr/share/php';

if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once $vendor . '/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}
$fedoraClassLoader->addPrefix('Kdyby\\Events\\', dirname(dirname(__DIR__)));
require_once __DIR__ . '/exceptions.php';

// Dependencies
require_once $vendor . '/Doctrine/Common/autoload.php';
require_once $vendor . '/Nette/DI/autoload.php';
require_once $vendor . '/Nette/Utils/autoload.php';
