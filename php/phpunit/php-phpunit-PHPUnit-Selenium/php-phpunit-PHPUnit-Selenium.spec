%{!?__pear: %global __pear %{_bindir}/pear}
%global pear_name    PHPUnit_Selenium
%global pear_channel pear.phpunit.de

Name:           php-phpunit-PHPUnit-Selenium
Version:        1.3.2
Release:        1%{?dist}
Summary:        Selenium RC integration for PHPUnit

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/sebastianbergmann/phpunit-selenium
Source0:        http://pear.phpunit.de/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.9.4
BuildRequires:  php-channel(%{pear_channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(%{pear_channel}/PHPUnit) >= 3.7.0
Requires:       php(language) >= 5.3.3
Requires:       php-curl
Requires:       php-dom
# phpcompatinfo detected extensions in 1.3.2
Requires:       php-date
Requires:       php-pcre
Requires:       php-json
Requires:       php-reflection
Requires:       php-spl

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
Selenium RC integration for PHPUnit


%prep
%setup -q -c
cd %{pear_name}-%{version}
# package.xml is V2
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/PHPUnit/Extensions/SeleniumCommon
%{pear_phpdir}/PHPUnit/Extensions/SeleniumTestCase
%{pear_phpdir}/PHPUnit/Extensions/SeleniumTestCase.php
%{pear_phpdir}/PHPUnit/Extensions/Selenium2TestCase
%{pear_phpdir}/PHPUnit/Extensions/Selenium2TestCase.php
%{pear_phpdir}/PHPUnit/Extensions/SeleniumTestSuite.php
%{pear_phpdir}/PHPUnit/Extensions/SeleniumBrowserSuite.php


%changelog
* Mon Aug 26 2013 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- Update to 1.3.2

* Mon Jun 03 2013 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1

* Mon May 06 2013 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0

* Mon Feb 04 2013 Remi Collet <remi@fedoraproject.org> - 1.2.12-1
- Version 1.2.12 (stable) - API 1.2.1 (stable)

* Mon Dec 10 2012 Remi Collet <remi@fedoraproject.org> - 1.2.11-1
- Version 1.2.11 (stable) - API 1.2.1 (stable)

* Mon Oct 22 2012 Remi Collet <remi@fedoraproject.org> - 1.2.10-1
- Version 1.2.10 (stable) - API 1.2.1 (stable)

* Sat Sep 29 2012 Remi Collet <remi@fedoraproject.org> - 1.2.9-1
- Version 1.2.9 (stable) - API 1.2.1 (stable)
- raise dependencies: php 5.3.3, PHPUnit 3.7.0

* Thu Aug  9 2012 Remi Collet <remi@fedoraproject.org> - 1.2.8-1
- Version 1.2.8 (stable) - API 1.2.1 (stable)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Remi Collet <remi@fedoraproject.org> - 1.2.7-1
- Version 1.2.7 (stable) - API 1.2.1 (stable)

* Sun Apr 01 2012 Remi Collet <remi@fedoraproject.org> - 1.2.6-1
- Version 1.2.6 (stable) - API 1.2.1 (stable)

* Sat Mar 17 2012 Remi Collet <remi@fedoraproject.org> - 1.2.5-1
- Version 1.2.5 (stable) - API 1.2.1 (stable)

* Mon Mar 12 2012 Remi Collet <remi@fedoraproject.org> - 1.2.4-1
- Version 1.2.4 (stable) - API 1.2.1 (stable)

* Fri Feb 17 2012 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- Version 1.2.3 (stable) - API 1.2.1 (stable)

* Mon Jan 23 2012 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Version 1.2.1 (stable) - API 1.2.1 (stable)
- add Selenium2TestCase extension

* Mon Jan 16 2012 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Version 1.2.0 (stable) - API 1.2.0 (stable)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- Version 1.1.3 (stable) - API 1.1.0 (stable)

* Mon Dec 12 2011 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Version 1.1.2 (stable) - API 1.1.0 (stable)

* Wed Nov 30 2011 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Version 1.1.1 (stable) - API 1.1.0 (stable)

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Version 1.1.0 (stable) - API 1.1.0 (stable)

* Fri Jun 10 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.3-1
- Version 1.0.3 (stable) - API 1.0.0 (stable)
- remove PEAR hack (only needed for EPEL)
- raise PEAR dependency to 1.9.2

* Tue May  3 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.2-3
- rebuild for doc in /usr/share/doc/pear

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.2-1
- Version 1.0.2 (stable) - API 1.0.0 (stable)
- CHANGELOG and LICENSE are now in the tarball

* Wed Nov 17 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.1-1
- Version 1.0.1 (stable) - API 1.0.0 (stable)

* Fri Nov 05 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.0-2
- lower PEAR dependency to allow el6 build
- fix URL

* Sun Sep 26 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.0-1
- initial generated spec + clean

