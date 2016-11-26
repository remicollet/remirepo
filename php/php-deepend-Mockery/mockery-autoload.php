<?php
/* Autoloader for mockery/mockery and its dependencies */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Mockery\\', __DIR__);
\Fedora\Autoloader\Autoload::addClassMap(
    array('mockery' => '/../Mockery.php'),
    __DIR__
);
\Fedora\Autoloader\Dependencies::required(array(
    '/usr/share/php/Hamcrest/autoload.php',
));

