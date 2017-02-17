# remirepo spec file for owncloud from:
#
# Fedora spec file for owncloud
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
Name:           owncloud
Version:        9.1.4
Release:        2%{?dist}
Summary:        Private file sync and share server
Group:          Applications/Internet

License:        AGPLv3+ and MIT and BSD and CC-BY and CC-BY-SA and GPLv3 and Public Domain and (MPLv1.1 or GPLv2+ or LGPLv2+) and (MIT or GPL+) and (MIT or GPLv2) and ASL 2.0 and LGPLv3
URL:            http://owncloud.org

Source0:        https://download.owncloud.org/community/%{name}-%{version}.tar.bz2

Source1:        %{name}-httpd.conf
Source2:        %{name}-access-httpd.conf.avail

Source200:        %{name}-default-nginx.conf
Source201:        %{name}-conf-nginx.conf
Source202:        %{name}-php-fpm.conf
Source203:        %{name}-el7-php-fpm.conf

# Config snippets
Source100:      %{name}-auth-any.inc
Source101:      %{name}-auth-local.inc
Source102:      %{name}-auth-none.inc
Source103:      %{name}-defaults.inc
# packaging notes and doc
Source3:        %{name}-README.fedora
Source4:        %{name}-mysql.txt
Source5:        %{name}-postgresql.txt
# config.php containing just settings we want to specify, OwnCloud's
# initial setup will fill out other settings appropriately
Source7:        %{name}-config.php

# Our autoloader for core
Source8:        %{name}-fedora-autoloader.php

# Stop OC from trying to do stuff to .htaccess files. Just calm down, OC.
# Distributors are on the case.
Patch2:         %{name}-9.1.0-dont_update_htacess.patch

# Remove explicit load of dropbox
Patch3:         %{name}-9.1.0-dropbox-autoloader.patch

# Remove explicit load of google
Patch4:         %{name}-9.1.0-google-autoloader.patch

# Remove explicit load of aws
Patch5:         %{name}-9.1.0-amazon-autoloader.patch

# Display the appropriate upgrade command for fedora/epel users bz#1321417
Patch6:         %{name}-8.2.3-correct-cli-upgrade-command.patch

# Disable the integrity checking whilst a better way to deal with it is found
Patch7:         %{name}-9.1.0-default_integrity_check_disabled.patch

# No need to check PHP versions, Fedora maintainers are on the job
Patch8:         %{name}-9.1.4-dont_warn_about_php_versions.patch

#Backport of php7.1 fixes
Patch9:         %{name}-b129d5d-php71-backport.patch
Patch10:        %{name}-463e2ea-php71-backport.patch

# Need to work around an NSS issue
# fixed in 7.3         https://bugzilla.redhat.com/1241172,
# not yet fixed in 6.8 https://bugzilla.redhat.com/1260678
Patch11:        %{name}-9.1.1-work-arround-nss-issue.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch


# expand pear macros on install
BuildRequires:  php-pear

# For sanity %%check
BuildRequires:       php-cli
BuildRequires:       php-composer(sabre/dav)  >= 3.0.8
BuildRequires:       php-composer(sabre/dav)  < 4.0
BuildRequires:       php-composer(doctrine/dbal) >= 2.5.4
BuildRequires:       php-composer(doctrine/dbal) < 2.6
BuildRequires:       php-composer(mcnetic/zipstreamer) >= 1.0
BuildRequires:       php-composer(mcnetic/zipstreamer) < 2.0
BuildRequires:       php-composer(phpseclib/phpseclib) >= 2.0
BuildRequires:       php-composer(phpseclib/phpseclib) < 3.0
BuildRequires:       php-opencloud >= 1.9.2
BuildRequires:       php-composer(jeremeamia/superclosure) >= 2.1.0
BuildRequires:       php-composer(bantu/ini-get-wrapper) >= 1.0.1
BuildRequires:       php-composer(natxet/CssMin) >= 3.0.4
BuildRequires:       php-composer(punic/punic) >= 1.6.3
BuildRequires:       php-composer(pear/archive_tar) >= 1.4.1
BuildRequires:       php-composer(pear/archive_tar) < 2.0
BuildRequires:       php-composer(patchwork/utf8) >= 1.2.6
BuildRequires:       php-composer(patchwork/utf8) < 2.0
BuildRequires:       php-composer(symfony/console) >= 2.8.3
BuildRequires:       php-composer(symfony/event-dispatcher) >= 2.8.3
BuildRequires:       php-composer(symfony/routing) >= 2.8.1
BuildRequires:       php-composer(symfony/process) >= 2.8.1
BuildRequires:       php-composer(pimple/pimple) >= 3.0.2
BuildRequires:       php-composer(pimple/pimple) < 4.0
BuildRequires:       php-composer(ircmaxell/password-compat) >= 1.0.0
BuildRequires:       php-composer(nikic/php-parser) >= 1.4.1
BuildRequires:       php-composer(nikic/php-parser) < 2.0
BuildRequires:       php-composer(icewind/streams) >= 0.5.2
BuildRequires:       php-composer(swiftmailer/swiftmailer) >= 5.4.1
BuildRequires:       php-composer(guzzlehttp/guzzle) >= 5.3.0
BuildRequires:       php-composer(guzzlehttp/guzzle) < 6.0
BuildRequires:       php-composer(league/flysystem) >= 1.0.20
BuildRequires:       php-composer(interfasys/lognormalizer) >= 1.0
BuildRequires:       php-composer(owncloud/tarstreamer) >= 0.1
BuildRequires:       php-composer(patchwork/jsqueeze) >= 2.0
BuildRequires:       php-composer(patchwork/jsqueeze) < 3.0
BuildRequires:       php-composer(kriswallsmith/assetic) >= 1.3.2-3
BuildRequires:       php-composer(kriswallsmith/assetic) < 2.0
BuildRequires:       php-composer(icewind/smb)     >= 1.1.0
%if 0%{?rhel} != 5
BuildRequires:       php-pecl(smbclient) >= 0.8.0
%endif
BuildRequires:       php-google-apiclient >= 1.0.3
BuildRequires:       php-aws-sdk >= 2.7.0
BuildRequires:       php-composer(symfony/yaml) >= 2.6.0
BuildRequires:       php-composer(symfony/yaml) < 3.0.0
BuildRequires:       php-pear(pear.dropbox-php.com/Dropbox)
BuildRequires:       php-composer(symfony/polyfill-php70) >= 1.0
BuildRequires:       php-composer(symfony/polyfill-php70) < 2.0
BuildRequires:       php-composer(symfony/polyfill-php55) >= 1.0
BuildRequires:       php-composer(symfony/polyfill-php55) < 2.0
BuildRequires:       php-composer(symfony/polyfill-php56) >= 1.0
BuildRequires:       php-composer(symfony/polyfill-php56) < 2.0
BuildRequires:       php-composer(lukasreschke/id3parser) >= 0.0.1
BuildRequires:       php-composer(lukasreschke/id3parser) < 1.0.0

