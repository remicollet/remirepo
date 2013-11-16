%global github_owner    nikic
%global github_name     PHP-Parser
%global github_version  0.9.4
%global github_commit   1e5e280ae88a27effa2ae4aa2bd088494ed8594f

%global lib_name        PHPParser

%global php_min_ver     5.2.0

Name:          php-%{lib_name}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       A PHP parser written in PHP

Group:         Development/Libraries
License:       BSD
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# For tests
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
# For tests: phpcompatinfo
BuildRequires: php-ctype
BuildRequires: php-filter
BuildRequires: php-pcre
BuildRequires: php-spl
BuildRequires: php-tokenizer
BuildRequires: php-xmlreader
BuildRequires: php-xmlwriter

Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo requires
Requires:      php-ctype
Requires:      php-filter
Requires:      php-pcre
Requires:      php-spl
Requires:      php-tokenizer
Requires:      php-xmlreader
Requires:      php-xmlwriter

Obsoletes:     %{name}-test

%description
A PHP parser written in PHP to simplify static analysis and code manipulation.


%prep
%setup -q -n %{github_name}-%{github_commit}


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php
cp -rp lib/%{lib_name} %{buildroot}%{_datadir}/php/


%check
%{_bindir}/phpunit


%files
%defattr(-,root,root,-)
%doc LICENSE *.md doc grammar composer.json
%{_datadir}/php/%{lib_name}


%changelog
* Sat Nov 16 2013 Remi Collet <remi@fedoraproject.org> 0.9.4-1
- backport 0.9.4 for remi repo.

* Fri Nov 15 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.9.4-1
- Updated to 0.9.4
- Spec cleanup

* Tue Jan  8 2013 Remi Collet <remi@fedoraproject.org> 0.9.3-2
- backport 0.9.3 for remi repo.

* Mon Dec 31 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 0.9.3-2
- Added php_min_ver
- Fixed requires for php_min_ver and non-Fedora

* Thu Dec 20 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 0.9.3-1
- Initial package
