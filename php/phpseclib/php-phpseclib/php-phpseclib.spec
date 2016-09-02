%global composer_vendor         phpseclib
%global composer_project        phpseclib

%global github_owner            phpseclib
%global github_name             phpseclib
%global github_commit           41f85e9c2582b3f6d1b7d20395fb40c687ad5370
%global github_short            %(c=%{github_commit}; echo ${c:0:7})
%if 0%{?rhel} == 5
%global with_tests              0%{?_with_tests:1}
%else
%global with_tests              0%{!?_without_tests:1}
%endif

Name:       php-%{composer_vendor}
Version:    2.0.3
Release:    1%{?dist}
Summary:    PHP Secure Communications Library

Group:      System Environment/Libraries
License:    MIT
URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{name}-%{version}-%{github_short}.tgz
Source1:    %{name}-autoload.php
# Generate a full archive from git snapshot, with tests
Source2:    makesrc.sh

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{with_tests}
BuildRequires:  php-composer(symfony/class-loader)
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  %{_bindir}/phpab
# Optional at runtime, to avoid too muck skipped tests
BuildRequires:  php-bcmath
BuildRequires:  php-gmp
BuildRequires:  php-mcrypt
%endif

Requires:   php(language) >= 5.3.3
Requires:   php-bcmath
Requires:   php-date
Requires:   php-gmp
Requires:   php-hash
Requires:   php-openssl
Requires:   php-pcre
Requires:   php-session
Requires:   php-standard
Requires:   php-xml
Requires:   php-composer(symfony/class-loader)

Provides:   php-composer(%{composer_vendor}/%{composer_project}) = %{version}


%description
MIT-licensed pure-PHP implementations of an arbitrary-precision integer 
arithmetic library, fully PKCS#1 (v2.1) compliant RSA, DES, 3DES, RC4, 
Rijndael, AES, Blowfish, Twofish, SSH-1, SSH-2, SFTP, and X.509

%prep
%setup -qn %{github_name}-%{github_commit}
cp %{SOURCE1} %{composer_vendor}/autoload.php

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/php
cp -pr %{composer_vendor} %{buildroot}%{_datadir}/php

%if %{with_tests}
%check
%{_bindir}/phpab --output tests/bootstrap.php tests
echo 'require "%{buildroot}%{_datadir}/php/%{composer_vendor}/autoload.php";' >> tests/bootstrap.php

ret=0
run=0
if which php56; then
   php56 %{_bindir}/phpunit || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose
fi
exit $ret
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_datadir}/php/%{composer_vendor}
%doc AUTHORS CHANGELOG.md composer.json README.md
%{!?_licensedir:%global license %%doc}
%license LICENSE


%changelog
* Fri Sep  2 2016 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- update to 2.0.3

* Tue Jun  7 2016 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- update to 2.0.2

* Tue Jan 19 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1
- sources from git snapshot for tests
- run test suite with both PHP 5 and 7 when available

* Sun Sep  6 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-4
- change source0 to commit reference
- add BR for better test coverage
- add needed backport stuff for EL-5 in #remirepo

* Wed Sep 02 2015 François Kooman <fkooman@tuxed.net> - 2.0.0-3
- apply patch for test to avoid loading class that is now autoloaded

* Wed Sep 02 2015 François Kooman <fkooman@tuxed.net> - 2.0.0-2
- add autoload script
- make use of autoload script when running tests during build
- fix double inclusion of directory

* Sat Aug 08 2015 François Kooman <fkooman@tuxed.net> - 2.0.0-1
- initial package