Requires:       %{name}-webserver = %{version}-%{release}
Requires:       %{name}-database = %{version}-%{release}

# Core PHP libs/extensions required by OC core
Requires:       php-curl
Requires:       php-dom
Requires:       php-exif
Requires:       php-fileinfo
Requires:       php-gd
Requires:       php-iconv
Requires:       php-json
Requires:       php-ldap
Requires:       php-mbstring
Requires:       php-openssl
Requires:       php-pcre
Requires:       php-pdo
Requires:       php-session
Requires:       php-simplexml
Requires:       php-xmlwriter
Requires:       php-spl
Requires:       php-zip
Requires:       php-filter

### External PHP libs required by OC core


# "doctrine/dbal": "2.5.4"
# pulls in doctrine/common as a strict requires
# which pulls in doctrine/{annotations,inflector,cache,collections,lexer} as strict requires
Requires:       php-composer(doctrine/dbal) >= 2.5.4
Requires:       php-composer(doctrine/dbal) < 2.6

#"mcnetic/zipstreamer": "^1.0"
Requires:       php-composer(mcnetic/zipstreamer) >= 1.0
Requires:       php-composer(mcnetic/zipstreamer) < 2.0

# "phpseclib/phpseclib": "2.0.0"
Requires:       php-composer(phpseclib/phpseclib) >= 2.0
Requires:       php-composer(phpseclib/phpseclib) < 3.0

#Requires:       php-composer(rackspace/php-opencloud) >= 1.9.2
# pulls in guzzle/http as a strict requires
# guzzle/http package include common, parser and stream too
Requires:       php-opencloud >= 1.9.2

# "jeremeamia/superclosure": "2.1.0"
Requires:       php-composer(jeremeamia/superclosure) >= 2.1.0

# "bantu/ini-get-wrapper": "v1.0.1"
Requires:       php-composer(bantu/ini-get-wrapper) >= 1.0.1

# "natxet/CssMin": "dev-master"
Requires:       php-composer(natxet/CssMin) >= 3.0.4

# "punic/punic": "1.6.3"
Requires:       php-composer(punic/punic) >= 1.6.3

# "pear/archive_tar": "1.4.1"
Requires:       php-composer(pear/archive_tar) >= 1.4.1
Requires:       php-composer(pear/archive_tar) < 2.0

# "patchwork/utf8": "1.2.6"
Requires:       php-composer(patchwork/utf8) >= 1.2.6
Requires:       php-composer(patchwork/utf8) < 2.0

# "symfony/console": "2.8.3"
Requires:       php-composer(symfony/console) >= 2.8.3
# "symfony/event-dispatcher": "2.8.3"
Requires:       php-composer(symfony/event-dispatcher) >= 2.8.3
# "symfony/routing": "2.8.1"
Requires:       php-composer(symfony/routing) >= 2.8.1
# "symfony/process": "2.8.1"
Requires:       php-composer(symfony/process) >= 2.8.1

# "pimple/pimple": "3.0.2"
Requires:       php-composer(pimple/pimple) >= 3.0.2
Requires:       php-composer(pimple/pimple) < 4.0

# "ircmaxell/password-compat": "1.0.*"
Requires:       php-composer(ircmaxell/password-compat) >= 1.0.0

# "nikic/php-parser": "1.4.1"
Requires:       php-composer(nikic/php-parser) >= 1.4.1
Requires:       php-composer(nikic/php-parser) < 2.0

# "icewind/Streams": "0.5.2"
Requires:       php-composer(icewind/streams) >= 0.5.2

# "swiftmailer/swiftmailer": "@stable"
# Version 5.4.1 for autoloader in /usr/share/php
Requires:       php-composer(swiftmailer/swiftmailer) >= 5.4.1

# "guzzlehttp/guzzle": "5.3.0"
# pulls in guzzlehttp/ringphp as strict requires
# ringphp pulls in guzzlehttp/streams and react/promise as strict requires
Requires:       php-composer(guzzlehttp/guzzle) >= 5.3.0
Requires:       php-composer(guzzlehttp/guzzle) < 6.0

# "league/flysystem": "1.0.20"
Requires:       php-composer(league/flysystem) >= 1.0.20


# "pear/pear-core-minimal": "v1.10.1"
# this includes pear/console_getopt and pear/PEAR 
# which is not listed in composer.json unlike archive_tar
Requires:       php-composer(pear/pear-core-minimal) >= 1.10.1

# "interfasys/lognormalizer": "v1.0"
Requires:       php-composer(interfasys/lognormalizer) >= 1.0

