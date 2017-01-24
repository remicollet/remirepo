# remirepo spec file for php-echonest-api, from:
#
# Fedora spec file for php-echonest-api
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global commit 662d62a7df1247515572bf517e14b795714e0824
%global short_commit %(echo %{commit} | cut -c 1-8)

Name:       php-echonest-api
Version:    0
Release:    0.3.20131228git.%{short_commit}%{?dist}
BuildArch:  noarch

License:    MIT
Summary:    PHP classes for the Echo Nest API
URL:        https://github.com/Afterster/php-echonest-api
Source0:    %{url}/archive/%{commit}.tar.gz
Source1:    autoload.php

BuildRequires: php-phpunit-PHPUnit   

Requires:      php(language) >= 5.2.0
Requires:      php-curl
Requires:      php-date
Requires:      php-json
Requires:      php-spl
Requires:      php-xml


%description
A simple, Object Oriented API wrapper for the EchoNest Api written with PHP5.
This library is modeled after the php-github-api library built by ornicar.


%prep
%setup -q -n %{name}-%{commit}

echo $(ls ..)

chmod a-x LICENSE
chmod a-x README.md

# https://github.com/Afterster/php-echonest-api/pull/1
find . -name "*.php" | xargs chmod 0644


%install
install -d -p -m 0755 %{buildroot}/%{_datadir}/php

cp -a -r lib/EchoNest %{buildroot}/%{_datadir}/php/

install -p -m 0644 %{S:1} %{buildroot}/%{_datadir}/php/EchoNest


%check
# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap %{buildroot}/%{_datadir}/php/EchoNest/autoload.php || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap %{buildroot}/%{_datadir}/php/EchoNest/autoload.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
phpunit --bootstrap=%{buildroot}/%{_datadir}/php/EchoNest/autoload.php
# remirepo:2
fi
exit $ret


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%{_datadir}/php/EchoNest


%changelog
* Tue Jan 24 2017 Remi Collet <remi@remirepo.net> - 0-0.3.20131228git.662d62a7
- backport for remi repo

* Sat Jan 21 2017 Randy Barlow <bowlofeggs@fedoraproject.org> - 0-0.3.20131228git.662d62a7
- Add the commit date into the release.
- Remove the execute bit on php files.
- Do not require php virtual provides by version.

* Sat Jan 14 2017 Randy Barlow <bowlofeggs@fedoraproject.org> - 0-0.2.git.662d62a7
- Depend on php(language) instead of php.
- Use the full commit reference.
- Require needed php components explicitly.
- Included a simple autoload.php file.
- Run the tests against the installed library.

* Sun Jan 08 2017 Randy Barlow <bowlofeggs@fedoraproject.org> - 0-0.1.git.662d62a7
- Initial release.
