# remirepo spec file for phpMyAdmin
#
# Copyright (c) 2008-2017 Remi Collet
#
# Fedora spec file for phpMyAdmin
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%global prever beta1
%{!?_pkgdocdir: %global _pkgdocdir %{_datadir}/doc/%{name}-%{version}}
%if 0%{?fedora} >= 21
# nginx 1.6 with nginx-filesystem
%global with_nginx     1
# httpd 2.4 with httpd-filesystem
%global with_httpd     1
%else
%global with_nginx     0
%global with_httpd     0
%endif

Name: phpMyAdmin
Version: 4.7.0
Release: 0.1.%{prever}%{?dist}
Summary: Web based MySQL browser written in php

Group: Applications/Internet
# MIT (js/jquery/, js/codemirror/),
# BSD (libraries/plugins/auth/recaptcha/),
# GPLv2+ (the rest)
License: GPLv2+ and MIT and BSD
URL: https://www.phpmyadmin.net/
Source0: https://files.phpmyadmin.net/%{name}/%{version}%{?prever:-%prever}/%{name}-%{version}%{?prever:-%prever}-all-languages.tar.xz
Source1: https://files.phpmyadmin.net/%{name}/%{version}%{?prever:-%prever}/%{name}-%{version}%{?prever:-%prever}-all-languages.tar.xz.asc
Source2: phpMyAdmin.htaccess
Source3: phpMyAdmin.nginx

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires(post): coreutils sed
Requires:  webserver
%if %{with_nginx}
Requires:  nginx-filesystem
%endif
%if %{with_httpd}
Requires:  httpd-filesystem
Requires:  php(httpd)
Suggests:  httpd
%endif
# From composer.json, "require": {
#        "php": ">=5.5.0",
#        "ext-mbstring": "*",
#        "ext-mysqli": "*",
#        "ext-xml": "*",
#        "ext-pcre": "*",
#        "ext-json": "*",
#        "phpmyadmin/sql-parser": "^4.1",
#        "phpmyadmin/motranslator": "^3.0",
#        "phpmyadmin/shapefile": "^2.0",
#        "tecnickcom/tcpdf": "^6.2",
#        "phpseclib/phpseclib": "^2.0",
#        "google/recaptcha": "^1.1"
Requires:  php(language) >= 5.5
Requires:  php-mbstring
Requires:  php-mysqli
Requires:  php-openssl
Requires:  php-xml
Requires:  php-pcre
Requires:  php-json
Requires:  php-composer(phpmyadmin/sql-parser)   <  5
Requires:  php-composer(phpmyadmin/sql-parser)   >= 4.1
Requires:  php-composer(phpmyadmin/motranslator) <  4
Requires:  php-composer(phpmyadmin/motranslator) >= 3.0
Requires:  php-composer(phpmyadmin/shapefile)    <  3
Requires:  php-composer(phpmyadmin/shapefile)    >= 2.0
Requires:  php-composer(tecnickcom/tcpdf)        <  7
Requires:  php-composer(tecnickcom/tcpdf)        >= 6.2
Requires:  php-tcpdf-dejavu-sans-fonts
Requires:  php-composer(phpseclib/phpseclib)     <  3
Requires:  php-composer(phpseclib/phpseclib)     >= 2.0
Requires:  php-composer(google/recaptcha)        <  2
Requires:  php-composer(google/recaptcha)        >= 1.1
# Autoloader
Requires:  php-composer(fedora/autoloader)
# From composer.json, "suggest": {
#        "ext-openssl": "Cookie encryption",
#        "ext-curl": "Updates checking",
#        "ext-opcache": "Better performance",
#        "ext-zlib": "For gz import and export",
#        "ext-bz2": "For bzip2 import and export",
#        "ext-zip": "For zip import and export",
#        "ext-gd2": "For image transformations",
#        "tecnickcom/tcpdf": "For PDF support"
Requires:  php-openssl
Requires:  php-curl
Requires:  php-zlib
Requires:  php-bz2
Requires:  php-zip
Requires:  php-gd
%if 0%{?fedora} >= 21
Recommends: php-opcache
%endif
# From phpcompatinfo reports for 4.7.0
Requires:  php-date
Requires:  php-filter
Requires:  php-hash
Requires:  php-iconv
Requires:  php-libxml
Requires:  php-recode
Requires:  php-session
Requires:  php-simplexml
Requires:  php-spl
Requires:  php-xmlwriter

Provides:  php-composer(phpmyadmin/phpmyadmin) = %{version}
Provides:  phpmyadmin = %{version}-%{release}
Obsoletes: phpMyAdmin3
Obsoletes: phpMyAdmin4


%description
phpMyAdmin is a tool written in PHP intended to handle the administration of
MySQL over the Web. Currently it can create and drop databases,
create/drop/alter tables, delete/edit/add fields, execute any SQL statement,
manage keys on fields, manage privileges,export data into various formats and
is available in 50 languages


%prep
%setup -qn phpMyAdmin-%{version}%{?prever:-%prever}-all-languages

# Minimal configuration file
sed -e "/'extension'/s@'mysql'@'mysqli'@"  \
    -e "/'blowfish_secret'/s@''@'MUSTBECHANGEDONINSTALL'@"  \
    -e "/'UploadDir'/s@''@'%{_localstatedir}/lib/%{name}/upload'@"  \
    -e "/'SaveDir'/s@''@'%{_localstatedir}/lib/%{name}/save'@" \
    config.sample.inc.php >CONFIG

# Setup vendor config file
sed -e "/'CHANGELOG_FILE'/s@./ChangeLog@%{_pkgdocdir}/ChangeLog@" \
    -e "/'LICENSE_FILE'/s@./LICENSE@%{_pkgdocdir}/LICENSE@" \
    -e "/'CONFIG_DIR'/s@''@'%{_sysconfdir}/%{name}/'@" \
    -e "/'SETUP_CONFIG_FILE'/s@./config/config.inc.php@%{_localstatedir}/lib/%{name}/config/config.inc.php@" \