# "deepdiver1975/TarStreamer": "v0.1.0"
# Despite the difference in name this is correct
# https://github.com/owncloud/3rdparty/tree/master/deepdiver1975/tarstreamer
Requires:       php-composer(owncloud/tarstreamer) >= 0.1

# "patchwork/jsqueeze": "^2.0"
Requires:       php-composer(patchwork/jsqueeze) >= 2.0
Requires:       php-composer(patchwork/jsqueeze) < 3.0

# "kriswallsmith/assetic": "1.3.2"
# Need release 3 for the autoloader fix to avoid it spamming the logs
Requires:       php-composer(kriswallsmith/assetic) >= 1.3.2-3
Requires:       php-composer(kriswallsmith/assetic) < 2.0

# "sabre/dav" : "3.0.8"
# pulls in sabre event, http and vobject, xml, uri as strict requires
Requires:       php-composer(sabre/dav)  >= 3.0.8
Requires:       php-composer(sabre/dav)  < 4.0

# symfony/polyfill-mbstring is not in composer.json but is in the 3rdparty folder
# we don't need it though as we ship mbstring itself

# "symfony/polyfill-php70": "^1.0",
# pulls in s strict requires of paragonie/random_compat
Requires:       php-composer(symfony/polyfill-php70) >= 1.0
Requires:       php-composer(symfony/polyfill-php70) < 2.0
# "symfony/polyfill-php55": "^1.0",
Requires:       php-composer(symfony/polyfill-php55) >= 1.0
Requires:       php-composer(symfony/polyfill-php55) < 2.0
# "symfony/polyfill-php56": "^1.0"
Requires:       php-composer(symfony/polyfill-php56) >= 1.0
Requires:       php-composer(symfony/polyfill-php56) < 2.0

# "lukasreschke/id3parser" : "^0.0.1"
Requires:       php-composer(lukasreschke/id3parser) >= 0.0.1
Requires:       php-composer(lukasreschke/id3parser) < 1.0.0

### For dependencies of apps/files_external

## SMB/CIFS external storage stuff

#"icewind/smb": "1.1.0"
# note that streams is a dep but already required by core anyway
Requires:       php-composer(icewind/smb)     >= 1.1.0
# This makes smb external storage usable in performance
# and doesn't break things like encryption due to timeouts
%if 0%{?rhel} != 5
Requires:       php-pecl(smbclient) >= 0.8.0
%endif


# Requiring so that the shipped external smb storage works
# The net command is needed and enabling smb tests for smbclient command
%if 0%{?fedora} >= 20 || 0%{?rhel} >= 7
Requires:       samba-common-tools
Requires:       samba-client
%else
Requires:       %{_bindir}/net
Requires:       %{_bindir}/smbclient
%endif

## Note these next bits are not listed in composer but manually dropped in place

## Dropbox external storage
Requires:       php-pear(pear.dropbox-php.com/Dropbox)

## Google Drive external storage
Requires:       php-google-apiclient >= 1.0.3

## AWS S3 external storage
Requires:       php-aws-sdk >= 2.7.0

## For dependency of apps/gallery 
# "symfony/yaml": "~2.6"
Requires:       php-composer(symfony/yaml) >= 2.6.0
Requires:       php-composer(symfony/yaml) < 3.0.0

%if 0%{?rhel}
Requires(post): policycoreutils-python
Requires(postun): policycoreutils-python
%endif

%description
ownCloud gives you universal access to your files through a web interface or
WebDAV. It also provides a platform to easily view & sync your contacts,
calendars and bookmarks across all your devices and enables basic editing right
on the web. ownCloud is extendable via a simple but powerful API for
applications and plugins.


%package httpd
Summary:    Httpd integration for ownCloud
Group:      Applications/Internet

Provides:   %{name}-webserver = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}

# PHP dependencies
Requires:       php

%description httpd
%{summary}.


%package nginx
Summary:    Nginx integration for ownCloud
Group:      Applications/Internet

Provides:   %{name}-webserver = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}

# PHP dependencies
Requires:   php-fpm nginx

%description nginx
%{summary}.


%package mysql
Summary:    MySQL database support for ownCloud
Group:      Applications/Internet

Provides:   %{name}-database = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}

# From getSupportedDatabases, mysql => pdo, mysql
Requires:   php-pdo_mysql

%description mysql
This package ensures the necessary dependencies are in place for ownCloud to
work with MySQL / MariaDB databases. It does not require a MySQL / MariaDB
server to be installed, as you may well wish to use a remote database
server.

If you want the database to be on the same system as ownCloud itself, you must
also install and enable a MySQL / MariaDB server package. See README.mysql for
more details.

%package postgresql
Summary:    PostgreSQL database support for ownCloud
Group:      Applications/Internet

Provides:   %{name}-database = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}

# From getSupportedDatabases, pgsql => function, pg_connect
Requires:   php-pgsql

%description postgresql
This package ensures the necessary dependencies are in place for ownCloud to
work with a PostgreSQL database. It does not require the PostgreSQL server
package to be installed, as you may well wish to use a remote database
server.

If you want the database to be on the same system as ownCloud itself, you must
also install and enable the PostgreSQL server package. See README.postgresql
for more details.


%package sqlite
Summary:    SQLite 3 database support for ownCloud
Group:      Applications/Internet

Provides:   %{name}-database = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
# From getSupportedDatabases, pgsql => class, SQLite3
Requires:   php-sqlite3 php-pcre

%description sqlite
This package ensures the necessary dependencies are in place for ownCloud to
work with an SQLite 3 database stored on the local system.


%prep
%setup -q -n %{name}
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%if 0%{?rhel} >= 5 && 0%{?rhel} <= 6
%patch11 -p1
%endif

