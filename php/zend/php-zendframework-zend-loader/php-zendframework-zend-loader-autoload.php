<?php
/*
Simple autoloader for Zend Framework
Inspired from https://github.com/zendframework/ZendSkeletonApplication

Set autoregister_zf     for Zend Framework
Set fallback_autoloader for dependencies which are PSR-0 compliant
*/
require_once __DIR__ . '/Loader/AutoloaderFactory.php';
Zend\Loader\AutoloaderFactory::factory(array(
    'Zend\Loader\StandardAutoloader' => array(
        'fallback_autoloader' => true,
        'autoregister_zf' => true
     )
));

// Dependencies during build
if (defined('RPM_BUILDROOT')) {
    foreach(glob(RPM_BUILDROOT . '/*-autoload.php') as $dep) {
        require_once $dep;
    }
}
// Dependencies outside Zend namespace
foreach(glob(__DIR__ . '/*-autoload.php') as $dep) {
    require_once $dep;
}
// Common optional dependencies
foreach ([
    '/usr/share/php/Psr/Http/Message/autoload.php',
    '/usr/share/php/Interop/Container/autoload.php',
] as $dep) {
    if (file_exists($dep)) {
        require_once($dep);
    }
}

