# remirepo spec file for php-phpmd-PHP-PMD, from
#
# Fedora spec file for php-phpmd-PHP-PMD
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%global gh_commit    148b605040ae6f7cc839e14a9e206beec9868d97
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     phpmd
%global gh_project   phpmd
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    PHP_PMD
%global pear_channel pear.phpmd.org
%global php_home     %{_datadir}/php/PHPMD
%global with_tests   0%{!?_without_tests:1}

Name:           php-phpmd-PHP-PMD
Version:        2.4.4
Release:        1%{?dist}
Summary:        PHPMD - PHP Mess Detector

Group:          Development/Libraries
License:        BSD
URL:            http://phpmd.org/
# git snashop to get upstream test suite
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh
# Autoloader
Source2:        %{name}-autoload.php
Patch0:         %{name}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
# For tests
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "^4.0",
#        "squizlabs/php_codesniffer": "^2.0"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.0
BuildRequires:  php(language) >= 5.3.9
BuildRequires:  php-composer(pdepend/pdepend) >= 2.0.4
BuildRequires:  php-date
BuildRequires:  php-libxml
BuildRequires:  php-pcre
BuildRequires:  php-simplexml
BuildRequires:  php-spl
# Autoloader
BuildRequires:  php-composer(fedora/autoloader)
%endif

# From composer.json,     "require": {
#        "php": ">=5.3.9",
#        "pdepend/pdepend": "^2.0.4",
Requires:       php(language) >= 5.3.9
Requires:       php-composer(pdepend/pdepend) >= 2.0.4
Requires:       php-composer(pdepend/pdepend) <  3
# From phpcompatinfo report for version 2.2.3
Requires:       php-date
Requires:       php-libxml
Requires:       php-pcre
Requires:       php-simplexml
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

# Single package in this channel
Obsoletes:      php-channel-phpmd <= 1.3

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
This is the project site of PHPMD. It is a spin-off project of PHP Depend 
and aims to be a PHP equivalent of the well known Java tool PMD. PHPMD can 
be seen as an user friendly front-end application for the raw metrics 
stream measured by PHP Depend.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p0
cp %{SOURCE2} src/main/php/PHPMD/autoload.php

find src/main/php -name \*php -exec sed -e 's:@package_version@:%{version}:' -i {} \;
find src/test     -type f     -exec sed -e 's:@package_version@:%{version}:' -i {} \;


%build
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}

: Library
mkdir -p $(dirname %{buildroot}%{php_home})
cp -pr src/main/php/PHPMD %{buildroot}%{php_home}

: Resources
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -pr src/main/resources %{buildroot}%{_datadir}/%{name}/resources

: Command
install -Dpm 0755 src/bin/phpmd %{buildroot}%{_bindir}/phpmd


%check
%if %{with_tests}
cat << 'EOF' | tee src/test/php/bootstrap.php
<?php
require '%{buildroot}%{php_home}/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('PHPMD\\',  __DIR__ . '/PHPMD');
EOF

# remirepo:11
ret=0
run=0
if which php71; then
    php71 %{_bindir}/phpunit --verbose || ret=1
    run=1
fi
if which php56; then
    php56 %{_bindir}/phpunit --verbose || ret=1
    run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose
# remirepo:2
fi
exit $ret
%else
: Test suite disabled
%endif


%pre
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      %{pear_channel}/%{pear_name} >/dev/null || :
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json
%doc CONTRIBUTING.md README.rst AUTHORS.rst
%doc CHANGELOG
%{php_home}
%{_datadir}/%{name}
%{_bindir}/phpmd


%changelog
* Tue Nov 22 2016 Remi Collet <remi@fedoraproject.org> - 2.4.4-1
- update to 2.4.4
- raise dependency on PHP 5.3.9
- switch to fedora/autoloader

* Thu Apr 21 2016 Remi Collet <remi@fedoraproject.org> - 2.4.3-1
- update to 2.4.3

* Fri Mar 11 2016 Remi Collet <remi@fedoraproject.org> - 2.4.2-1
- update to 2.4.2

* Wed Mar  9 2016 Remi Collet <remi@fedoraproject.org> - 2.4.1-1
- update to 2.4.1

