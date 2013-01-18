%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%global pear_name   PHP_CompatInfo
%global channel     bartlett.laurent-laville.org

# TODO : link /usr/share/pear/data/PHP_CompatInfo/misc/jquery-min.js
#        to system jquery when available, then fix License (BSD only)


Name:           php-bartlett-PHP-CompatInfo
Version:        2.12.1
Release:        1%{?dist}
Summary:        Find out version and the extensions required for a piece of code to run

Group:          Development/Libraries
# PHP-CompatInfo is BSD, bundled jquery is MIT (or GPL)
License:        BSD and MIT
URL:            http://php5.laurent-laville.org/compatinfo/
Source0:        http://bartlett.laurent-laville.org/get/%{pear_name}-%{version}%{?prever}.tgz

# Update reference for PHP 5.5
# https://github.com/remicollet/php-compat-info/commits/issue-php55
Patch1:         0001-cuirl-reference-for-php-5.5.patch
Patch2:         0002-hash-reference-for-php-5.5.patch
Patch3:         0003-tokoniser-reference-for-php-5.5.patch
Patch4:         0004-standard-reference-for-php-5.5.patch
Patch5:         0005-snmp-reference-for-php-5.5.patch
Patch6:         0006-openssl-reference-for-php-5.5.patch
Patch7:         0007-mysqli-reference-for-php-5.5.patch
Patch8:         0008-Fix-json-reference-for-PHP-5.5.patch
Patch9:         0009-Fix-intl-reference-for-PHP-5.5.patch
Patch10:        0010-fix-Core-reference-for-PHP-5.5.patch
Patch11:        0011-fix-order-in-intl.patch
Patch12:        0012-curl-reference-for-php-5.5-more.patch
Patch13:        0013-use-LATEST_PHP_5_4-macro.patch
Patch14:        0014-curl-reference-for-php-5.5-more.patch
Patch15:        0015-mysqli-new-constant.patch
Patch16:        0016-MYSQLI_OPT_CAN_HANDLE_EXPIRED_PASSWORDS-is-5.4.12.patch
Patch17:        0017-data-reference-for-php-5.5-date-immutable.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.9.0
BuildRequires:  php-channel(%{channel})
# to run test suite
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit) >= 3.6.0
BuildRequires:  php-pear(%{channel}/PHP_Reflect) >= 1.5.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-common >= 5.2.1
Requires:       php-date
Requires:       php-dom
Requires:       php-libxml
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.9.0
Requires:       php-pear(%{channel}/PHP_Reflect) >= 1.5.0
Requires:       php-pear(Console_CommandLine) >= 1.2.0
# Optional
Requires:       php-pear(pear.phpunit.de/PHPUnit) >= 3.6.0
Requires:       php-pear(pear.phpunit.de/PHP_Timer) >= 1.0.0
# Optional and not yet availalble php-pear(Net_Growl) >= 2.2.2

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}%{?prever}


%description
PHP_CompatInfo will parse a file/folder/array to find out the minimum
version and extensions required for it to run. CLI version has many reports
(extension, interface, class, function, constant) to display and ability to
show content of dictionary references.

HTML Documentation:  %{pear_docdir}/%{pear_name}/html/index.html

This package provides experimental references for PHP 5.5.


%prep
%setup -q -c

# Package is V2
cd %{pear_name}-%{version}%{?prever}

%patch1  -p1
%patch2  -p1
%patch3  -p1
%patch4  -p1
%patch5  -p1
%patch6  -p1
%patch7  -p1
%patch8  -p1
%patch9  -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1

# remove checksum for patched files
sed -e 's/md5sum.*name/name/' \
    ../package.xml >%{name}.xml


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

# Fix wrong-script-end-of-line-encoding
sed -i -e 's/\r//' %{buildroot}%{_bindir}/phpci

# Create default package configuration
sed -e '/reference=/s/PHP5/ALL/' \
     %{buildroot}%{pear_cfgdir}/%{pear_name}/phpcompatinfo.xml.dist \
    >%{buildroot}%{pear_cfgdir}/%{pear_name}/phpcompatinfo.xml


%check
cd %{pear_name}-%{version}%{?prever}

%if 0%{?rhel} == 6
# php-5.3.3-CVE-2012-0057.patch add new constants from php 5.3.9
# so drop this test which fails with
# Constant 'XSL_SECPREF_CREATE_DIRECTORY', found in Reference (5.3.9,), exists.
rm -f tests/Reference/XslTest.php
%endif

# Tests: 654, Assertions: 9682, Skipped: 28, when most extensions installed
# OK, but incomplete or skipped tests!
# Tests: 462, Assertions: 5936, Skipped: 254, in mock
# Reference tests need some fixes for EL-4, so ignore result for now
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


%changelog
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

* Sat Jun 02 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.0.0-1
- Version 2.0.0 (stable) - API 2.0.0 (stable)
- add HTML documentation

* Tue Apr 26 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.0.0-0.3.RC4
- Version 2.0.0RC4 (beta) - API 2.0.0 (beta)

* Fri Mar 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.0.0-0.2.RC3
- Version 2.0.0RC3

* Wed Feb 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.0.0-0.1.RC2
- Version 2.0.0RC2
- Initial Release

