# remirepo/fedora spec file for php-znerol-php-stringprep
#
# Copyright (c) 2014-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global gh_commit    fe3f274cb0a862e7e511a7f2033301a06cbfb4f1
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_date      20150618
%global gh_owner     znerol
%global gh_project   Stringprep
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%global topdir       %{_datadir}/php/Znerol
%global basedir      %{topdir}/Component/Stringprep

Name:           php-znerol-php-stringprep
Version:        0
Release:        0.4.%{gh_date}git%{gh_short}%{?dist}
Summary:        Implementation of RFC 3454 Preparation of Internationalized Strings

Group:          Development/Libraries
License:        LGPLv3
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) > 5.3
BuildRequires:  php-iconv
BuildRequires:  php-intl
BuildRequires:  php-spl
BuildRequires:  php-phpunit-PHPUnit
%endif
BuildRequires:  php-theseer-autoload

# From documentation
Requires:       php(language) > 5.3
Requires:       php-iconv
Requires:       php-intl
# From phpcompatinfo
Requires:       php-spl

Provides:       php-composer(znerol/php-stringprep) = %{version}


%description
Implementation of RFC 3454 Preparation of Internationalized Strings.

See: http://tools.ietf.org/html/rfc3454


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate a simple autoloader
%{_bindir}/phpab \
   --exclude *Test.php \
   --output autoload.php \
   .


%install
rm -rf   %{buildroot}
mkdir -p %{buildroot}%{basedir}
cp -pr Profile RFC3454 *php \
         %{buildroot}%{basedir}


%check
%if %{with_tests}
# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap %{buildroot}%{basedir}/autoload.php || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap %{buildroot}%{basedir}/autoload.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --bootstrap %{buildroot}%{basedir}/autoload.php --verbose
# remirepo:2
fi
exit $ret
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md doc
%{topdir}


%changelog
* Sun Jul  3 2016 Remi Collet <remi@fedoraproject.org> - 0-0.4.20150618gitfe3f274
- new snapshot
- drop patch merges upstream

* Thu Jun 18 2015 Remi Collet <remi@fedoraproject.org> - 0-0.2.20150519git804b0d5
- add patch for autoload issue
  https://github.com/znerol/Stringprep/pull/6

* Tue May 19 2015 Remi Collet <remi@fedoraproject.org> - 0-0.1.20150519git804b0d5
- new snapshot (License PR merged)

* Sun Nov  9 2014 Remi Collet <remi@fedoraproject.org> - 0-0.1.20141109gita23ef29
- initial package (git snapshot)
