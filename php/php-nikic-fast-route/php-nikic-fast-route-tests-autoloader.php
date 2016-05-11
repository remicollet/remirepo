<?php

spl_autoload_register(function($class) {
    if (strpos($class, 'FastRoute\\') === 0 && strcasecmp(substr($class, -4), 'Test') === 0) {
        $name = substr($class, strlen('FastRoute'));
        require __DIR__ . strtr($name, '\\', DIRECTORY_SEPARATOR) . '.php';
    }
});

require_once 'BUILDROOT_PATH/bootstrap.php';
