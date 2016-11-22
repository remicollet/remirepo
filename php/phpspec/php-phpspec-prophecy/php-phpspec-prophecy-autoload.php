<?php
/* Autoloader for phpspec/prophecy and its dependencies */

// Rely on include_path as in PHPUnit dependencies + circular dependencies

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Prophecy\\', __DIR__);

// Dependencies
require_once 'Doctrine/Instantiator/autoload.php';
require_once 'SebastianBergmann/Comparator/autoload.php';
require_once 'SebastianBergmann/RecursionContext/autoload.php';
require_once 'phpDocumentor/Reflection/DocBlock/autoload.php';
