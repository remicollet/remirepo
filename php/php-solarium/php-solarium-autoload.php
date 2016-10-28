<?php
/* Autoloader for solarium/solarium and its dependencies */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Solarium\\', __DIR__);
\Fedora\Autoloader\Dependencies::required(array(
    array(
        '/usr/share/php/Symfony/Component/autoload.php',
        '/usr/share/php/Symfony/autoload.php',
    ),
));

