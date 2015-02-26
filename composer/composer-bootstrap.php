<?php
require 'Composer/autoload.php';
$loader->registerNamespaces(array(
    'Composer\\Test'  => __DIR__
));
require __DIR__.'/Composer/TestCase.php';
