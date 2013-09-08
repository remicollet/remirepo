#global prever rc1

Name: phpMyAdmin
Version: 4.0.6
Release: 1%{?dist}
Summary: Web based MySQL browser written in php

Group: Applications/Internet
License: GPLv2+
URL: http://www.phpmyadmin.net/
Source0: http://downloads.sourceforge.net/sourceforge/phpmyadmin/%{name}-%{version}%{?prever:-%prever}-all-languages.tar.bz2
Source2: phpMyAdmin.htaccess

# https://github.com/phpmyadmin/phpmyadmin/pull/357
Patch0: %{name}-vendor.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: unzip

Requires:  webserver
Requires:  php(language) >= 5.2.0
Requires:  php-bcmath
Requires:  php-bz2
Requires:  php-ctype
Requires:  php-curl
Requires:  php-date
Requires:  php-filter
Requires:  php-gd
Requires:  php-gmp
Requires:  php-hash
Requires:  php-iconv
Requires:  php-json
Requires:  php-libxml
Requires:  php-mbstring
Requires:  php-mcrypt
Requires:  php-mysqli
Requires:  php-pcre
Requires:  php-recode
Requires:  php-session
Requires:  php-simplexml
Requires:  php-spl
Requires:  php-xmlwriter
Requires:  php-zip
Requires:  php-zlib
Requires:  php-php-gettext
Requires:  php-tcpdf
Requires:  php-tcpdf-dejavu-sans-fonts

Provides:  phpmyadmin = %{version}-%{release}
Obsoletes: phpMyAdmin3


%description
phpMyAdmin is a tool written in PHP intended to handle the administration of
MySQL over the Web. Currently it can create and drop databases,
create/drop/alter tables, delete/edit/add fields, execute any SQL statement,
manage keys on fields, manage privileges,export data into various formats and
is available in 50 languages


%prep
%setup -qn phpMyAdmin-%{version}%{?prever:-%prever}-all-languages

%patch0 -p1

# Minimal configuration file
sed -e "/'extension'/s@'mysql'@'mysqli'@"  \
    -e "/'blowfish_secret'/s@''@'MUSTBECHANGEDONINSTALL'@"  \
    -e "/'UploadDir'/s@''@'%{_localstatedir}/lib/%{name}/upload'@"  \
    -e "/'SaveDir'/s@''@'%{_localstatedir}/lib/%{name}/save'@" \
    config.sample.inc.php >CONFIG

# Setup vendor config file
sed -e "/'CHANGELOG_FILE'/s@./ChangeLog@%{_datadir}/doc/%{name}-%{version}/ChangeLog@" \
    -e "/'LICENSE_FILE'/s@./LICENSE@%{_datadir}/doc/%{name}-%{version}/LICENSE@" \
    -e "/'CONFIG_DIR'/s@'./'@'%{_sysconfdir}/%{name}/'@" \
    -e "/'SETUP_CONFIG_FILE'/s@./config/config.inc.php@%{_localstatedir}/lib/%{name}/config/config.inc.php@" \
    -e "/'GETTEXT_INC'/s@./libraries/php-gettext/gettext.inc@%{_datadir}/php/gettext/gettext.inc@" \
    -e "/'TCPDF_INC'/s@./libraries/tcpdf/tcpdf.php@%{_datadir}/php/tcpdf/tcpdf.php@" \
    -i libraries/vendor_config.php

# For debug
grep '^define' libraries/vendor_config.php

# to avoid rpmlint warnings
find . -name \*.php -exec chmod -x {} \;

#for archive in %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15} %{SOURCE16}
#do
#    %{__unzip} -q $archive -d themes
#done

# Remove bundled libraries
rm -rf libraries/php-gettext
rm -rf libraries/tcpdf


%build
# Nothing to do


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/%{name}
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
cp -ad ./* %{buildroot}/%{_datadir}/%{name}
cp %{SOURCE2} %{buildroot}/%{_sysconfdir}/httpd/conf.d/phpMyAdmin.conf
cp CONFIG %{buildroot}/%{_sysconfdir}/%{name}/config.inc.php

rm -f %{buildroot}/%{_datadir}/%{name}/*txt
rm -f %{buildroot}/%{_datadir}/%{name}/[CIRLT]*
rm -f %{buildroot}/%{_datadir}/%{name}/libraries/.htaccess
rm -f %{buildroot}/%{_datadir}/%{name}/setup/lib/.htaccess
rm -f %{buildroot}/%{_datadir}/%{name}/setup/frames/.htaccess
rm -rf %{buildroot}/%{_datadir}/%{name}/contrib

mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/{upload,save,config}
rm -rf %{buildroot}%{_datadir}/%{pkgname}/libraries/php-gettext
rm -rf %{buildroot}%{_datadir}/%{pkgname}/libraries/tcpdf


%clean
rm -rf %{buildroot}


%if %{?fedora}%{!?fedora:99} <= 16
%pre
echo -e "\nWARNING : Fedora %{fedora} is now EOL :"
echo -e "You should consider upgrading to a supported release.\n"
%endif

%post
# generate a secret key for this install
sed -i -e "/'blowfish_secret'/s/MUSTBECHANGEDONINSTALL/$RANDOM$RANDOM$RANDOM$RANDOM/" \
    %{_sysconfdir}/%{name}/config.inc.php


%files
%defattr(-,root,root,-)
%doc ChangeLog README LICENSE
%{_datadir}/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/config.inc.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%dir %{_localstatedir}/lib/%{name}/upload
%dir %attr(755,apache,root) %{_localstatedir}/lib/%{name}/save
%dir %attr(755,apache,root) %{_localstatedir}/lib/%{name}/config


%changelog
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

