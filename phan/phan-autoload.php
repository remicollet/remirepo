<?php
/* Autoloader for etsy/phan and its dependencies */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Phan\\', __DIR__);
\Fedora\Autoloader\Dependencies::required(array(
    '/usr/share/php/Symfony/Component/Console/autoload.php',
));
