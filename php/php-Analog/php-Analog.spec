# remirepo spec file for php-Analog, from:
#
# Fedora spec file for php-Analog
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global gh_owner   jbroadway
%global gh_project analog
%global gh_commit  9e02358735912ed203c073d192b5e07cb6b663dd
%global gh_short   %(c=%{gh_commit}; echo ${c:0:7})
#global gh_date    20150213
%global real_name  Analog

Name:           php-Analog
Summary:        PHP micro logging package
Version:        1.0.9
%if 0%{?gh_date}
Release:        5.%{gh_date}git%{gh_short}%{?dist}
%else
Release:        2%{?dist}
%endif
License:        MIT
Group:          Development/Libraries
URL:            https://github.com/jbroadway/analog
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-composer(fedora/autoloader)
# For tests
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php-composer(psr/log)

# from composer.json,  "require": {
#                "psr/log": "1.*",
#                "php": ">=5.3.2"
Requires:       php(language) >= 5.3.2
Requires:       php-composer(psr/log)
# From phpcompatinfo report
Requires:       php-curl
Requires:       php-date
Requires:       php-json
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl
Requires:       php-xml
# mongo is optional
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(analog/analog) = %{version}


%description
MicroPHP logging package based on the idea of using closures for
configurability and extensibility. It functions as a static class,
but you can completely control the writing of log messages through
a closure function (aka anonymous functions).

Analog also comes with over a dozen pre-written handlers,
with examples for each in the examples folder. These include:
- Amon - Send logs to the Amon server monitoring tool
- Buffer - Buffer messages to send all at once (works with File,
  Mail, Stderr, and Variable handlers)
- File - Append messages to a file
- FirePHP - Send messages to FirePHP browser plugin
- GELF - Send message to the Graylog2 log management server
- Ignore - Do nothing
- LevelBuffer - Buffer messages and send only if sufficient error
  level reached
- Mail - Send email notices
- Mongo - Save to MongoDB collection, requires php-pecl(mongo)
  package to be installed
- Multi - Send different log levels to different handlers
- Post - Send messages over HTTP POST to another machine
- Stderr - Send messages to STDERR
- Syslog - Send messages to syslog
- Variable - Buffer messages to a variable reference.

So while it's a micro class, it's highly extensible and very capable
out of the box too.

Autoloader: %{_datadir}/php/%{real_name}/autoload.php


%prep
%setup -qn %{gh_project}-%{gh_commit}


%build
cat << 'EOF' | tee -a lib/%{real_name}/autoload.php
<?php
/* Autoloader for analog/analog and its dependencies */

require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Analog\\', __DIR__);
\Fedora\Autoloader\Dependencies::required(array(
        '%{_datadir}/php/Psr/Log/autoload.php',
));
EOF


%install
rm -rf %{buildroot}

# install framework files
install -d %{buildroot}%{_datadir}/php
cp -a lib/%{real_name} %{buildroot}%{_datadir}/php/


%check
: Use and test our autoloader
cat <<EOF | tee tests/bootstrap.php
<?php
require '%{buildroot}%{_datadir}/php/%{real_name}/autoload.php';
EOF

: Run upstream test suite
run=0
ret=0
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



%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%doc examples lib/%{real_name}.php
%doc composer.json
%dir %{_datadir}/php/%{real_name}
%{_datadir}/php/%{real_name}/*


%changelog
* Mon Oct 31 2016 Remi Collet <remi@fedoraproject.org> - 1.0.9-2
- update to 1.0.9
- switch to fedora/autoloader

* Thu Aug 11 2016 Remi Collet <remi@fedoraproject.org> - 1.0.8-1
- update to 1.0.8

* Thu May  5 2016 Remi Collet <remi@fedoraproject.org> - 1.0.7-2
- generate a simple autoloader (and use it for test suite)

* Thu May 05 2016 Johan Cwiklinski <johan AT x-tnd DOT be> - 1.0.7-1
- Update to 1.0.7 (PHP7 compatible)

* Tue May 26 2015 Remi Collet <remi@fedoraproject.org> - 1.0.6-1
- update to 1.0.6
- composer dependencies
- add patch for PHP-7 (add Ignore, Null is deprecated)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-5.git9ab4c9e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4.git9ab4c9e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Feb 10 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 1.0.0-4.git9ab4c9e
- Add patch for locked file (https://github.com/jbroadway/analog/issues/7)
- Remove licence file and patch applied upstream
- Change github source URL

* Sun Dec 30 2012 Johan Cwiklinski <johan AT x-tnd DOT be> - 1.0.0-2.git876d8a3bb
- Fix a typo
- Run tests, add relevant BR and patch

* Sun Dec 30 2012 Johan Cwiklinski <johan AT x-tnd DOT be> - 1.0.0-1.git876d8a3bb
- Fix version
- remove not needeed php-hash requirement
- remove php-mongo requirement (add a line in %%description)
- remove unneeded macro
- add LICENSE file (upstream bug https://github.com/jbroadway/analog/issues/2)

* Mon Dec 24 2012 Johan Cwiklinski <johan AT x-tnd DOT be> - 1.0.0.1-1.git876d8a3bb
- Latest snapshot (bug fixes, new handlers)
- Fix Requires

* Sat Dec 01 2012 Johan Cwiklinski <johan AT x-tnd DOT be> - 1.0.0-1
- Initial packaging