# patch backup files and .git stuff
find . -name \*.orig    -type f        -exec rm    {} \; -print
find . -name .gitignore -type f        -exec rm    {} \; -print
find . -name .github    -type d -prune -exec rm -r {} \; -print


# prepare package doc
cp %{SOURCE3} README.fedora
cp %{SOURCE4} README.mysql
cp %{SOURCE5} README.postgresql


mv 3rdparty/composer.json 3rdparty_composer.json
mv apps/files_external/3rdparty/composer.json files_external_composer.json
mv apps/gallery/composer.json gallery_composer.json


# Explicitly remove the bundled libraries we're aware of
pushd 3rdparty
rm -r doctrine/{annotations,cache,collections,common,dbal,inflector,lexer}
rm -r mcnetic/zipstreamer
rm -r phpseclib/phpseclib
rm -r rackspace/php-opencloud guzzle/{http,common,parser,stream}
rm -r jeremeamia/SuperClosure
rm -r bantu/ini-get-wrapper
rm -r natxet/CssMin
rm -r punic/punic
rm -r pear/archive_tar
rm -r patchwork/utf8
rm -r symfony/console
rm -r symfony/event-dispatcher
rm -r symfony/routing
rm -r symfony/process
rm -r pimple/pimple
rm -r ircmaxell/password-compat
rm -r nikic/php-parser
rm -r icewind/streams
rm -r swiftmailer/swiftmailer
rm -r guzzlehttp/{guzzle,ringphp,streams} react/promise
rm -r league/flysystem
rm -r pear/{pear-core-minimal,console_getopt,pear_exception}
rm -r interfasys/lognormalizer
rm -r deepdiver1975/tarstreamer
rm -r patchwork/jsqueeze
rm -r kriswallsmith/assetic
rm -r sabre/{dav,event,http,vobject,uri,xml}
rm -r symfony/polyfill-{php55,php56,php70,mbstring,util}
rm -r paragonie/random_compat
rm -r lukasreschke/id3parser
rm README.md

# remove composer stuff
rm -r composer*

# clean up any empty directories
find -type d -empty  -delete

# remove extraneous files now we've cleaned up
rm "LICENSE INFO" patches.txt

# add our Fedora autoloader 
cp %{SOURCE8} ./autoload.php

# Set the vendor directory to macro based datadir in our autoloader
sed -i "s,##DATADIR##,%{_datadir}," autoload.php
popd


# remove files_external bundled libraries
rm -r apps/files_external/3rdparty/{icewind,Dropbox,google-api-php-client,aws-sdk-php,composer*}

# create autoloader, from composer.json, "require": {
#                "icewind/smb": "1.0.4",
#                "icewind/streams": "0.2"
# include stuff required directly but not in composer too
cat << 'EOF' | tee apps/files_external/3rdparty/autoload.php
<?php
require_once '%{_datadir}/php/Icewind/Streams/autoload.php';
require_once '%{_datadir}/php/Icewind/SMB/autoload.php';
require_once '%{_datadir}/pear/Dropbox/autoload.php';
require_once '%{_datadir}/php/Google/autoload.php';
require_once '%{_datadir}/php/Aws/autoload.php';
EOF

# remove gallery external bundled libraries 
rm -r apps/gallery/vendor/{symfony,composer*}
rm    apps/gallery/composer.lock

# create autoloader, from composer.json, "require": {
#                "symfony/yaml": "_2.6"
cat << 'EOF' | tee apps/gallery/vendor/autoload.php
<?php
require_once '%{_datadir}/php/Symfony/Component/Yaml/autoload.php';
EOF

# clean up content
for f in {l10n.pl,init.sh,setup_owncloud.sh,image-optimization.sh,install_dependencies.sh}; do
    find . -name "$f" -exec rm {} \;
done
find . -size 0 -type f -exec rm {} \;

# let's not ship upstream's 'updatenotification' app, which has zero chance of working and
# a big chance of blowing things up
rm -r apps/updatenotification

# also remove the actual updater
rm -r updater



%check
# files_external checks
nb=$(ls %{buildroot}%{_datadir}/%{name}/apps/files_external/3rdparty | wc -l)
if [ $nb -gt 1  ]; then
  false apps/files_external/3rdparty must only have autoload.php
fi

if grep -r 3rdparty %{buildroot}%{_datadir}/%{name}/apps/files_external \
   | grep -v 3rdparty/autoload.php | grep -v signature.json; then
   false App files_external needs to be adapted
fi

php %{buildroot}%{_datadir}/%{name}/apps/files_external/3rdparty/autoload.php

# gallery checks
nb=$(ls %{buildroot}%{_datadir}/%{name}/apps/gallery/vendor | wc -l)
if [ $nb -gt 1  ]; then
  false apps/gallery/vendor must only have autoload.php
fi

php %{buildroot}%{_datadir}/%{name}/apps/gallery/vendor/autoload.php

# core checks
nb=$(ls %{buildroot}%{_datadir}/%{name}/3rdparty | wc -l)
if [ $nb -gt 1  ]; then
  false core 3rdparty must only have autoload.php
fi

php %{buildroot}%{_datadir}/%{name}/3rdparty/autoload.php

# There should not be an composer.json files remaining
nb=$(find -name 'composer.*' | wc -l)
if [ $nb -gt 0  ]
  then
  false found unexpected composer.json files
fi

%build
# Nothing to build


%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_datadir}/%{name}

# create owncloud datadir
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/data
# create writable app dir for appstore
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/apps
# create owncloud sysconfdir
mkdir -p %{buildroot}%{_sysconfdir}/%{name}

# install content
for d in $(find . -mindepth 1 -maxdepth 1 -type d | grep -v config); do
    cp -a "$d" %{buildroot}%{_datadir}/%{name}
done

