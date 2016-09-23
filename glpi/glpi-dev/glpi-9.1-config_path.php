<?php
// for Redhat/Fedora RPM defaults

// Config
define('GLPI_CONFIG_DIR',     '/etc/glpi');

// Runtime Data
define('GLPI_DOC_DIR',        '/var/lib/glpi/files');
define('GLPI_CRON_DIR',       GLPI_DOC_DIR . '/_cron');
define('GLPI_DUMP_DIR',       GLPI_DOC_DIR . '/_dumps');
define('GLPI_GRAPH_DIR',      GLPI_DOC_DIR . '/_graphs');
define('GLPI_LOCK_DIR',       GLPI_DOC_DIR . '/_lock');
define('GLPI_PICTURE_DIR',    GLPI_DOC_DIR . '/_pictures');
define('GLPI_PLUGIN_DOC_DIR', GLPI_DOC_DIR . '/_plugins');
define('GLPI_RSS_DIR',        GLPI_DOC_DIR . '/_rss');
define('GLPI_SESSION_DIR',    GLPI_DOC_DIR . '/_sessions');
define('GLPI_TMP_DIR',        GLPI_DOC_DIR . '/_tmp');
define('GLPI_UPLOAD_DIR',     GLPI_DOC_DIR . '/_uploads');

// Log
define('GLPI_LOG_DIR',        '/var/log/glpi');

// System libraries
define('GLPI_HTMLAWED',       '/usr/share/php/htmLawed/htmLawed.php');

// Fonts
define('GLPI_FONT_FREESANS',  '/usr/share/fonts/gnu-free/FreeSans.ttf');

//Use system cron
define('GLPI_SYSTEM_CRON', true);
