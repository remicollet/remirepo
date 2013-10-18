# spec file for php-bartlett-PHP-CompatInfo
#
# Copyright (c) 2011-2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name   PHP_CompatInfo
%global channel     bartlett.laurent-laville.org

# TODO : link /usr/share/pear/data/PHP_CompatInfo/misc/jquery-min.js
#        to system jquery when available, then fix License (BSD only)


Name:           php-bartlett-PHP-CompatInfo
Version:        2.24.0
Release:        1%{?dist}
Summary:        Find out version and the extensions required for a piece of code to run

Group:          Development/Libraries
# PHP-CompatInfo is BSD, bundled jquery is MIT (or GPL)
License:        BSD and MIT
URL:            http://php5.laurent-laville.org/compatinfo/
Source0:        http://bartlett.laurent-laville.org/get/%{pear_name}-%{version}%{?prever}.tgz
Source1:        https://raw.github.com/llaville/php-compat-info/master/misc/phpcompatinfo.1

# Update configuration for best experience
# Reference = ALL known extension (instead of installed ones)
# Make cache / save_path user specific
# Add .install .module to fileExtensions (for drupal)
Patch0:         %{pear_name}-conf.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.9.0
BuildRequires:  php-channel(%{channel})
# to run test suite
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit) >= 3.6.0
BuildRequires:  php-pear(%{channel}/PHP_Reflect) >= 1.9.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-date
Requires:       php-dom
Requires:       php-libxml
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.9.0
Requires:       php-pear(%{channel}/PHP_Reflect) >= 1.9.0
Requires:       php-pear(%{channel}/PHP_Reflect) <  2
Requires:       php-pear(Console_CommandLine) >= 1.2.0
# Optional
Requires:       php-pear(pear.phpunit.de/PHPUnit) >= 3.6.0
Requires:       php-pear(pear.phpunit.de/PHP_Timer) >= 1.0.0
# Optional and not yet availalble php-pear(Net_Growl) >= 2.2.2

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}%{?prever}
Provides:       phpci = %{version}%{?prever}
Provides:       phpcompatinfo = %{version}%{?prever}


%description
PHP_CompatInfo will parse a file/folder/array to find out the minimum
version and extensions required for it to run. CLI version has many reports
(extension, interface, class, function, constant) to display and ability to
show content of dictionary references.

HTML Documentation:  %{pear_docdir}/%{pear_name}/html/index.html


%prep
%setup -q -c

cd %{pear_name}-%{version}%{?prever}

# Copy upstream default configuration
cp phpcompatinfo.xml.dist phpcompatinfo.xml
# Apply our changes
%patch0  -p1 -b .rpm

cp ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}%{?prever}


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}%{?prever}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}

# Create default package configuration
install -pm 644 phpcompatinfo.xml %{buildroot}%{pear_cfgdir}/%{pear_name}/

# Install the man page
mkdir -p %{buildroot}%{_mandir}/man1
install -pm 644 %{SOURCE1} %{buildroot}%{_mandir}/man1/phpcompatinfo.1

# Keep old phpci command for compatibility (will be remove later)
cd %{buildroot}%{_bindir}
ln -s phpcompatinfo phpci


%check
cd %{pear_name}-%{version}%{?prever}

%if 0%{?rhel} == 6
# php-5.3.3-CVE-2012-0057.patch add new constants from php 5.3.9
# so drop this test which fails with
# Constant 'XSL_SECPREF_CREATE_DIRECTORY', found in Reference (5.3.9,), exists.
rm -f tests/Reference/XslTest.php
%endif

# OK, but incomplete or skipped tests!
# Tests: 810, Assertions: 10996, Skipped: 80, when most extensions installed
# Tests: 551, Assertions: 6833, Skipped: 378, in mock
# Reference tests need some fixes for EL-5, so ignore result for now
%{_bindir}/phpunit \
    -d date.timezone=UTC \
    -d memory_limit=-1 \
    --bootstrap %{buildroot}%{pear_phpdir}/Bartlett/PHP/CompatInfo/Autoload.php \
%if 0%{?rhel} < 6 && 0%{?fedora} < 8
    tests || exit 0
%else
    tests
%endif


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%dir %{pear_cfgdir}/%{pear_name}
# Editable configuration
%config(noreplace) %{pear_cfgdir}/%{pear_name}/phpcompatinfo.xml
# Default configuration
%{pear_cfgdir}/%{pear_name}/phpcompatinfo.xml.dist
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Bartlett/PHP/Compat*
%{pear_testdir}/%{pear_name}
%{pear_datadir}/%{pear_name}
%{_bindir}/phpci
%{_bindir}/phpcompatinfo
%{_mandir}/man1/phpcompatinfo.*


