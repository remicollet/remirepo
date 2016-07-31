Additional installation and update information:

Upstream documentation: http://trac.roundcube.net/wiki

Notice
- temporary files are stored in /var/lib/roundcubemail/temp
- logs files are stored in /var/log/roundcubemail
- configuration files are stored in /etc/roundcubemail
- PGP keys used by enigma plugin are stored in /var/lib/roundcubemail/enigma

As those directories are not served by the web server,
there is no need to protect them.

Databases

Roundcube supports various database providers, including SQLite, MySQL and
PostgreSQL. The package depends only on php-pdo, which provides SQLite
support. However, the default configuration is for a MySQL database, for
performance reasons. To use the MySQL database, ensure php-mysql is
installed. If you want to use another database, adjust the configuration
file, and ensure the appropriate PDO plugin is installed. If necessary.


The installer is available at http://localhost/roundcubemail/installer
The webmail is available at http://localhost/roundcubemail

By default, access to Roundcube and the installer is only allowed from the
server, locally, in /etc/httpd/conf.d/roundcubemail.conf . Best practice is
to create a new file - e.g. /etc/httpd/conf.d/z-roundcubemail-allow.conf -
to adjust the access permissions. You can also edit roundcubemail.conf directly,
but then any changes to it in future package updates will cause the creation
of a .rpmnew file, and you will have to merge the changes manually: creating
a new config file to configure access permissions avoids that.

First use the installer to configure Roundcube, ideally from the server so you
do not need to allow any wider access to the installer, but you can use a new
config file to grant wider access to /usr/share/roundcubemail and
/usr/share/roundcubemail/installer if necessary. Once you have completed
deployment, you should restrict access to the /installer subdirectory again, as
an attacker could use it to do anything they liked to your Roundcube
installation.

UPGRADING: when upgrading from < 1.0 the old configuration files named
main.inc.php and db.inc.php are now deprecated and should be replaced with one
single config.inc.php file. Run the /usr/share/roundcube/bin/update.sh script
as root to get this conversion done or manually merge the files. The update
script will also update the database configuration. Check the permissions of
the config.inc.php file and all backups the script creates! Make sure they
are not world-readable, as they may contain sensitive information (e.g.
database passwords).

NOTE: the new config.inc.php should only contain options that differ from the
ones listed in defaults.inc.php.
