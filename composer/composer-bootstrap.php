<?php
require 'Composer/autoload.php';
/* \Fedora\Autoloader\Autoload::addPsr0('Composer\\Test\\', __DIR__ . '/'); broken for now */
\Fedora\Autoloader\Autoload::addPsr4('Composer\\Test\\', __DIR__ . '/Composer/Test');
require __DIR__.'/Composer/TestCase.php';