%changelog
* Fri Oct 18 2013 Remi Collet <remi@fedoraproject.org> - 2.24.0-1
- update to 2.24.0
- raise dependency, PHP_Reflect 1.9.0

* Sat Oct 12 2013 Remi Collet <remi@fedoraproject.org> - 2.24.0-0.1
- 2.24.0 test (not released)

* Mon Sep 23 2013 Remi Collet <remi@fedoraproject.org> - 2.23.1-1
- Update to 2.23.1

* Fri Sep 20 2013 Remi Collet <remi@fedoraproject.org> - 2.23.0-1
- Update to 2.23.0
- raise dependencies: PHP 5.3.0, PHP_Reflect 1.8.0 (and < 2)
- add patch for new constants in jsonc 1.3.2

* Fri Aug 23 2013 Remi Collet <remi@fedoraproject.org> - 2.22.0-1
- Update to 2.22.0

* Tue Aug 20 2013 Remi Collet <remi@fedoraproject.org> - 2.21.0-1
- Update to 2.21.0
- patch for https://github.com/llaville/php-compat-info/issues/99

* Thu Jul 25 2013 Remi Collet <remi@fedoraproject.org> - 2.20.0-1
- Update to 2.20.0
- patch from https://github.com/llaville/php-compat-info/pull/98

* Fri Jul 12 2013 Remi Collet <remi@fedoraproject.org> - 2.19.0-1
- Update to 2.19.0
- add module and install to fileExtensions in default configuration
  for drupal packages, #979830
- patch from https://github.com/llaville/php-compat-info/pull/95

* Wed Jun 26 2013 Remi Collet <remi@fedoraproject.org> - 2.18.0-1
- Update to 2.18.0
- raise dependencies, PHP_Reflect 1.7.0
- drop PHP 5.5 patches, applied upstream
- add patch for windows only constants

* Fri Jun 07 2013 Remi Collet <remi@fedoraproject.org> - 2.17.0-2
- keep phpci command for now

* Fri Jun 07 2013 Remi Collet <remi@fedoraproject.org> - 2.17.0-1
- Update to 2.17.0
- phpci command renamed to phpcompatinfo

* Fri May 10 2013 Remi Collet <remi@fedoraproject.org> - 2.16.0-1
- Update to 2.16.0

* Fri Apr 12 2013 Remi Collet <remi@fedoraproject.org> - 2.15.0-2
- add upstream man page (from github)

* Fri Apr 12 2013 Remi Collet <remi@fedoraproject.org> - 2.15.0-1
- Update to 2.15.0
- raise dependencies, PHP_Reflect 1.6.2
- add more patches for PHP 5.5 reference

* Tue Apr 02 2013 Remi Collet <remi@fedoraproject.org> - 2.14.1-1
- Update to 2.14.1
- make cache path user dependent

* Mon Mar 18 2013 Remi Collet <remi@fedoraproject.org> - 2.14.0-3
- add patch for broken extension report
  https://github.com/llaville/php-compat-info/issues/76

* Mon Mar 18 2013 Remi Collet <remi@fedoraproject.org> - 2.14.0-2
- provides phpci
- cleanups

* Mon Mar 18 2013 Remi Collet <remi@fedoraproject.org> - 2.14.0-1
- Update to 2.14.0

* Tue Feb 26 2013 Remi Collet <remi@fedoraproject.org> - 2.13.2-1
- Update to 2.13.2

* Tue Feb 26 2013 Remi Collet <remi@fedoraproject.org> - 2.13.1-1
- Update to 2.13.1
- raise dependencies, PHP_Reflect 1.6.1

* Fri Feb 22 2013 Remi Collet <remi@fedoraproject.org> - 2.13.0-1
- Update to 2.13.0
- raise dependencies, PHP_Reflect 1.6.0

* Fri Jan 18 2013 Remi Collet <remi@fedoraproject.org> - 2.12.1-1
- update to Version 2.12.1
- fix path to documentation in description

* Thu Jan 17 2013 Remi Collet <remi@fedoraproject.org> - 2.12.0-1
- update to Version 2.12.0
- drop dependency on eZ components
- raise PHPUnit dependency to 3.6.0
- update References for PHP 5.5 (non yet merged by upstream)

