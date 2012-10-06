<?php

/*
 * This file is part of the Symfony package.
 *
 * (c) Fabien Potencier <fabien@symfony.com>
 *
 * For the full copyright and license information, please view the LICENSE
 * file that was distributed with this source code.
 */

//date_default_timezone_set('UTC');
spl_autoload_register(function ($class) {
    if (0 === strpos(ltrim($class, '/'), 'Symfony\Component')) {
        $file = substr(str_replace('\\', '/', $class), strlen('Symfony\Component')).'.php';
        if (file_exists(__DIR__.'/../..'.$file)) {
            # Run from source tree
            require_once __DIR__.'/../..'.$file;
        } else {
            # Run from install dir
            require_once 'Symfony/Component'.$file;        
        }
    }
});
