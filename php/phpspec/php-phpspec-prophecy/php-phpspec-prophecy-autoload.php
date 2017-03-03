<?php
/* Autoloader for phpspec/prophecy and its dependencies */

// Rely on include_path as in PHPUnit dependencies + circular dependencies

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Prophecy\\', __DIR__);

// Dependencies
require_once 'Doctrine/Instantiator/autoload.php';
require_once 'phpDocumentor/Reflection/DocBlock/autoload.php';

if (!class_exists('SebastianBergmann\\Comparator\\Comparator')) { // v2 from phpunit, v1 from phpspec
  require_once (stream_resolve_include_path('SebastianBergmann/Comparator2/autoload.php') ?: 'SebastianBergmann/Comparator/autoload.php');
}
if (!class_exists('SebastianBergmann\\RecursionContext\\Context')) { // v3 from phpunit, v2 from phpspec (via exporter)
  require_once (stream_resolve_include_path('SebastianBergmann/RecursionContext3/autoload.php') ?: 'SebastianBergmann/RecursionContext/autoload.php');
}

