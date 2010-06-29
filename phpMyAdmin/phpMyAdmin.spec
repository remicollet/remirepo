Name: phpMyAdmin
Version: 3.3.4
Release: 1%{?dist}
Summary: Web based MySQL browser written in php

Group:	Applications/Internet
License: GPLv2+
URL: http://www.phpmyadmin.net/	
Source0: http://downloads.sourceforge.net/sourceforge/phpmyadmin/%{name}-%{version}-all-languages.tar.bz2
Source2: phpMyAdmin.htaccess

Source10: http://downloads.sourceforge.net/sourceforge/phpmyadmin/smooth_yellow-3.3.zip
Source11: http://downloads.sourceforge.net/sourceforge/phpmyadmin/arctic_ocean-3.3.zip
Source12: http://downloads.sourceforge.net/sourceforge/phpmyadmin/paradice-3.0b.zip


# See https://sourceforge.net/tracker/?func=detail&atid=377410&aid=2965613&group_id=23067
Patch0:   phpMyAdmin-vendor.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires: unzip
Requires: webserver 
Requires: php >= 5.2.0
Requires: php-mysql >= 5.2.0
Requires: php-mbstring >= 5.2.0
Requires: php-gd >= 5.2.0
Requires: php-mcrypt >= 5.2.0
Provides: phpmyadmin = %{version}-%{release}


%description
phpMyAdmin is a tool written in PHP intended to handle the administration of
MySQL over the Web. Currently it can create and drop databases,
create/drop/alter tables, delete/edit/add fields, execute any SQL statement,
manage keys on fields, manage privileges,export data into various formats and
is available in 50 languages


%prep
%setup -qn phpMyAdmin-%{version}-all-languages

%patch0 -p0

# Minimal configuration file
sed -e "/'extension'/s@'mysql'@'mysqli'@"  \
    -e "/'blowfish_secret'/s@''@'MUSTBECHANGEDONINSTALL'@"  \
    -e "/'UploadDir'/s@''@'%{_localstatedir}/lib/%{name}/upload'@"  \
    -e "/'SaveDir'/s@''@'%{_localstatedir}/lib/%{name}/save'@" \
    config.sample.inc.php >CONFIG

# Setup vendor config file
sed -e "/'CHANGELOG_FILE'/s@./ChangeLog@%{_datadir}/doc/%{name}-%{version}/ChangeLog@" \
    -e "/'LICENSE_FILE'/s@./LICENSE@%{_datadir}/doc/%{name}-%{version}/LICENSE@" \
    -e "/'CONFIG_FILE'/s@./config.inc.php@%{_sysconfdir}/%{name}/config.inc.php@" \
    -e "/'SETUP_CONFIG_FILE'/s@./config/config.inc.php@%{_localstatedir}/lib/%{name}/config/config.inc.php@" \
    -i libraries/vendor_config.php

# For debug
grep '^define' libraries/vendor_config.php

# to avoid rpmlint warnings
find . -name \*.php -exec chmod -x {} \;

for archive in %{SOURCE10} %{SOURCE11} %{SOURCE12}
do
    %{__unzip} -q $archive -d themes
done


%build
# Nothing to do


%install
rm -rf %{buildroot}
%{__mkdir} -p %{buildroot}/%{_datadir}/%{name}
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/%{name}
%{__cp} -ad ./* %{buildroot}/%{_datadir}/%{name}
%{__cp} %{SOURCE2} %{buildroot}/%{_sysconfdir}/httpd/conf.d/phpMyAdmin.conf
%{__cp} CONFIG %{buildroot}/%{_sysconfdir}/%{name}/config.inc.php

%{__rm} -f %{buildroot}/%{_datadir}/%{name}/*txt
%{__rm} -f %{buildroot}/%{_datadir}/%{name}/[CIRLT]*
%{__rm} -f %{buildroot}/%{_datadir}/%{name}/libraries/.htaccess
%{__rm} -f %{buildroot}/%{_datadir}/%{name}/setup/lib/.htaccess
%{__rm} -rf %{buildroot}/%{_datadir}/%{name}/contrib
%{__rm} -rf %{buildroot}/%{_datadir}/%{name}/documentation-gsoc

%{__mkdir} -p %{buildroot}/%{_localstatedir}/lib/%{name}/{upload,save,config}


%clean
rm -rf %{buildroot}


%if %{?fedora}%{!?fedora:99} <= 10
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
%doc ChangeLog README LICENSE CREDITS TODO Documentation.txt documentation-gsoc
%{_datadir}/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/config.inc.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/phpMyAdmin.conf
%dir %{_localstatedir}/lib/%{name}/upload
%dir %attr(755,apache,root) %{_localstatedir}/lib/%{name}/save
%dir %attr(755,apache,root) %{_localstatedir}/lib/%{name}/config


%changelog
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

* Wed Jun 30 2009 Remi Collet <rpms@famillecollet.com> 3.2.1-1.###.remi
- Upstream released 3.2.1 (bug fixes and a new language: Uzbek)
- build for EOL fedora and EL

* Wed Jun 30 2009 Remi Collet <rpms@famillecollet.com> 3.2.0.1-1.###.remi
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

