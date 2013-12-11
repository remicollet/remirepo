<?php
// for Redhat/Fedora RPM defaults

// Config
define('GLPI_CONFIG_DIR',     '/etc/glpi');

// Runtime Data
define('GLPI_DOC_DIR',        '/var/lib/glpi/files');
define('GLPI_DUMP_DIR',       '/var/lib/glpi/files/_dumps');
define('GLPI_CACHE_DIR',      '/var/lib/glpi/files/_cache/');
define('GLPI_CRON_DIR',       '/var/lib/glpi/files/_cron');
define('GLPI_SESSION_DIR',    '/var/lib/glpi/files/_sessions');
define('GLPI_PLUGIN_DOC_DIR', '/var/lib/glpi/files/_plugins');
define('GLPI_LOCK_DIR',       '/var/lib/glpi/files/_lock/');
define('GLPI_GRAPH_DIR',      '/var/lib/glpi/files/_graphs/');
define('GLPI_TMP_DIR',        '/var/lib/glpi/files/_tmp/');
define('GLPI_RSS_DIR',        '/var/lib/glpi/files/_rss/');
define('GLPI_UPLOAD_DIR',     '/var/lib/glpi/files/_uploads/');
//define('GLPI_SCRIPT_DIR',

// Log
define('GLPI_LOG_DIR',        '/var/log/glpi');

// System libraries
define('GLPI_CACHE_LITE_DIR', 'Cache');
define('GLPI_PHPMAILER_DIR',  'PHPMailer');
define('GLPI_EZC_BASE',       'ezc/Base/base.php');
define('GLPI_PHPCAS',         'CAS.php');
define('GLPI_HTMLAWED',       'htmLawed/htmLawed.php');
define('GLPI_ZEND_PATH',      '/usr/share/php/Zend');
define("GLPI_SIMPLEPIE_PATH", '/usr/share/php/php-simplepie');

// Fonts
define('GLPI_FONT_FREESANS',  '/usr/share/fonts/gnu-free/FreeSans.ttf');
?>