for f in {*.php,*.xml,*.html,occ,robots.txt}; do
    install -pm 644 "$f" %{buildroot}%{_datadir}/%{name} 
done

# symlink config dir
ln -sf %{_sysconfdir}/%{name} %{buildroot}%{_datadir}/%{name}/config

# Owncloud looks for ca-bundle.crt in config dir
ln -sf %{_sysconfdir}/pki/tls/certs/ca-bundle.crt %{buildroot}%{_sysconfdir}/%{name}/ca-bundle.crt

# set default config
install -pm 644 %{SOURCE7}    %{buildroot}%{_sysconfdir}/%{name}/config.php

# httpd config
install -Dpm 644 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
install -Dpm 644 %{SOURCE2} \
    %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}-access.conf.avail
install -Dpm 644 %{SOURCE100} %{SOURCE101} %{SOURCE102} %{SOURCE103} \
    %{buildroot}%{_sysconfdir}/httpd/conf.d/

# nginx config
install -Dpm 644 %{SOURCE200} \
    %{buildroot}%{_sysconfdir}/nginx/default.d/%{name}.conf
install -Dpm 644 %{SOURCE201} \
    %{buildroot}%{_sysconfdir}/nginx/conf.d/%{name}.conf
%if 0%{?rhel}
install -Dpm 644 %{SOURCE203} \
    %{buildroot}%{_sysconfdir}/php-fpm.d/%{name}.conf
%else
install -Dpm 644 %{SOURCE202} \
    %{buildroot}%{_sysconfdir}/php-fpm.d/%{name}.conf
%endif


%if 0%{?fedora} < 21 && 0%{?rhel} < 7
%post
semanage fcontext -a -t httpd_sys_rw_content_t '%{_sysconfdir}/%{name}/config.php' 2>/dev/null || :
semanage fcontext -a -t httpd_sys_rw_content_t '%{_sysconfdir}/%{name}' 2>/dev/null || :
semanage fcontext -a -t httpd_sys_rw_content_t '%{_localstatedir}/lib/%{name}(/.*)?' 2>/dev/null || :
restorecon -R %{_sysconfdir}/%{name} || :
restorecon -R %{_localstatedir}/lib/%{name} || :

%postun
if [ $1 -eq 0 ] ; then
semanage fcontext -d -t httpd_sys_rw_content_t '%{_sysconfdir}/%{name}/config.php' 2>/dev/null || :
semanage fcontext -d -t httpd_sys_rw_content_t '%{_sysconfdir}/%{name}' 2>/dev/null || :
semanage fcontext -d -t httpd_sys_rw_content_t '%{_localstatedir}/lib/%{name}(/.*)?' 2>/dev/null || :
fi
%endif


%post httpd
%if 0%{?fedora} || 0%{?rhel} > 6
/usr/bin/systemctl reload httpd.service > /dev/null 2>&1 || :
%else
/sbin/service httpd reload > /dev/null 2>&1 || :
%endif

%postun httpd
if [ $1 -eq 0 ]; then
%if 0%{?fedora} || 0%{?rhel} > 6
  /usr/bin/systemctl reload httpd.service > /dev/null 2>&1 || :
%else
  /sbin/service httpd reload > /dev/null 2>&1 || :
%endif
fi

%post nginx
%if 0%{?rhel}
  # Work around missing php session directory for php-fpm in el7 bz#1338444
  if [ ! -d /var/lib/php/session ]
    then
    mkdir /var/lib/php/session
  fi
  /usr/bin/chown apache /var/lib/php/session
%endif
%if 0%{?fedora} || 0%{?rhel} > 6
  /usr/bin/systemctl reload nginx.service > /dev/null 2>&1 || :
  /usr/bin/systemctl reload php-fpm.service > /dev/null 2>&1 || :
%else
  /sbin/service nginx reload > /dev/null 2>&1 || :
  /sbin/service php-fpm reload > /dev/null 2>&1 || :
%endif

%postun nginx
if [ $1 -eq 0 ]; then
%if 0%{?fedora} || 0%{?rhel} > 6
  /usr/bin/systemctl reload nginx.service > /dev/null 2>&1 || :
  /usr/bin/systemctl reload php-fpm.service > /dev/null 2>&1 || :
%else
  /sbin/service nginx reload > /dev/null 2>&1 || :
  /sbin/service php-fpm reload > /dev/null 2>&1 || :
%endif
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING-AGPL README.fedora config/config.sample.php
%doc *_composer.json

%dir %attr(-,apache,apache) %{_sysconfdir}/%{name}
# contains sensitive data (dbpassword, passwordsalt)
%config(noreplace) %attr(0600,apache,apache) %{_sysconfdir}/%{name}/config.php
# need the symlink in confdir but it's not config
%{_sysconfdir}/%{name}/ca-bundle.crt

%{_datadir}/%{name}
%dir %attr(0755,apache,apache) %{_localstatedir}/lib/%{name}
# user data must not be world readable
%dir %attr(0750,apache,apache) %{_localstatedir}/lib/%{name}/data
%attr(-,apache,apache) %{_localstatedir}/lib/%{name}/apps


