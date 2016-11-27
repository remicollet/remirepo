# remirepo spec file for php-slim3, from
#
# Fedora spec file for php-slim3
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries

%global gh_commit   a685fe91a9435e1432e8eeb7cf516e2f5cee7f64
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    slimphp
%global gh_project  Slim
%global pk_project  slim
%global gh_version  3.6.0
%global php_home    %{_datadir}/php
%global slim_home   %{php_home}/Slim3


Name:           php-slim3
Summary:        PHP micro framework
Version:        %{gh_version}
Release:        1%{?dist}

# Use a git snapshot as upstream remove tests from distribution
Source0:       %{name}-%{gh_version}-%{gh_short}.tgz
# Script to pull the git snapshot
Source1:       %{name}-makesrc.sh

URL:            http://www.slimframework.com/
License:        MIT
Group:          Development/Libraries

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

#main app
BuildRequires:  php(language) >= 5.5.0
BuildRequires:  php-spl
BuildRequires:  php-simplexml
BuildRequires:  php-date
BuildRequires:  php-json
BuildRequires:  php-pcre
BuildRequires:  php-libxml
BuildRequires:  %{_bindir}/phpab
#test specific
BuildRequires:  php-composer(phpunit/phpunit) >= 4.0
BuildRequires:  php-mbstring
BuildRequires:  php-composer(psr/http-message) >= 1.0
BuildRequires:  php-composer(pimple/pimple) >= 3.0
BuildRequires:  php-composer(container-interop/container-interop) >= 1.1
BuildRequires:  php-composer(nikic/fast-route) >= 1.0

Requires:       php(language) >= 5.5.0
Requires:       php-spl
Requires:       php-simplexml
Requires:       php-date
Requires:       php-json
Requires:       php-pcre
Requires:       php-libxml
Requires:       php-composer(psr/http-message) >= 1.0
Requires:       php-composer(psr/http-message) < 2.0
Requires:       php-composer(pimple/pimple) >= 3.0
Requires:       php-composer(pimple/pimple) < 4.0
Requires:       php-composer(container-interop/container-interop) >= 1.1
Requires:       php-composer(container-interop/container-interop) < 2.0
Requires:       php-composer(nikic/fast-route) >= 1.0
Requires:       php-composer(nikic/fast-route) < 2.0

Provides:       php-composer(%{pk_project}/%{pk_project}) = %{version}
Provides:       php-composer(psr/http-message-implementation) = 1.0


%description
Slim is a PHP micro framework that helps you quickly write simple yet
powerful web applications and APIs.

Features:
- Powerful router
    - Standard and custom HTTP methods
    - Route parameters with wildcards and conditions
    - Route redirect, halt, and pass
    - Route middleware
- Template rendering with custom views
- Flash messages
- Secure cookies with AES-256 encryption
- HTTP caching
- Logging with custom log writers
- Error handling and debugging
- Middleware and hook architecture
- Simple configuration

Autoloader: %{slim_home}/autoload.php


%prep
%setup -qn %{gh_project}-%{gh_commit}


%build
: Generate a simple classmap autoloader
%{_bindir}/phpab \
  --output %{gh_project}/autoload.php \
  %{gh_project}

cat << 'EOF' | tee -a %{gh_project}/autoload.php

// Dependencies
require_once '%{php_home}/Psr/Http/Message/autoload.php';
require_once '%{php_home}/Interop/Container/autoload.php';
require_once '%{php_home}/Pimple/autoload.php';
require_once '%{php_home}/FastRoute/bootstrap.php';

EOF

: Generate a simple classmap autoloader for tests
%{_bindir}/phpab \
  --output tests/autoload.php \
  tests


%install
rm -rf %{buildroot}

# install framework files
install -d %{buildroot}%{slim_home}
cp -a %{gh_project}/* %{buildroot}%{slim_home}/


%check
sed -e \
        "s|dirname(__DIR__) . '/vendor/autoload.php'|'%{buildroot}%{slim_home}/autoload.php'|" \
        -e "s|\$autoloader->addPsr4.*$|require 'autoload.php';|" \
        -i tests/bootstrap.php

# OK (Tests: 512, Assertions: 820, Skipped: 13)
# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit -d memory_limit=-1 tests || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit -d memory_limit=-1 tests || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit \
    -d memory_limit=-1 \
    tests
# remirepo:2
fi
exit $ret


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%doc README.md CONTRIBUTING.md composer.json
%dir %{slim_home}/
%{slim_home}/*


%changelog
* Sun Nov 27 2016 Johan Cwiklinski <Johan AT x-tnd DOT be> - 3.6.0-1
- New upstream release

* Tue Jun 21 2016 Remi Collet <remi@fedoraproject.org> - 3.4.2-1
- update to 3.4.2

* Tue May 17 2016 Johan Cwiklinski <johan AT x-tnd DOT be> - 3.4.1-1
- Update to Slim 3
- Use a git snapshot as upstream drop tests from distribution (thanks to Remi)
- Remove tests subpackage
- Rename package to php-slim3

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 11 2015 Remi Collet <remi@fedoraproject.org> - 2.6.2-3
- fix autoloader name
- add comment about autoloader in package description

* Fri Oct 23 2015 Remi Collet <remi@fedoraproject.org> - 2.6.2-2
- provide php-composer(slim/slim)
- don't ignore test suite result
- add a simpler autoloader

* Thu Oct 22 2015 Johan Cwiklinski <johan AT x-tnd DOT be> - 2.6.2-1
- Last upstream release

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 10 2014 Johan Cwiklinski <johan AT x-tnd DOT be> - 2.4.3-1
- New upstream release

* Sun Dec 08 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 2.4.0-1
- New upstream release

* Thu Aug 08 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 2.3.0-1
- New upstream release

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 17 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 2.2.0-1
- New upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Nov 25 2012 Johan Cwiklinski <johan AT x-tnd DOT be> - 2.1.0-5
- Fix permissions on phpunit.xml.dist
- Remove not needeed %%if in %%check

* Sun Nov 25 2012 Johan Cwiklinski <johan AT x-tnd DOT be> - 2.1.0-4
- phpunit.xml.dist should not be in package's %%doc

* Sun Nov 25 2012 Johan Cwiklinski <johan AT x-tnd DOT be> - 2.1.0-3
- Remove unneedeed %%{real_name} subdirectory
- Move phpunit.xml.dist file in test subpackage

* Thu Nov 22 2012 Johan Cwiklinski <johan AT x-tnd DOT be> - 2.1.0-2
- Various changes and improvements thanks to Remi

* Wed Nov 21 2012 Johan Cwiklinski <johan AT x-tnd DOT be> - 2.1.0-1
- Initial packaging
