# remirepo/fedora spec file for php-mcnetic-zipstreamer
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    44c99c659abf4dac92882437c1da68de824ca9d0
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     McNetic
%global gh_project   PHPZipStreamer
%global with_tests   0%{!?_without_tests:1}
%global namespace    ZipStreamer

Name:           php-mcnetic-zipstreamer
Epoch:          1
Version:        0.7
Release:        1%{?dist}
Summary:        Stream zip files without i/o overhead

Group:          Development/Libraries
License:        GPLv3+
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# See https://github.com/McNetic/PHPZipStreamer/issues/29
Patch1:         %{name}-warn.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-composer(theseer/autoload)
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-date
BuildRequires:  php-hash
BuildRequires:  php-mbstring
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(phpunit/phpunit)
BuildRequires:  php-pecl(Xdebug)
BuildRequires:  php-pecl(pecl_http)
%endif

# From composer.json
#      "php": ">=5.3.0"
Requires:       php(language) >= 5.3.0
# From phpcompatinfo report for version0.7
Requires:       php-date
Requires:       php-hash
Requires:       php-mbstring
Requires:       php-spl
%if 0%{?fedora} > 21
# For compression
Recommends:     php-pecl(pecl_http)
%else
Requires:       php-pecl(pecl_http)
%endif

Provides:       php-composer(mcnetic/zipstreamer) = %{version}


%description
Simple Class to create zip files on the fly and stream directly to the
HTTP client as the content is added (without using temporary files).

Autoloader: %{_datadir}/php/%{namespace}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch1 -p0 -b .rpm
find . -name \*.rpm -exec rm {} \;


%build
%{_bindir}/phpab -o src/autoload.php src


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{_datadir}/php
cp -pr src %{buildroot}%{_datadir}/php/%{namespace}


%check
%if %{with_tests}
: Ensure we use our autoloader
sed -e '/^ZipStreamer.php/d' -i test/*php

if [ $(php -r "echo PHP_INT_SIZE;") -eq 8 ]; then
  : Run test suite
  %{_bindir}/phpunit \
    --bootstrap %{buildroot}%{_datadir}/php/%{namespace}/autoload.php \
    --configuration test/phpunit.xml
else
  : Ignore test suite as Count64 do not support 32 bits overflow
fi

if which php70; then
  : Run test suite with PHP 7.0 SCL
  php70 %{_bindir}/phpunit \
    --bootstrap %{buildroot}%{_datadir}/php/%{namespace}/autoload.php \
    --configuration test/phpunit.xml
fi
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc *.md
%doc composer.json
%{_datadir}/php/%{namespace}


%changelog
* Wed Jan 20 2016 Remi Collet <remi@fedoraproject.org> - 1:0.7.1
- fix version, from review #1296901

* Fri Jan  8 2016 Remi Collet <remi@fedoraproject.org> - 1.7.2
- ensure we use our autoloader during the test suite
- ignore test suite on 32bits build

* Fri Jan  8 2016 Remi Collet <remi@fedoraproject.org> - 1.7.1
- initial package
- add patch to workaround error raised by pecl_http
  see https://github.com/McNetic/PHPZipStreamer/issues/29