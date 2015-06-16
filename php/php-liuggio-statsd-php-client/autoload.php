<?php
$vendor = '/usr/share/php';
if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once $vendor . '/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

if (is_dir($vendor . '/Monolog')) {
	$fedoraClassLoader->addPrefix('Monolog',  $vendor);
	$fedoraClassLoader->addPrefix('Psr\\Log', $vendor);
}
$fedoraClassLoader->addPrefix('Liuggio\\StatsdClient', dirname(dirname(__DIR__)));

return $fedoraClassLoader;
