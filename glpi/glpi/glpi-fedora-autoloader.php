<?php
$vendor = '##DATADIR##/php';

// Dependencies from composer.json
// "ircmaxell/password-compat"
// => useless for php >= 5.5
//require_once $vendor . '/password_compat/password.php';
// "jasig/phpcas"
require_once '##DATADIR##/pear/CAS/Autoload.php';
// "iamcal/lib_autolink"
require_once $vendor . '/php-iamcal-lib-autolink/autoload.php';
// "phpmailer/phpmailer"
require_once $vendor . '/PHPMailer/PHPMailerAutoload.php';
// "sabre/vobject"
require_once $vendor . '/Sabre/VObject/autoload.php';
// "simplepie/simplepie"
require_once $vendor . '/php-simplepie/autoloader.php';
// "tecnickcom/tcpdf"
require_once $vendor . '/tcpdf/autoload.php';
// "zendframework/zend-cache"
// "zendframework/zend-i18n"
// "zendframework/zend-loader"
require_once $vendor . '/Zend/autoload.php';
// "zetacomponents/graph"
require_once $vendor . '/ezc/Graph/autoloader.php';
// "ramsey/array_column"
// => useless for php >= 5.5
// "michelf/php-markdown"
require_once $vendor . '/Michelf/markdown-autoload.php';
// "true/punycode"
if (file_exists($vendor . '/TrueBV/autoload.php')) {
    require_once $vendor . '/TrueBV/autoload.php';
} else {
    require_once $vendor . '/TrueBV/Punycode.php';
}