%files httpd
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_sysconfdir}/httpd/conf.d/%{name}-access.conf.avail
%{_sysconfdir}/httpd/conf.d/*.inc

%files nginx
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/nginx/default.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/php-fpm.d/%{name}.conf

%files mysql
%defattr(-,root,root,-)
%doc README.mysql

%files postgresql
%defattr(-,root,root,-)
%doc README.postgresql

%files sqlite
%defattr(-,root,root,-)


%changelog
* Fri Feb 17 2017 Remi Collet <remi@remirepo.net> - 9.1.4-2
- apply missing patch (integrity check)

* Fri Feb 03 2017 James Hogarth <james.hogarth@gmail.com> - 9.1.4-1
- Update to 9.1.4
- Fix guzzle autoloader ordering dependency issue

* Wed Dec 14 2016 James Hogarth <james.hogarth@gmail.com> - 9.1.3-1
- Fix bz#1404441 - php7 does not get the httpd php settings
- No need to check PHP versions within the code
- Backport php7.1 fixes
- Update to 9.1.3

* Tue Dec 13 2016 Remi Collet <remi@fedoraproject.org> - 9.1.3-1
- Update to 9.1.3
- fix autoloader to ensure Guzzle v5 is used by updater

* Tue Nov  8 2016 Remi Collet <remi@fedoraproject.org> - 9.1.2-1
- Update to 9.1.2

* Thu Oct 06 2016 James Hogarth <james.hogarth@gmail.com> - 9.1.1-1
- Update to 9.1.1

* Tue Sep 20 2016 Remi Collet <remi@fedoraproject.org> - 9.0.5-1
- Update to 9.0.5

* Tue Jul 19 2016 James Hogarth <james.hogarth@gmail.com> - 9.0.4-1
- New release 9.0.4

* Tue Jul 12 2016 James Hogarth <james.hogarth@gmail.com> - 9.0.3-3
- Added selinux remote DB details to readme bz#1349700

* Mon Jul  4 2016 Remi Collet <remi@fedoraproject.org> - 9.0.3-2
- mysql support uses pdo_mysql (not mysql extension)

* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 9.0.3-1
- Update to 9.0.3

* Tue Jun 14 2016 James Hogarth <james.hogarth@gmail.com> - 9.0.2-4
- Fix an infinite loop on a shared link with password and postgres bz#1346233

* Wed Jun 01 2016 James Hogarth <james.hogarth@gmail.com> - 9.0.2-3
- Place composer.json files in %%doc rather than remove them entirely

* Wed Jun 01 2016 James Hogarth <james.hogarth@gmail.com> - 9.0.2-2
- Remove updater app used by upstream
- More vigorous checking for composer.json

* Fri May 06 2016 James Hogarth <james.hogarth@gmail.com> - 9.0.2-1
- Update to 9.0.2
- Need a better way to deal with the integrity checking stuff from upstream

* Thu May 05 2016 James Hogarth <james.hogarth@gmail.com> - 9.0.1-1
- Remove el6 conditionals as it's no longer a supported platform
- Change nginx configuration as per bz#1332900 
- Add php-fpm owncloud dedicated pool
- No longer ships non-free jshint in aceeditor so don't need repack
- Update to 9.0.1

* Thu May  5 2016 Remi Collet <remi@fedoraproject.org> - 8.2.4-1
- Update to 8.2.4
- raise dependency on icewind/smb >= 1.0.8

* Thu Apr 28 2016 James Hogarth <james.hogarth@gmail.com> - 8.2.3-6
- Enable the sanity check of the autoloaders

* Tue Apr 12 2016 James Hogarth <james.hogarth@gmail.com> - 8.2.3-5
- Add autoloader based external libraries for core and gallery
- Add checks to catch future added dependencies
- Backport encryption patches from 9.0.x to support php-icewind-streams > 0.3.0

* Fri Apr 01 2016 James Hogarth <james.hogarth@gmail.com> - 8.2.3-4
- Update to new dependency versions now packaged
- Add fedora autoloader based external_files 
- Add patch to fix bz#1321417

* Thu Mar 24 2016 James Hogarth <james.hogarth@gmail.com> - 8.2.3-3
- Add typical appstore issue to readme
- Clean up spec to make it easier to follow the requires from unbundling

* Wed Mar 23 2016 Remi Collet <remi@fedoraproject.org> - 8.2.3-2
- use php-swift-Swift 5.4 in /usr/share/php
- fix patch to not update .htaccess
- drop samba dependency on old EL

* Tue Mar 22 2016 James Hogarth <james.hogarth@gmail.com> - 8.2.3-2
- Add smbclient dependency so that shipped external storage works as expected
- Add some data to the Fedora readme

* Mon Mar 14 2016 James Hogarth <james.hogarth@gmail.com> - 8.2.3-1
- new release 8.2.3

* Mon Mar 14 2016 Remi Collet <remi@fedoraproject.org> - 8.1.6-1
- Update to 8.1.6
- fix autoloader to ensure sabre/vobject 3.4 is used

* Sat Feb 20 2016 James Hogarth <james.hogarth@gmail.com> - 8.1.5-1
- Update to 8.1.5

* Mon Jan 11 2016 Adam Williamson <awilliam@redhat.com> - 8.0.10-1
- new release 8.0.10 (multiple security fixes)

* Wed Nov 04 2015 Adam Williamson <awilliam@redhat.com> - 8.0.9-1
- new release 8.0.9 (with security fixes)

* Fri Sep 18 2015 Adam Williamson <awilliam@redhat.com> - 8.0.8-1
- new release 8.0.8

* Wed Sep 02 2015 Adam Williamson <awilliam@redhat.com> - 8.0.7-1
- new release 8.0.7

* Fri Jul 10 2015 Adam Williamson <awilliam@redhat.com> - 8.0.5-1
- new release 8.0.5 (should fix app enabling, RHBZ #1240776)
- patch to use Google lib autoloader

* Sun Jul  5 2015 Remi Collet <remi@remirepo.net> - 8.0.4-3
- backport for remirepo

* Sat Jul 04 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 8.0.4-3
- Fix Symfony max version (2.6 changed to 3.0)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Adam Williamson <awilliam@redhat.com> - 8.0.4-1
- new release 8.0.4

* Mon May 04 2015 Adam Williamson <awilliam@redhat.com> - 8.0.3-2
- disable the htaccess fiddling stuff harder

* Fri May 01 2015 Adam Williamson <awilliam@redhat.com> - 8.0.3-1
- new release 8.0.3

* Sat Apr 25 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org>
- Fix nginx conf to serve static apps-appstore

* Fri Apr 24 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org>
- Use php handler from php-fpm nginx conf

* Sun Mar 15 2015 Adam Williamson <awilliam@redhat.com> - 8.0.2-1
- new release 8.0.2

* Fri Mar 06 2015 Adam Williamson <awilliam@redhat.com> - 8.0.1-0.2.rc1
- backport some significant app store fixes from upstream stable8

* Fri Mar 06 2015 Adam Williamson <awilliam@redhat.com> - 8.0.1-0.1.rc1
- update to 8.0.1rc1

* Mon Feb 23 2015 Adam Williamson <awilliam@redhat.com> - 8.0.0-6
- extend the htaccess patch to cover updater as well as initial setup
- rebase apache config stuff again, private dir denials only on 8.x branch

* Mon Feb 23 2015 Adam Williamson <awilliam@redhat.com> - 8.0.0-5
- simplify dropbox autoloader patch (just drop it entirely a la AWS)

* Mon Feb 23 2015 Adam Williamson <awilliam@redhat.com> - 8.0.0-4
- unbundle php-natxet-cssmin, add getid3 to the list of symlink hacks

* Mon Feb 23 2015 Adam Williamson <awilliam@redhat.com> - 8.0.0-3
- merge second version of Apache/Nginx config changes into 8.x build
- backport upstream PR #14119 to fix OC for DBAL 2.5.1

* Sun Feb 22 2015 Adam Williamson <awilliam@redhat.com> - 7.0.4-3
- revise and strengthen Apache configuration layout, fix external apps
- fix external apps for Nginx

* Sun Feb 22 2015 Adam Williamson <awilliam@redhat.com> - 8.0.0-2
- Initial version of Apache/Nginx config changes later re-done in 7.0.4-3

* Sat Feb 21 2015 Adam Williamson <awilliam@redhat.com> - 8.0.0-1
- new release 8.0.0
- rediff patches, adjust for new bundled libs, etc etc

* Sat Dec 20 2014 Adam Williamson <awilliam@redhat.com> - 7.0.4-2
- backport upstream support for google PHP lib 1.x and unbundle it

* Tue Dec 09 2014 Adam Williamson <awilliam@redhat.com> - 7.0.4-1
- new release 7.0.4

* Tue Nov 25 2014 Adam Williamson <awilliam@redhat.com> - 7.0.3-3
- fix dropbox autoload patch (thanks Tomas Dolezal) #1168082

* Tue Nov 11 2014 Adam Williamson <awilliam@redhat.com> - 7.0.3-2
- drop unnecessary bits from 3rdparty_includes.patch
- split Dropbox loading changes into a separate patch (submitted upstream)

* Mon Nov 10 2014 Adam Williamson <awilliam@redhat.com> - 7.0.3-1
- new release 7.0.3

* Wed Oct 29 2014 Adam Williamson <awilliam@redhat.com> - 7.0.2-4
- db sub-packages should not depend on db server packages
- improve README
- improve db sub-package descriptions
- don't check for new versions or working .htaccess files

* Tue Oct 28 2014 Adam Williamson <awilliam@redhat.com> - 7.0.2-3
- drop unnecessary deps: php-gmp (#1152438) and Net_Curl(#999720)
- re-arrange deps in spec to be the way I like 'em

* Tue Sep 09 2014 Adam Williamson <awilliam@redhat.com> - 7.0.2-2
- 10927.patch: backport fix for an upgrade bug (upstream #10762)

* Thu Aug 28 2014 Adam Williamson <awilliam@redhat.com> - 7.0.2-1
- update to 7.0.2
- update patch for using Composer autoloader with 3rdparty deps

* Wed Aug 20 2014 Adam Williamson <awilliam@redhat.com> - 7.0.1-2
- make php directives in httpd config conditional on mod_php (FPM compat)

* Wed Aug 20 2014 Adam Williamson <awilliam@redhat.com> - 7.0.1-1
- update to 7.0.1
- drop contact_type.patch (merged upstream)

* Tue Jul 29 2014 Adam Williamson <awilliam@redhat.com> - 7.0.0-6
- do not ship upstream's 'updater' app (it'll only lead to tears)
- don't patch and ship OC's sample config, write a stub instead

* Tue Jul 29 2014 Adam Williamson <awilliam@redhat.com> - 7.0.0-5
- fix up sabre paths right this time

* Tue Jul 29 2014 Adam Williamson <awilliam@redhat.com> - 7.0.0-4
- more autoloader tweaking
- use composer not OC autoloader for legacy 3rdparty includes (core#9643)
- specify explicit paths to Sabre deps

* Sun Jul 27 2014 Adam Williamson <awilliam@redhat.com> - 7.0.0-3
- update apache config for OC 7 changes
- drop unneeded isoft/mssql-bundle from 3rdparty

* Sun Jul 27 2014 Adam Williamson <awilliam@redhat.com> - 7.0.0-2
- opcache_invalidate.patch: avoid triggering a crash in the PHP opcache
- contact_type.patch: fix selection of current field type in contact view

* Thu Jul 24 2014 Adam Williamson <awilliam@redhat.com> - 7.0.0-1
- 7.0.0
- rediff 3rdparty_includes.patch
- update 3rdparty strip commands and dependencies for upstream changes
- update dependencies

* Mon Jun 30 2014 Gregor Tätzner <brummbq@fedoraproject.org> - 6.0.4-1
- 6.0.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 01 2014 Gregor Tätzner <brummbq@fedoraproject.org> - 6.0.3-1
- 6.0.3
- update symfony routing patch

* Tue Mar 04 2014 Gregor Tätzner <brummbq@fedoraproject.org> - 6.0.2-1
- 6.0.2

* Mon Feb 24 2014 Adam Williamson <awilliam@redhat.com> - 6.0.1-3
- set a minimum ver on the DBAL req for safety (using with 2.3 is dangerous)

* Mon Jan 27 2014 Adam Williamson <awilliam@redhat.com> - 6.0.1-2
- unbundle phpseclib (packaged now)

* Thu Jan 23 2014 Gregor Tätzner <brummbq@fedoraproject.org> - 6.0.1-1
- 6.0.1

* Tue Jan 14 2014 Gregor Tätzner <brummbq@fedoraproject.org>  - 6.0.0a-9
- fix routing with symfony 2.3

* Fri Jan 10 2014 Adam Williamson <awilliam@redhat.com> - 6.0.0a-8
- make a warning OC keeps triggering into a debug message

* Thu Jan  9 2014 Adam Williamson <awilliam@redhat.com> - 6.0.0a-7
- re-enable irods, patch loading of it, add dependency on it

* Fri Jan  3 2014 Adam Williamson <awilliam@redhat.com> - 6.0.0a-6
- disable irods a bit harder

* Fri Jan  3 2014 Adam Williamson <awilliam@redhat.com> - 6.0.0a-5
- drop non-existent OC_User_IMAP from config file

* Fri Jan  3 2014 Adam Williamson <awilliam@redhat.com> - 6.0.0a-4
- apps_3rdparty_includes: fix more 3rdparty loading stuff
- disable_irods: disable storage app's irods (it's broken)

* Mon Dec 30 2013 Adam Williamson <awilliam@redhat.com> - 6.0.0a-3
- tar-include, blowfish-include, dropbox-include: fix more paths

* Mon Dec 30 2013 Adam Williamson <awilliam@redhat.com> - 6.0.0a-2
- dropbox-include.patch: fix loading of system copy of php-Dropbox

* Sun Dec 22 2013 Adam Williamson <awilliam@redhat.com> - 6.0.0a-1
- 6.0.0a

* Sun Dec 22 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 6.0.0-1
- 6.0.0

* Fri Dec 20 2013 Adam Williamson <awilliam@redhat.com> - 5.0.14a-2
- Correct location of php-symfony-routing: #1045301

* Fri Dec 20 2013 Adam Williamson <awilliam@redhat.com> - 5.0.14a-1
- 5.0.14a

* Sat Nov 16 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 5.0.13-1
- 5.0.13

* Tue Oct 08 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 5.0.12-1
- 5.0.12

* Tue Sep 24 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 5.0.11-2
- keep MDB2/pgsql driver, genuine version causes upgrade problems (RBZ#962082)

* Sat Sep 07 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 5.0.11-1
- 5.0.11

* Wed Sep 04 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 5.0.10-4
- unbundle sabredav again

* Fri Aug 23 2013 Adam Williamson <awilliam@redhat.com> - 5.0.10-3
- patch mediaelement not to try and use its plugins

* Fri Aug 23 2013 Adam Williamson <awilliam@redhat.com> - 5.0.10-2
- drop binary Flash and Silverlight blobs: #1000257
- don't ship source of jplayer in the binary package

* Sun Aug 18 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 5.0.10-1
- 5.0.10

* Thu Aug 15 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 4.5.13-2
- RBZ #962082 keep 3rdparty pqsql mdb2 driver

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 5.0.9-2
- buildreq: php-pear (RBZ #987279)

* Tue Jul 16 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 5.0.9-1
- major upgrade to 5.0.9
- symlink 3rdparty libs and drop most of the patches
- new deps: php-ZendFramework symfony

* Sat Jun 08 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 4.5.12-1
- 4.5.12

* Thu May 16 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 4.5.11-2
- RBZ #963701: require mdb2-mysql not mysqli

* Thu May 16 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 4.5.11-1
- 4.5.11

* Tue Apr 23 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 4.5.10-1
- 4.5.10

* Sat Apr 13 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 4.5.9-1
- 4.5.9
- disable remote access by default

* Fri Mar 15 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 4.5.8-1
- 4.5.8
- unbundle dropbox-php
- log to syslog
- include nginx config

* Mon Feb 25 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 4.5.7-2
- added script for re-creating stripped tarball
- new httpd.conf for httpd 2.4

* Sun Feb 24 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 4.5.7-1
- 4.5.7

* Sun Jan 13 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.8-7
- fixed selinux file context on rhel

* Sat Dec 08 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.8-6
- unbundled phpass and php-when
- added database setup instructions

* Thu Nov 08 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.8-5
- moved included sqlite3 driver to owncloud-sqlite
- unbundled php-cloudfiles
- reworked runtime requirements

* Sun Nov 04 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.8-4
- repacked source tarball (deleted jslint code)

* Sat Nov 03 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.8-3
- added missing licenses
- obliterated jslint code from aceeditor

* Fri Nov 02 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.8-2
- updated license field
- added README.fedora

* Thu Oct 18 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.8-1
- owncloud-4.0.8

* Fri Oct 12 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.7-5
- unbundle php-getid3
- remove conf dir access check

* Tue Oct 02 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.7-4
- require rsyslog
- switched log type back to 'owncloud'

* Sun Sep 23 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.7-3
- unbundled Archive/Tar.php, Guess.php, phpmailer
- created virtual packages for supported databases
- added logrotate script

* Thu Sep 20 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.7-2
- moved httpd files and sciptlets into own subpackage
- redirected log output to /var/log/owncloud.log
- deleted unecessary files

* Wed Sep 19 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.7-1
- updated to version 4.0.7

* Fri Apr 06 2012 Felix Kaechele <heffer@fedoraproject.org> - 3.0.1-1
- initial package