* Tue Mar  8 2016 Remi Collet <remi@fedoraproject.org> - 2.3.3-1
- update to 2.3.3

* Fri Sep 25 2015 Remi Collet <remi@fedoraproject.org> - 2.3.2-1
- update to 2.3.2
- drop dependency on symfony

* Tue Sep 22 2015 Remi Collet <remi@fedoraproject.org> - 2.3.1-1
- update to 2.3.1

* Tue Sep 22 2015 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- update to 2.3.0

* Thu Jul  2 2015 Remi Collet <remi@fedoraproject.org> - 2.2.3-1
- update to 2.2.3
- switch from pear channel to git snapshot sources
- run upstream test suite during build

* Fri Jul 26 2013 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- Update to 1.5.0

* Fri Dec 14 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.4.1-1
- upstream 1.4.1 for remi repo
- spec cleanups

* Sat Sep  8 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.4.0-1
- upstream 1.4.0

* Sat Mar 03 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.3.3-1
- upstream 1.3.3

* Tue Feb 28 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.3.2-1
- upstream 1.3.2

* Thu Feb 23 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.3.1-1
- upstream 1.3.1

* Sat Feb 11 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.3.0-1
- upstream 1.3.0, rebuild for remi repository

* Thu Feb  9 2012 Christof Damian <christof@damian.net> - 1.3.0-1
- upstream 1.3.0

* Tue Nov 01 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.2.0-1
- upstream 1.2.0, rebuild for remi repository
- doc in /usr/share/doc/pear

* Fri Oct 28 2011 Christof Damian <christof@damian.net> - 1.2.0-1
- upstream 1.2.0

* Sat Jul 16 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.1.1-1
- rebuild for remi repository

* Fri Jul 15 2011 Christof Damian <christof@damian.net> - 1.1.1-1
- upstream 1.1.1

* Fri Mar 25 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.1.0-1
- rebuild for remi repository

* Thu Mar 24 2011 Christof Damian <christof@damian.net> - 1.1.0-1
- upstream 1.1.0

* Wed Feb 16 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.0.1-1
- upstream 1.0.1 - bugfixes
- rebuild for remi repository

* Tue Feb 15 2011 Christof Damian <christof@damian.net> - 1.0.1-1
- upstream 1.0.1 - bugfixes

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.0.0-1
- upstream stable release 1.0.0
- rebuild for remi repository

* Sun Feb  6 2011 Christof Damian <christof@damian.net> - 1.0.0-1
- upstream stable release 1.0.0

* Sun Oct  3 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.2.7-1
- new upstream
- rebuild for remi repository

* Sat Oct  2 2010 Christof Damian <christof@damian.net> - 0.2.7-1
- new upstream

* Mon Jul  5 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.2.6-1
- rebuild for remi repository

* Sun Jul  4 2010 Christof Damian <christof@damian.net> - 0.2.6-1
- upstream 0.2.6

* Mon Apr  5 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.2.5-1
- rebuild for remi repository

* Sun Apr  4 2010 Christof Damian <christof@damian.net> - 0.2.5-1
- upsteam 0.2.5: bugfixes

* Tue Mar  9 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.2.4-1
- rebuild for remi repository

* Tue Mar  9 2010 Christof Damian <christof@damian.net> - 0.2.4-1
- upstream 0.2.4 : Small bugfix release which closes an E_NOTICE issue introduced with release 0.2.3

* Sat Mar  6 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.2.3-1
- rebuild for remi repository

* Thu Mar  4 2010 Christof Damian <christof@damian.net> - 0.2.3-1
- upstream 0.2.3
- increased php and pdepend requirements 

* Mon Feb 01 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.2.2-2
- rebuild for remi repository

* Sun Jan 31 2010 Christof Damian <christof@damian.net> - 0.2.2-2
- use pear_datadir in filesection

* Sat Jan 30 2010 Christof Damian <christof@damian.net> 0.2.2-1
- upstream 0.2.2
- changed define to global
- moved docs to /usr/share/doc
- use channel macro in postun

* Tue Jan 12 2010 Christof Damian <christof@damian.net> - 0.2.1-1
- upstream 0.2.1

* Fri Jan  1 2010 Christof Damian <christof@damian.net> 0.2.0-1
- initial release

