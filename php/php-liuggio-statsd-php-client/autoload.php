<?php
$vendor = '/usr/share/php';
if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once $vendor . '/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

if (file_exists( $vendor . '/Monolog/autoload.php')) {
    require_once $vendor . '/Monolog/autoload.php';

} else if (is_dir($vendor . '/Monolog')) {
    $fedoraClassLoader->addPrefix('Monolog',  $vendor);
    $fedoraClassLoader->addPrefix('Psr\\Log', $vendor);
}
$fedoraClassLoader->addPrefix('Liuggio\\StatsdClient', dirname(dirname(__DIR__)));

return $fedoraClassLoader;
