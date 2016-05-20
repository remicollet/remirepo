#
# RPM spec file for php-PHPParser
#
# Copyright (c) 2012-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner    nikic
%global github_name     PHP-Parser
%global github_version  1.4.1
%global github_commit   f78af2c9c86107aa1a34cd1dbb5bbe9eeb0d9f51
%global github_short    %(c=%{github_commit}; echo ${c:0:7})

%global lib_name        PhpParser
%global lib_name_old    PHPParser

%global php_min_ver     5.3

%if 0
%global script  1
%else
%global script  0
%endif

Name:          php-%{lib_name_old}
Version:       %{github_version}
Release:       4%{?dist}
Summary:       A PHP parser written in PHP

Group:         Development/Libraries
License:       BSD
URL:           https://github.com/%{github_owner}/%{github_name}
# Upstream tarball don't provide test suite
# Use mksrc.sh to generate a git snapshot tarball
Source0:       %{name}-%{github_version}-%{github_short}.tgz
Source1:       makesrc.sh

# Patch for distribution
Patch0:        %{name}-command.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# For tests
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: %{_bindir}/phpunit
# For tests: phpcompatinfo (computed from version 1.4.1)
BuildRequires: php-ctype
BuildRequires: php-filter
BuildRequires: php-pcre
BuildRequires: php-spl
BuildRequires: php-tokenizer
BuildRequires: php-xmlreader
BuildRequires: php-xmlwriter

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-tokenizer
# phpcompatinfo (computed from version 1.4.1)
Requires:      php-filter
Requires:      php-pcre
Requires:      php-spl
Requires:      php-xmlreader
Requires:      php-xmlwriter
%if %{script}
Requires:      php-cli
%endif

Provides:      php-composer(nikic/php-parser) = %{version}


%description
A PHP parser written in PHP to simplify static analysis and code manipulation.
%if %{script}
This package provides the library version 1 and the php-parse command.
The php-nikic-php-parser package provides the library version 2.
%else
This package provides the library version 1.
The php-nikic-php-parser package provides the library version 2
and the  php-parse command.
%endif
Autoloader: '%{_datadir}/php/%{lib_name}/autoload.php';


%prep
%setup -q -n %{github_name}-%{github_short}

%patch0 -p0 -b .rpm
rm lib/%{lib_name}/*rpm


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php
cp -rp lib/%{lib_name} %{buildroot}%{_datadir}/php/%{lib_name}

# Compat with old version (< 1.0.0)
mkdir -p -m 755 %{buildroot}%{_datadir}/php/%{lib_name_old}
ln -s ../%{lib_name}/Autoloader.php \
    %{buildroot}%{_datadir}/php/%{lib_name_old}/Autoloader.php

%if %{script}
install -Dpm 755 bin/php-parse.php %{buildroot}%{_bindir}/php-parse
%endif


%check
%{_bindir}/phpunit \
    --bootstrap %{buildroot}%{_datadir}/php/%{lib_name}/autoload.php \
    --verbose


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md doc grammar composer.json
%if %{script}
%{_bindir}/php-parse
%endif
%{_datadir}/php/%{lib_name_old}
%{_datadir}/php/%{lib_name}


%changelog
* Fri May 20 2016 Remi Collet <remi@fedoraproject.org> - 1.4.1-4
- drop the php-parse command, provided by php-nikic-php-parser

* Sun Sep 20 2015 Remi Collet <remi@fedoraproject.org> - 1.4.1-1
- update to 1.4.1

* Sun Aug  9 2015 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- update to 1.4.0
- add a simple autoload.php

* Mon May  4 2015 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- update to 1.3.0

* Sat Apr  4 2015 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- update to 1.2.2

* Wed Feb 25 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-2
- provide the php-parse command

* Wed Feb 25 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0
- use git snapshot as upstream tarball don't provide the test suite

* Wed Nov  5 2014 Remi Collet <remi@fedoraproject.org> 1.0.2-1
- Update to 1.0.2

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