%if 0%{?_licensedir:1}
    -e '/LICENSE_FILE/s:%_defaultdocdir:%_defaultlicensedir:' \
%endif
    -i libraries/vendor_config.php

# For debug
grep '^define' libraries/vendor_config.php

# Generate autoloader
rm -rf vendor/*
cat << 'EOF' | tee vendor/autoload.php
<?php
/* Autoloader for phpMyAdmin and its dependencies */

require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('PMA\\', dirname(__DIR__));
\Fedora\Autoloader\Dependencies::required([
    '%{_datadir}/php/PhpMyAdmin/SqlParser/autoload.php',
    '%{_datadir}/php/PhpMyAdmin/MoTranslator/autoload.php',
    '%{_datadir}/php/PhpMyAdmin/ShapeFile/autoload.php',
    '%{_datadir}/php/tcpdf/autoload.php',
    '%{_datadir}/php/phpseclib/autoload.php',
    '%{_datadir}/php/ReCaptcha/autoload.php',
]);
EOF


%build
# Nothing to do


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/%{name}
cp -ad ./* %{buildroot}/%{_datadir}/%{name}
install -Dpm 0640 CONFIG %{buildroot}/%{_sysconfdir}/%{name}/config.inc.php
# Apache
install -Dpm 0644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/httpd/conf.d/phpMyAdmin.conf
# Nginx
%if %{with_nginx}
install -Dpm 0644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/nginx/default.d/phpMyAdmin.conf
%endif

rm -f %{buildroot}/%{_datadir}/%{name}/config.sample.inc.php
rm -f %{buildroot}/%{_datadir}/%{name}/*txt
rm -f %{buildroot}/%{_datadir}/%{name}/[CDLR]*
rm -f %{buildroot}/%{_datadir}/%{name}/libraries/.htaccess
rm -f %{buildroot}/%{_datadir}/%{name}/setup/lib/.htaccess
rm -f %{buildroot}/%{_datadir}/%{name}/setup/frames/.htaccess
rm -rf %{buildroot}/%{_datadir}/%{name}/contrib
rm     %{buildroot}/%{_datadir}/%{name}/composer.*

# documentation
rm -rf    %{buildroot}%{_datadir}/%{name}/examples/
rm -rf    %{buildroot}%{_datadir}/%{name}/doc/
mkdir -p  %{buildroot}%{_datadir}/%{name}/doc/
ln -s %{_pkgdocdir}/html  %{buildroot}%{_datadir}/%{name}/doc/html

mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/{upload,save,config}

mv -f $RPM_BUILD_ROOT%{_datadir}/%{name}/js/jquery/MIT-LICENSE.txt LICENSE-jquery
mv -f $RPM_BUILD_ROOT%{_datadir}/%{name}/js/codemirror/LICENSE LICENSE-codemirror


%clean
rm -rf %{buildroot}


%pretrans
# allow dir to link upgrade
if  [ -d %{_datadir}/%{name}/doc/html ]; then
  rm -rf %{_datadir}/%{name}/doc/html
fi

%post
# generate a 32 chars secret key for this install
SECRET=$(printf "%04x%04x%04x%04x%04x%04x%04x%04x" $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM)
sed -e "/'blowfish_secret'/s/MUSTBECHANGEDONINSTALL/$SECRET/" \
    -i %{_sysconfdir}/%{name}/config.inc.php


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE*
%doc ChangeLog README CONTRIBUTING.md DCO config.sample.inc.php
%doc doc/html/
%doc examples/
%doc composer.json
%{_datadir}/%{name}
%attr(0750,root,apache) %dir %{_sysconfdir}/%{name}
%config(noreplace) %attr(0640,root,apache) %{_sysconfdir}/%{name}/config.inc.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%if %{with_nginx}
%config(noreplace) %{_sysconfdir}/nginx/default.d/%{name}.conf
%endif
%dir %{_localstatedir}/lib/%{name}/
%dir %attr(0750,apache,apache) %{_localstatedir}/lib/%{name}/upload
%dir %attr(0750,apache,apache) %{_localstatedir}/lib/%{name}/save
%dir %attr(0750,apache,apache) %{_localstatedir}/lib/%{name}/config


%changelog
* Fri Jan 27 2017 Remi Collet <remi@remirepo.net> 4.7.0-0.1.beta1
- update to 4.7.0-beta1
- raise dependency on phpmyadmin/sql-parser version 4.1
- add dependency on phpmyadmin/motranslator
- add dependency on phpmyadmin/shapefile
- add dependency on google/recaptcha
- use fedora autoloader instead of composer one

* Tue Jan 24 2017 Remi Collet <remi@remirepo.net> 4.6.6-1
- update to 4.6.6 (2017-01-23, bug and security fixes)

* Mon Jan 23 2017 Remi Collet <remi@remirepo.net> 4.6.5.2-2
- ensure phpmyadmin/sql-parser v3 is used

* Tue Dec  6 2016 Remi Collet <remi@remirepo.net> 4.6.5.2-1
- update to 4.6.5.2 (2016-12-06, bug fixes)

* Mon Nov 28 2016 Remi Collet <remi@remirepo.net> 4.6.5.1-2
- drop unneeded patch

* Sat Nov 26 2016 Remi Collet <remi@remirepo.net> 4.6.5.1-1
- update to 4.6.5.1 (2016-11-26, bug fixes)
- add patch to fix broken links on home page,
  open https://github.com/phpmyadmin/phpmyadmin/pull/12741

* Fri Nov 25 2016 Remi Collet <remi@remirepo.net> 4.6.5-1
- update to 4.6.5 (2016-11-25, security and bug fixes)
- bump dependency on sql-parser 3.4.13

* Wed Aug 31 2016 Remi Collet <remi@remirepo.net> 4.6.4-1
- update to 4.6.4 (2016-08-17, security and bug fixes)

* Tue Jul 26 2016 Remi Collet <remi@remirepo.net> 4.6.4-1
- bump dependency on sql-parser 3.4.4

* Thu Jun 23 2016 Remi Collet <remi@remirepo.net> 4.6.3-1
- update to 4.6.3 (2016-06-23, security and maintenance release)

* Thu May 26 2016 Remi Collet <remi@remirepo.net> 4.6.2-1
- update to 4.6.2 (2016-05-25, maintenance release)

* Tue May  3 2016 Remi Collet <remi@remirepo.net> 4.6.1-1
- update to 4.6.1 (2016-05-03, maintenance release)

* Tue Mar 22 2016 Remi Collet <remi@remirepo.net> 4.6.0-1
- update to 4.6.0 (2016-03-22, features release)

* Thu Mar  3 2016 Remi Collet <remi@remirepo.net> 4.6.0-0.1.rc2
- update to 4.6.0-rc2

* Tue Mar  1 2016 Remi Collet <remi@remirepo.net> 4.5.5.1-1
- update to 4.5.5.1 (2016-02-29, security and bugfix)
- raise dependency on udan11/sql-parser >= 3.4.0

* Tue Feb 23 2016 Remi Collet <remi@remirepo.net> 4.5.5-1
- update to 4.5.5 (2016-02-22, bugfix)
- raise dependency on udan11/sql-parser >= 3.3.1

* Fri Jan 29 2016 Remi Collet <remi@remirepo.net> 4.5.4.1-1
- update to 4.5.4.1 (2016-01-29, bugfix)

* Thu Jan 28 2016 Remi Collet <remi@remirepo.net> 4.5.4-1
- update to 4.5.4 (2016-01-28, security and bugfix)

* Sat Dec 26 2015 Remi Collet <remi@remirepo.net> 4.5.3.1-1
- update to 4.5.3.1 (2015-12-25, security)
- raise dependency on udan11/sql-parser >= 3.0.8

* Wed Nov 25 2015 Remi Collet <remi@remirepo.net> 4.5.2-1
- update to 4.5.2 (2015-11-23, bugfix)
- raise dependency on udan11/sql-parser >= 3.0.5

* Fri Sep 25 2015 Remi Collet <remi@remirepo.net> 4.5.1-1
- update to 4.5.1 (2015-10-23, bugfix)
- raise dependency on udan11/sql-parser >= 3.0.3

* Fri Sep 25 2015 Remi Collet <remi@remirepo.net> 4.5.0.2-1
- update to 4.5.0.2 (2015-09-25, regression fix)

* Thu Sep 24 2015 Remi Collet <remi@remirepo.net> 4.5.0.1-1
- update to 4.5.0.1 (2015-09-24, regression fix)

* Wed Sep 23 2015 Remi Collet <remi@remirepo.net> 4.5.0-1
- update to 4.5.0 (2015-09-23, features release)
- raise php minimal version to 5.5

* Sun Sep 20 2015 Remi Collet <remi@remirepo.net> 4.4.15-1
- update to 4.4.15 (2015-09-20, last bugfix release)

* Mon Sep 14 2015 Remi Collet <remi@remirepo.net> 4.5.0-0.1.rc1
- update to 4.5.0-rc1

* Wed Sep  9 2015 Remi Collet <remi@remirepo.net> 4.4.14.1-1
- update to 4.4.14.1 (2015-09-08, security)
- fix PMASA-2015-4

* Sun Sep  6 2015 Remi Collet <remi@remirepo.net> 4.4.14-2
- switch to phpseclib v2 for PHP 7
  see https://github.com/phpmyadmin/phpmyadmin/issues/11387

* Fri Aug 21 2015 Remi Collet <remi@remirepo.net> 4.4.14-1
- update to 4.4.14 (2015-08-20, bugfix)

* Sat Aug  8 2015 Remi Collet <remi@remirepo.net> 4.4.13.1-1
- update to 4.4.13.1 (2015-08-08, bugfix)

* Fri Aug  7 2015 Remi Collet <remi@remirepo.net> 4.4.13-1
- update to 4.4.13 (2015-08-07, bugfix)

* Tue Jul 21 2015 Remi Collet <remi@remirepo.net> 4.4.12-1
- update to 4.4.12 (2015-07-20, bugfix)
- fix sources URL

* Mon Jul  6 2015 Remi Collet <remi@remirepo.net> 4.4.11-1
- update to 4.4.11 (2015-07-06, bugfix)

* Wed Jun 17 2015 Remi Collet <remi@remirepo.net> 4.4.10-1
- update to 4.4.10 (2015-06-17, bugfix)

* Thu Jun  4 2015 Remi Collet <rpms@famillecollet.com> 4.4.9-1
- update to 4.4.9 (2015-06-04, bugfix)

* Thu May 28 2015 Remi Collet <rpms@famillecollet.com> 4.4.8-1
- update to 4.4.8 (2015-05-28, bugfix)

* Sat May 16 2015 Remi Collet <rpms@famillecollet.com> 4.4.7-1
- update to 4.4.7 (2015-05-16, bugfix)

* Wed May 13 2015 Remi Collet <rpms@famillecollet.com> 4.4.6.1-1
- update to 4.4.6.1 (2015-05-13, security)
- fix for PMASA-2015-2 and PMASA-2015-3

* Thu May  7 2015 Remi Collet <rpms@famillecollet.com> 4.4.6-1
- update to 4.4.6 (2015-05-07, bugfix)

* Tue May  5 2015 Remi Collet <rpms@famillecollet.com> 4.4.5-1
- update to 4.4.5 (2015-05-05, bugfix)

* Sun Apr 26 2015 Remi Collet <rpms@famillecollet.com> 4.4.4-1
- update to 4.4.4 (2015-04-26, bugfix)

* Mon Apr 20 2015 Remi Collet <rpms@famillecollet.com> 4.4.3-1
- update to 4.4.3 (2015-04-20, bugfix)

* Mon Apr 13 2015 Remi Collet <rpms@famillecollet.com> 4.4.2-1
- update to 4.4.2 (2015-04-13, bugfix)

* Wed Apr  8 2015 Remi Collet <rpms@famillecollet.com> 4.4.1.1-1
- update to 4.4.1.1 (2015-04-08, urgent fix)

* Tue Apr  7 2015 Remi Collet <rpms@famillecollet.com> 4.4.1-1
- update to 4.4.1 (2015-04-07, bugfix)

* Thu Apr  2 2015 Remi Collet <rpms@famillecollet.com> 4.4.0-1
- update to 4.4.0 (2015-04-01, new features)

* Sun Mar 29 2015 Remi Collet <rpms@famillecollet.com> 4.3.13
- update to 4.3.13 (2015-03-29, bugfix)

* Thu Mar 26 2015 Remi Collet <rpms@famillecollet.com> 4.4.0-0.1.rc1
- update to 4.4.0-rc1
- move examples into package documentation

* Sun Mar 15 2015 Remi Collet <rpms@famillecollet.com> 4.3.12
- update to 4.3.12 (2015-03-14, bugfix)

* Thu Mar  5 2015 Remi Collet <rpms@famillecollet.com> 4.3.11.1-1
- update to 4.3.11.1 (2015-03-04, security)

* Tue Mar  3 2015 Remi Collet <rpms@famillecollet.com> 4.3.11-1
- update to 4.3.11 (2015-03-02, bugfix)

* Fri Feb 20 2015 Remi Collet <rpms@famillecollet.com> 4.3.10-1
- update to 4.3.10 (Fri, 20 Feb 2015, bugfix)

* Tue Feb 10 2015 Remi Collet <rpms@famillecollet.com> 4.3.9-1
- update to 4.3.9 (Thu, 5 Feb 2015, bugfix)

* Sat Jan 24 2015 Remi Collet <rpms@famillecollet.com> 4.3.8-1
- update to 4.3.8 (Sat, 24 Jan 2015, bugfix)

* Thu Jan 15 2015 Remi Collet <rpms@famillecollet.com> 4.3.7-1
- update to 4.3.7 (Wed, 15 Jan 2015, bugfix)

* Thu Jan  8 2015 Remi Collet <rpms@famillecollet.com> 4.3.6-1
- update to 4.3.6 (Wed, 7 Jan 2015, bugfix)

* Mon Jan  5 2015 Remi Collet <rpms@famillecollet.com> 4.3.5-1
- update to 4.3.5 (Mon, 5 Jan 2015, bugfix)

* Mon Dec 29 2014 Remi Collet <rpms@famillecollet.com> 4.3.4-1
- update to 4.3.4 (Mon, 29 Dec 2014, bugfix)

* Sun Dec 21 2014 Remi Collet <rpms@famillecollet.com> 4.3.3-1
- update to 4.3.3 (Sun, 21 Dec 2014, bugfix)

* Fri Dec 12 2014 Remi Collet <rpms@famillecollet.com> 4.3.2-1
- update to 4.3.2 (Fri, 12 Dec 2014, bugfix)

* Mon Dec  8 2014 Remi Collet <rpms@famillecollet.com> 4.3.1-1
- update to 4.3.1 (Mon, 8 Dec 2014, bugfix)

* Fri Dec  5 2014 Remi Collet <rpms@famillecollet.com> 4.3.0-1
- update to 4.3.0 (Fri, 5 Dec 2014, new features)

* Wed Dec  3 2014 Remi Collet <rpms@famillecollet.com> 4.3.0-0.2.rc2
- update to 4.3.0-rc2

* Wed Dec  3 2014 Remi Collet <rpms@famillecollet.com> 4.2.13.1-1
- update to 4.2.13 (Wed, 3 Dec 2014, security)

* Tue Dec  2 2014 Remi Collet <rpms@famillecollet.com> 4.3.0-0.1.rc1
- update to 4.3.0-rc1
- examples are now required at runtime

* Sun Nov 30 2014 Remi Collet <rpms@famillecollet.com> 4.2.13-1
- update to 4.2.13 (Sun, 30 Nov 2014, bugfix)

* Thu Nov 20 2014 Remi Collet <rpms@famillecollet.com> 4.2.12-1
- update to 4.2.12 (Thu, 20 Nov 2014, bugfix and security)

* Fri Oct 31 2014 Remi Collet <rpms@famillecollet.com> 4.2.11-1
- update to 4.2.11 (Fri, 31 Oct 2014, bugfix)

* Tue Oct 21 2014 Remi Collet <rpms@famillecollet.com> 4.2.10.1-1
- update to 4.2.10.1 (Tue, 21 Oct 2014, bugfix)
- fix for PMASA-2014-12
- drop dependency on php-gmp

* Sat Oct 11 2014 Remi Collet <rpms@famillecollet.com> 4.2.10-1
- update to 4.2.10 (Sat, 11 Oct 2014, bugfix)

* Sat Oct  4 2014 Remi Collet <rpms@famillecollet.com> 4.2.9.1-2
- provide nginx configuration (Fedora >= 21)

* Wed Oct  1 2014 Remi Collet <rpms@famillecollet.com> 4.2.9.1-1
- update to 4.2.9.1 (Wed, 1 Oct 2014, security)
- fix for PMASA-2014-11

* Sat Sep 20 2014 Remi Collet <rpms@famillecollet.com> 4.2.9-1
- update to 4.2.9 (Sat, 20 Sep 2014, bugfix)

* Sat Sep 13 2014 Remi Collet <rpms@famillecollet.com> 4.2.8.1-1
- update to 4.2.8.1 (Sat, 13 Sep 2014, security)
- fix for PMASA-2014-10

* Sun Aug 31 2014 Remi Collet <rpms@famillecollet.com> 4.2.8-1
- update to 4.2.8 (Sun, 31 Aug 2014, bugfix)

* Mon Aug 18 2014 Remi Collet <rpms@famillecollet.com> 4.2.7.1-2
- restrict access to /etc/phpMyAdmin and /var/lib/phpMyAdmin

* Sun Aug 17 2014 Remi Collet <rpms@famillecollet.com> 4.2.7.1-1
- update to 4.2.7.1 (Sun, 17 Aug 2014, security)
- fix for PMASA-2014-8 and PMASA-2014-9

* Thu Jul 31 2014 Remi Collet <rpms@famillecollet.com> 4.2.7-1
- update to 4.2.7 (Thu, 31 Jul 2014, bugfix)

* Thu Jul 31 2014 Remi Collet <rpms@famillecollet.com> 4.2.6-3
- move documentation in /usr/share/doc
- move License in /usr/share/licenses

* Fri Jul 18 2014 Remi Collet <rpms@famillecollet.com> 4.2.6-2
- fix links on home page

* Fri Jul 18 2014 Remi Collet <rpms@famillecollet.com> 4.2.6-1
- update to 4.2.6 (Thu, 17 Jul 2014, security)
- fix for PMASA-2014-4 to PMASA-2014-7

* Tue Jul  8 2014 Remi Collet <rpms@famillecollet.com> 4.2.5-2
- apply upstream patch to use system phpseclib
- add dependency on php-phpseclib-crypt-aes

* Thu Jun 26 2014 Remi Collet <rpms@famillecollet.com> 4.2.5-1
- update to 4.2.5 (Thu, 26 Jun 2014, bugfix)

* Sun Jun 22 2014 Remi Collet <rpms@famillecollet.com> 4.2.4-1
- update to 4.2.4 (Fri, 20 Jun 2014, security)
- fix for PMASA-2014-2 and PMASA-2014-3

* Tue Jun 10 2014 Remi Collet <rpms@famillecollet.com> 4.2.3-1
- update to 4.2.3 (Sun, 08 June 2014, bugfix)

* Thu May 22 2014 Remi Collet <rpms@famillecollet.com> 4.2.2-1
- update to 4.2.2 (Tue, 20 May 2014, bugfix)

* Tue May 13 2014 Remi Collet <rpms@famillecollet.com> 4.2.1-1
- update to 4.2.1 (Tue, 13 May 2014, bugfix)

* Thu May  8 2014 Remi Collet <rpms@famillecollet.com> 4.2.0-1
- update to 4.2.0 (Thu, 08 May 2014)

* Mon Apr 28 2014 Remi Collet <rpms@famillecollet.com> 4.1.14-1
- update to 4.1.14 (Sat, 26 Apr 2014, bugfix)

* Sun Apr 13 2014 Remi Collet <rpms@famillecollet.com> 4.1.13-1
- update to 4.1.13 (Sun, 13 Apr 2014, bugfix)

* Thu Mar 27 2014 Remi Collet <rpms@famillecollet.com> 4.1.12-1
- update to 4.1.12 (Thu, 27 Mar 2014, bugfix)

* Sun Mar 23 2014 Remi Collet <rpms@famillecollet.com> 4.1.11-1
- update to 4.1.11 (Sat, 22 Mar 2014, bugfix)

* Sat Mar 22 2014 Remi Collet <rpms@famillecollet.com> 4.1.10-1
- update to 4.1.10 (Sat, 22 Mar 2014, bugfix)

* Fri Mar  7 2014 Remi Collet <rpms@famillecollet.com> 4.1.9-1
- update to 4.1.9 (Thu, 06 Mar 2014, bugfix)

* Sat Feb 22 2014 Remi Collet <rpms@famillecollet.com> 4.1.8-1
- update to 4.1.8 (Sat, 22 Feb 2014, bugfix)

* Tue Feb 11 2014 Remi Collet <rpms@famillecollet.com> 4.1.7-1
- update to 4.1.7 (Sun, 09 Feb 2014, bugfix)

* Sun Jan 26 2014 Remi Collet <rpms@famillecollet.com> 4.1.6-1
- update to 4.1.6 (Sun, 26 Jan 2014, bugfix)

* Fri Jan 17 2014 Remi Collet <rpms@famillecollet.com> 4.1.5-1
- update to 4.1.5 (Fri, 17 Jan 2014, bugfix)

* Sat Jan 11 2014 Remi Collet <rpms@famillecollet.com> 4.1.4-2
- fix for f20 and unversioned docdir

* Tue Jan  7 2014 Remi Collet <rpms@famillecollet.com> 4.1.4-1
- update to 4.1.4 (Tue, 07 Jan 2014, bugfix)

* Tue Dec 31 2013 Remi Collet <rpms@famillecollet.com> 4.1.3-1
- update to 4.1.3 (Tue, 31 Dec 2013, bugfix)

* Mon Dec 23 2013 Remi Collet <rpms@famillecollet.com> 4.1.2-1
- update to 4.1.2 (Mon, 23 Dec 2013, bugfix)

* Tue Dec 17 2013 Remi Collet <rpms@famillecollet.com> 4.1.1-1
- update to 4.1.1 (bugfix)

* Thu Dec 12 2013 Remi Collet <rpms@famillecollet.com> 4.1.0-1
- update to 4.1.0 final

* Thu Dec 12 2013 Ville Skyttä <ville.skytta@iki.fi> - 3.5.8.2-2
- Fix paths to changelog and license when doc dir is unversioned (#994036).
- Fix source URL, use xz compressed tarball.

* Sat Dec  7 2013 Remi Collet <rpms@famillecollet.com> 4.1.0-0.3.rc3
- update to 4.1.0-rc3

* Wed Dec  4 2013 Remi Collet <rpms@famillecollet.com> 4.1.0-0.2.rc2
- update to 4.1.0-rc2

* Wed Dec  4 2013 Remi Collet <rpms@famillecollet.com> 4.0.10-1
- update to 4.0.10 (bugfix)

* Sat Nov 23 2013 Remi Collet <rpms@famillecollet.com> 4.1.0-0.1.rc1
- update to 4.1.0-rc1

* Tue Nov  5 2013 Remi Collet <rpms@famillecollet.com> 4.0.9-1
- update to 4.0.9 (bugfix)

* Sun Oct  6 2013 Remi Collet <rpms@famillecollet.com> 4.0.8-1
- update to 4.0.8 (bugfix)

* Mon Sep 23 2013 Remi Collet <rpms@famillecollet.com> 4.0.7-1
- update to 4.0.7 (bugfix)

* Sun Sep  8 2013 Remi Collet <rpms@famillecollet.com> 4.0.6-1
- update to 4.0.6

* Tue Aug 27 2013 Remi Collet <rpms@famillecollet.com> 4.0.6-0.1.rc1
- update to 4.0.6-rc1

* Mon Aug  5 2013 Remi Collet <rpms@famillecollet.com> 4.0.5-1
- update to 4.0.5, security fixes for PMASA-2013-10

* Sun Jul 28 2013 Remi Collet <rpms@famillecollet.com> 4.0.4.2-1
- update to 4.0.4.2
  security fixes for PMASA-2013-8, PMASA-2013-9, PMASA-2013-11,
  PMASA-2013-12, PMASA-2013-13, PMASA-2013-14, PMASA-2013-15

* Mon Jul  1 2013 Remi Collet <rpms@famillecollet.com> 4.0.4.1-1
- update to 4.0.4.1 (security: PMASA-2013-7)

* Mon Jun 17 2013 Remi Collet <rpms@famillecollet.com> 4.0.4-1
- update to 4.0.4

* Wed Jun  5 2013 Remi Collet <rpms@famillecollet.com> 4.0.3-1
- update to 4.0.3

* Sat May 25 2013 Remi Collet <rpms@famillecollet.com> 4.0.2-1
- update to 4.0.2

* Sat May 18 2013 Remi Collet <rpms@famillecollet.com> 4.0.1-2
- only requires php-tcpdf-dejavu-sans-fonts

* Wed May 15 2013 Remi Collet <rpms@famillecollet.com> 4.0.1-1
- update to 4.0.1

* Mon May 13 2013 Remi Collet <rpms@famillecollet.com> 4.0.0-3
- upstream fixes for tcpdf 6.0

* Thu May  9 2013 Remi Collet <rpms@famillecollet.com> 4.0.0-2
- use system tcpdf library

* Fri May  3 2013 Remi Collet <rpms@famillecollet.com> 4.0.0-1
- update to 4.0.0 finale

* Sun Apr 28 2013 Remi Collet <rpms@famillecollet.com> 4.0.0-0.5.rc4
- 4.0.0-rc4

* Wed Apr 24 2013 Remi Collet <rpms@famillecollet.com> 4.0.0-0.4.rc3
- 4.0.0-rc3

* Tue Apr 16 2013 Remi Collet <rpms@famillecollet.com> 4.0.0-0.3.rc2
- 4.0.0-rc2

* Thu Apr  4 2013 Remi Collet <rpms@famillecollet.com> 4.0.0-0.2.rc1
- 4.0.0-rc1

* Wed Mar 27 2013 Remi Collet <rpms@famillecollet.com> 4.0.0-0.1.beta3
- 4.0.0-beta3
- remove all additional themes

* Fri Feb 15 2013 Remi Collet <rpms@famillecollet.com> 3.5.7-1
- Upstream released 3.5.7 (bugfix)
- patch for http://sourceforge.net/p/phpmyadmin/bugs/3828/
  MariaDB reported as MySQL

* Mon Jan 28 2013 Remi Collet <rpms@famillecollet.com> 3.5.6-1
- Upstream released 3.5.6 (bugfix)
- add theme metro 1.0

* Thu Dec 20 2012 Remi Collet <rpms@famillecollet.com> 3.5.5-1
- Upstream released 3.5.5 (bugfix)
- add theme cleanstrap 1.0

* Fri Nov 16 2012 Remi Collet <rpms@famillecollet.com> 3.5.4-1
- Upstream released 3.5.4 (bugfix)

* Fri Nov 16 2012 Remi Collet <rpms@famillecollet.com> 3.5.3-2
- update theme Darkblue/orange to 2.11
- add theme blueorange 1.0b

* Tue Oct  9 2012 Remi Collet <rpms@famillecollet.com> 3.5.3-1
- Upstream released 3.5.2.3 (security)
  fix PMASA-2012-6 and PMASA-2012-7

* Mon Sep  3 2012 Remi Collet <rpms@famillecollet.com> 3.5.2.2-1.1
- Obsoletes phpMyAdmin3

* Sun Aug 12 2012 Remi Collet <rpms@famillecollet.com> 3.5.2.2-1
- Upstream released 3.5.2.2 (security)
  fix PMASA-2012-4

* Fri Aug 03 2012 Remi Collet <rpms@famillecollet.com> 3.5.2.1-1
- Upstream released 3.5.2.1 (security)
  fix PMASA-2012-3

* Sun Jul 08 2012 Remi Collet <rpms@famillecollet.com> 3.5.2-1
- Upstream released 3.5.2 (bugfix release)

* Sun Jul 01 2012 Remi Collet <rpms@famillecollet.com> 3.5.2-0.1.rc1
- update to 3.5.2-rc1
- clean up spec, use system php-gettext

* Sat May 05 2012 Remi Collet <rpms@famillecollet.com> 3.5.1-2
- make config compatible httpd 2.2 / 2.4

* Fri May 04 2012 Remi Collet <rpms@famillecollet.com> 3.5.1-1
- Upstream released 3.5.1 (bugfix release)

* Tue Apr 10 2012 Remi Collet <rpms@famillecollet.com> 3.5.0-1
- Upstream released 3.5.0

* Wed Mar 28 2012 Remi Collet <rpms@famillecollet.com> 3.4.10.2-1
- Upstream released 3.4.10.2 (security)
  fix PMASA-2012-2

* Sat Feb 18 2012 Remi Collet <rpms@famillecollet.com> 3.4.10.1-1
- Upstream released 3.4.10.1 (security)
  fix PMASA-2012-1

* Tue Feb 14 2012 Remi Collet <rpms@famillecollet.com> 3.4.10-1
- Upstream released 3.4.10 (bugfix)

* Wed Dec 21 2011 Remi Collet <rpms@famillecollet.com> 3.4.9-1
- Upstream released 3.4.9 (bugfix and minor security)
  Fix PMASA-2011-19 and PMASA-2011-20

* Thu Dec 01 2011 Remi Collet <rpms@famillecollet.com> 3.4.8-1
- Upstream released 3.4.8 (security)
  Fix PMASA-2011-18
- remove patch merged upstream

* Sun Nov 13 2011 Remi Collet <rpms@famillecollet.com> 3.4.7.1-2
- add patch to avoid notice with php 5.4

* Sat Nov 12 2011 Remi Collet <rpms@famillecollet.com> 3.4.7.1-1
- Upstream released 3.4.7.1 (security)
  Fix PMASA-2011-17

* Sun Oct 23 2011 Remi Collet <rpms@famillecollet.com> 3.4.7-1
- Upstream released 3.4.7 (bugfix)
- add Paradice 3.4 theme

* Sun Oct 16 2011 Remi Collet <rpms@famillecollet.com> 3.4.6-1
- Upstream released 3.4.6 (security)
  Fix PMASA-2011-15 and PMASA-2011-16

* Wed Sep 14 2011 Remi Collet <rpms@famillecollet.com> 3.4.5-1
- Upstream released 3.4.5 (security)
  http://www.phpmyadmin.net/home_page/security/PMASA-2011-14.php

* Wed Aug 24 2011 Remi Collet <rpms@famillecollet.com> 3.4.4-1
- Upstream released 3.4.4 (security)
  http://www.phpmyadmin.net/home_page/security/PMASA-2011-13.php

* Sat Jul 23 2011 Remi Collet <rpms@famillecollet.com> 3.4.3.2-1
- Upstream released 3.4.3.2 (security)
  http://www.phpmyadmin.net/home_page/security/PMASA-2011-12.php
  http://www.phpmyadmin.net/home_page/security/PMASA-2011-9.php

* Sun Jul  3 2011 Remi Collet <rpms@famillecollet.com> 3.4.3.1-1
- Upstream released 3.4.3.1 (security)
  http://www.phpmyadmin.net/home_page/security/PMASA-2011-8.php
  http://www.phpmyadmin.net/home_page/security/PMASA-2011-5.php

* Mon Jun 27 2011 Remi Collet <rpms@famillecollet.com> 3.4.3-1
- Upstream released 3.4.3

* Fri Jun 10 2011 Remi Collet <rpms@famillecollet.com> 3.4.2-1
- Upstream released 3.4.2

* Thu May 26 2011 Remi Collet <rpms@famillecollet.com> 3.4.1-1
- Upstream released 3.4.1
  http://www.phpmyadmin.net/home_page/security/PMASA-2011-3.php
  http://www.phpmyadmin.net/home_page/security/PMASA-2011-4.php

* Wed May 11 2011 Remi Collet <rpms@famillecollet.com> 3.4.0-1
- Upstream released 3.4.0
- remove 3.3 themes and add 3.4 ones

* Sat Mar 19 2011 Remi Collet <rpms@famillecollet.com> 3.3.10-1
- Upstream released 3.3.10

* Fri Feb 11 2011 Remi Collet <rpms@famillecollet.com> 3.3.9.2-1
- Upstream released 3.3.9.2
  http://www.phpmyadmin.net/home_page/security/PMASA-2011-2.php

* Tue Feb 08 2011 Remi Collet <rpms@famillecollet.com> 3.3.9.1-1
- Upstream released 3.3.9.1
  http://www.phpmyadmin.net/home_page/security/PMASA-2011-1.php

* Sat Feb 05 2011 Remi Collet <rpms@famillecollet.com> 3.3.9-2
- upstream patches for CVE-2010-4480 and CVE-2010-4481

* Mon Jan 03 2011 Remi Collet <rpms@famillecollet.com> 3.3.9-1
- Upstream released 3.3.9
- update pmamhomme to 1.0b
- don't requires php (to allow nginx or lighttpd instead of apache)

* Mon Oct 25 2010 Remi Collet <rpms@famillecollet.com> 3.3.8.1-1
- Upstream released 3.3.8.1
- add pmamhomme 1.0 theme

* Mon Oct 25 2010 Remi Collet <rpms@famillecollet.com> 3.3.8-1
- Upstream released 3.3.8

* Tue Sep 07 2010 Remi Collet <rpms@famillecollet.com> 3.3.7-1
- Upstream released 3.3.7

* Sun Aug 29 2010 Remi Collet <rpms@famillecollet.com> 3.3.6-1
- Upstream released 3.3.6

* Fri Aug 20 2010 Remi Collet <rpms@famillecollet.com> 3.3.5.1-1
- Upstream released 3.3.5.1

* Mon Jul 26 2010 Remi Collet <rpms@famillecollet.com> 3.3.5-1
- Upstream released 3.3.5

* Tue Jun 29 2010 Remi Collet <rpms@famillecollet.com> 3.3.4-1
- Upstream released 3.3.4
- add Paradice 3.0b theme

* Mon May 10 2010 Remi Collet <rpms@famillecollet.com> 3.3.3-1.###.remi
- Upstream released 3.3.3
- clean old changelog entry (version < 3.0.0)

* Thu Mar 18 2010 Remi Collet <rpms@famillecollet.com> 3.3.1-1.###.remi
- Upstream released 3.3.1

* Mon Mar 08 2010 Remi Collet <rpms@famillecollet.com> 3.3.0-1.###.remi
- Upstream released 3.3.0
- remove obsolete 3.2 themes (clearview3, crimson_gray, grid, hillside, paradice)
- add new 3.3 themes (smooth_yellow, arctic_ocean)
- add some required extensions (gd, mcrypt)
- add upload, save, config dir in /var/lib/phpMyAdmin
- use vendor_config.php
- swicth to mysqli

* Sun Jan 10 2010 Remi Collet <rpms@famillecollet.com> 3.2.5-1.###.remi
- Upstream released 3.2.5 (bug fixes)
- build for EOL fedora and EL

* Wed Dec 02 2009 Remi Collet <rpms@famillecollet.com> 3.2.4-1.###.remi
- Upstream released 3.2.4 (bug fixes)
- build for EOL fedora and EL

* Fri Oct 30 2009 Remi Collet <rpms@famillecollet.com> 3.2.3-1.###.remi
- Upstream released 3.2.3 (bug fixes)
- build for EOL fedora and EL

* Tue Oct 13 2009 Remi Collet <rpms@famillecollet.com> 3.2.2.1-1.###.remi
- Upstream released 3.2.2.1 (security fix)
- build for EOL fedora and EL

* Sun Sep 13 2009 Remi Collet <rpms@famillecollet.com> 3.2.2-1.###.remi
- Upstream released 3.2.2 (bug fixes)
- build for EOL fedora and EL

* Tue Jun 30 2009 Remi Collet <rpms@famillecollet.com> 3.2.1-1.###.remi
- Upstream released 3.2.1 (bug fixes and a new language: Uzbek)
- build for EOL fedora and EL

* Tue Jun 30 2009 Remi Collet <rpms@famillecollet.com> 3.2.0.1-1.###.remi
- Upstream released 3.2.0.1 (security release)
- build for EOL fedora and EL

* Mon Jun 15 2009 Remi Collet <rpms@famillecollet.com> 3.2.0-1.###.remi
- Upstream released 3.2.0
- build for EOL fedora and EL
- add theme clearview3-3.1.zip
- add theme crimson_gray-3.1-3.2.zip
- add theme grid-2.11d.zip
- add theme hillside-3.0.zip
- add theme paradice-3.0a.zip

* Fri May 15 2009 Remi Collet <rpms@famillecollet.com> 3.1.5-1.###.remi
- Upstream released 3.1.5
- build for EOL fedora and EL

* Sat Apr 25 2009 Remi Collet <rpms@famillecollet.com> 3.1.4-1.###.remi
- Upstream released 3.1.4
- build for EOL fedora and EL

* Tue Apr 14 2009 Remi Collet <rpms@famillecollet.com> 3.1.3.2-1.###.remi
- Upstream released 3.1.3.1
- build for EOL fedora and EL

* Wed Mar 25 2009 Remi Collet <rpms@famillecollet.com> 3.1.3.1-1.###.remi
- build for EOL fedora and EL

* Wed Mar 25 2009 Robert Scheck <robert@fedoraproject.org> 3.1.3.1-1
- Upstream released 3.1.3.1 (#492066)

* Sun Mar 01 2009 Remi Collet <rpms@famillecollet.com> 3.1.3-1.###.remi
- Upstream released 3.1.3
- build for EOL fedora and EL

* Tue Jan 20 2009 Remi Collet <rpms@famillecollet.com> 3.1.2-1.###.remi
- rebuild for EOL fedora and EL

* Tue Jan 20 2009 Robert Scheck <robert@fedoraproject.org> 3.1.2-1
- Upstream released 3.1.2

* Fri Dec 12 2008 Remi Collet <rpms@famillecollet.com> 3.1.1-1.###.remi
- rebuild for EOL fedora and EL

* Thu Dec 11 2008 Robert Scheck <robert@fedoraproject.org> 3.1.1-1
- Upstream released 3.1.1 (#475954)

* Sat Nov 29 2008 Remi Collet <rpms@famillecollet.com> 3.1.0-1.###.remi
- rebuild for EOL fedora and EL

* Sat Nov 29 2008 Robert Scheck <robert@fedoraproject.org> 3.1.0-1
- Upstream released 3.1.0
- Replaced LocationMatch with Directory directive (#469451)

* Fri Oct 31 2008 Remi Collet <rpms@famillecollet.com> 3.0.1.1-1.###.remi
- rebuild for EOL fedora and EL

* Thu Oct 30 2008 Robert Scheck <robert@fedoraproject.org> 3.0.1.1-1
- Upstream released 3.0.1.1 (#468974)

* Thu Oct 23 2008 Remi Collet <rpms@famillecollet.com> 3.0.1-1.###.remi
- rebuild for EOL fedora

* Wed Oct 22 2008 Robert Scheck <robert@fedoraproject.org> 3.0.1-1
- Upstream released 3.0.1

* Sun Oct 19 2008 Robert Scheck <robert@fedoraproject.org> 3.0.0-1
- Upstream released 3.0.0

* Sun Oct 12 2008 Remi Collet <rpms@famillecollet.com> 3.0.0-1.fc#.remi
- update to 3.0.0
- update requires for php 5.2.0