* Fri Dec 21 2012 Remi Collet <remi@fedoraproject.org> - 2.11.0-1
- update to Version 2.11.0
- html documentation is now provided by upstream

* Mon Nov 26 2012 Remi Collet <remi@fedoraproject.org> - 2.10.0-2
- generate documentation using asciidoc, without phing

* Mon Nov 26 2012 Remi Collet <remi@fedoraproject.org> - 2.10.0-1
- Version 2.10.0 (stable) - API 2.10.0 (stable)
- raise dependencies, PHP_Reflect 1.5.0
- drop documentation build

* Tue Oct 30 2012 Remi Collet <remi@fedoraproject.org> - 2.9.0-1
- Version 2.9.0 (stable) - API 2.9.0 (stable)
- raise dependencies, PHP_Reflect 1.4.3, Console_CommandLine 1.2.0

* Sat Sep 29 2012 Remi Collet <remi@fedoraproject.org> - 2.8.1-1
- Version 2.8.1 (stable) - API 2.8.0 (stable)

* Mon Sep 17 2012 Remi Collet <remi@fedoraproject.org> - 2.8.0-1
- Version 2.8.0 (stable) - API 2.8.0 (stable)
- new extensions : amqp, geoip, inclued, xcache

* Mon Sep  3 2012 Remi Collet <remi@fedoraproject.org> - 2.7.0-1
- Version 2.7.0 (stable) - API 2.7.0 (stable)

* Sun Aug 19 2012 Remi Collet <remi@fedoraproject.org> - 2.6.0-3
- rebuilt for new pear_datadir

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 2.6.0-2
- rebuildt for new pear_testdir

* Wed Aug 01 2012 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- Version 2.6.0 (stable) - API 2.6.0 (stable)
- raise dependencies: PHPUnit 3.6.0, PHP_Reflect 1.4.2

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul  8 2012 Remi Collet <remi@fedoraproject.org> - 2.5.0-1.1
- drop XslTest in EL-6

* Fri Jun 22 2012 Remi Collet <remi@fedoraproject.org> - 2.5.0-1
- Version 2.5.0 (stable) - API 2.5.0 (stable)
- use reference="ALL" in provided config

* Fri May 11 2012 Remi Collet <remi@fedoraproject.org> - 2.4.0-1.1
- add patch for old libxml

* Fri May 11 2012 Remi Collet <remi@fedoraproject.org> - 2.4.0-1
- Version 2.4.0 (stable) - API 2.3.0 (stable)

* Mon Mar 05 2012 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- Version 2.3.0 (stable) - API 2.3.0 (stable)

* Sat Feb 25 2012 Remi Collet <remi@fedoraproject.org> - 2.2.5-1
- Version 2.2.5 (stable) - API 2.2.0 (stable)

* Fri Feb 17 2012 Remi Collet <remi@fedoraproject.org> - 2.2.4-1
- Version 2.2.4 (stable) - API 2.2.0 (stable)

* Tue Feb 14 2012 Remi Collet <remi@fedoraproject.org> - 2.2.3-1
- Version 2.2.3 (stable) - API 2.2.0 (stable)

* Thu Feb 09 2012 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- Version 2.2.2 (stable) - API 2.2.0 (stable)

* Sun Feb 05 2012 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- Version 2.2.1 (stable) - API 2.2.0 (stable)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Sep 24 2011 Remi Collet <remi@fedoraproject.org> - 2.1.0-3.1
- no html doc on EL6

* Wed Sep 21 2011 Remi Collet <remi@fedoraproject.org> - 2.1.0-3
- remove all files with licensing issue
  don't use it during test, don't install it
  can keep it in sources are this files are still under free license

* Tue Sep 20 2011 Remi Collet <remi@fedoraproject.org> - 2.1.0-2
- comments from review #693204
- remove ascii*js (not used)
- add MIT to license for bundled jquery

* Thu Aug 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.1.0-1
- Version 2.1.0 (stable) - API 2.1.0 (stable)
- fix documentation for asciidoc 8.4

* Sat Jun 04 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.0.0-1
- Version 2.0.0 (stable) - API 2.0.0 (stable)
- add HTML documentation

* Tue Apr 26 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.0.0-0.3.RC4
- Version 2.0.0RC4 (beta) - API 2.0.0 (beta)

* Fri Mar 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.0.0-0.2.RC3
- Version 2.0.0RC3

* Wed Feb 23 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.0.0-0.1.RC2
- Version 2.0.0RC2
- Initial Release

