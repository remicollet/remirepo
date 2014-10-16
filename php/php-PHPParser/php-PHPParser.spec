%global github_owner    nikic
%global github_name     PHP-Parser
%global github_commit   b9a60372f26356feb85b4b9ca50a395a5f0d7f34

%global oldlib_name     PHPParser
%global newlib_name     PhpParser

%global php_min_ver     5.3

Name:          php-%{oldlib_name}
Version:       1.0.1
Release:       1%{?dist}
Summary:       A PHP parser written in PHP

Group:         Development/Libraries
License:       BSD
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# For tests
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: %{_bindir}/phpunit
# For tests: phpcompatinfo
BuildRequires: php-ctype
BuildRequires: php-filter
BuildRequires: php-pcre
BuildRequires: php-spl
BuildRequires: php-tokenizer

# From composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-tokenizer
# phpcompatinfo requires (for 1.0.0)
Requires:      php-filter
Requires:      php-pcre
Requires:      php-spl
Requires:      php-xmlreader
Requires:      php-xmlwriter

Obsoletes:     %{name}-test

Provides:      php-composer(nikic/php-parser) = %{version}


%description
A PHP parser written in PHP to simplify static analysis and code manipulation.


%prep
%setup -q -n %{github_name}-%{github_commit}


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php/%{oldlib_name}
cp -rp lib/%{newlib_name} %{buildroot}%{_datadir}/php/

# For compat with old version (wihtout namespace
ln -s ../%{newlib_name}/Autoloader.php \
   %{buildroot}%{_datadir}/php/%{oldlib_name}/Autoloader.php


%check
%{_bindir}/phpunit


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md doc grammar composer.json
%{_datadir}/php/%{oldlib_name}
%{_datadir}/php/%{newlib_name}


%changelog
* Thu Oct 16 2014 Remi Collet <remi@fedoraproject.org> 1.0.1-1
- Update to 1.0.1

* Fri Sep 12 2014 Remi Collet <remi@fedoraproject.org> 1.0.0-1
- Update to 1.0.0

* Wed Jul 23 2014 Remi Collet <remi@fedoraproject.org> 1.0.0-0.2.beta1
- composer dependencies
- fix license handling

* Mon May 12 2014 Remi Collet <remi@fedoraproject.org> 1.0.0-0.1.beta1
- Update to 1.0.0beta1
- library in /usr/share/php/PhpParser
- provide /usr/share/php/PHPParser/Autoloader.php for compatibility
- drop dependencies on xmlreader and xmlwriter

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
