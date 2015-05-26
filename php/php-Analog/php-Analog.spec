%global commit 9ab4c9e462cd6804d74f6cae9ba967c054b1629e
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global real_name Analog
%global minus_name analog

%global devver 1

Name:           php-Analog
Summary:        PHP micro logging package
Version:        1.0.0
%if %{devver}
Release:        5.git%{shortcommit}%{?dist}
%else
Release:        3%{?dist}
%endif
%if %{devver}
Source0:        https://github.com/jbroadway/%{real_name}/archive/%{commit}/%{real_name}-%{version}-%{shortcommit}.tar.gz
%else
Source0:        https://github.com/downloads/jbroadway/%{minus_name}/%{minus_name}-%{version}-stable.tar.gz
%endif
URL:            https://github.com/jbroadway/analog
License:        MIT
Group:          Development/Libraries

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  php-pear(pear.phpunit.de/PHPUnit)

Requires:       php-common >= 5.3.0
Requires:       php-spl, php-date, php-json
Requires:       php-pcre, php-curl


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
- LevelBuffer - Buffer messages and send only if sufficient error
  level reached
- Mail - Send email notices
- Mongo - Save to MongoDB collection, requires php-pecl(mongo)
  package to be installed
- Multi - Send different log levels to different handlers
- Null - Do nothing
- Post - Send messages over HTTP POST to another machine
- Stderr - Send messages to STDERR
- Syslog - Send messages to syslog
- Variable - Buffer messages to a variable reference.

So while it's a micro class, it's highly extensible and very capable
out of the box too.


%prep
%if %{devver}
%setup -qn %{minus_name}-%{commit}
%else
%setup -qn %{minus_name}-%{version}-stable
%endif
#files that should not exist
find ./ -name "._*.php" -exec rm -f '{}' \;

#patch for locked file issue (applied upstreamà
sed -e "s/ | LOCK_NB//" -i lib/Analog/Handler/File.php


%build
# empty build section, nothing required


%install
rm -rf $RPM_BUILD_ROOT

# install framework files
install -d $RPM_BUILD_ROOT%{_datadir}/php
cp -a lib/%{real_name} $RPM_BUILD_ROOT%{_datadir}/php/


%check
#could fail because of seconds in date comparison
phpunit tests

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE README.md examples lib/%{real_name}.php
%dir %{_datadir}/php/%{real_name}
%{_datadir}/php/%{real_name}/*


%changelog
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

* Sun Dec 01 2012 Johan Cwiklinski <johan AT x-tnd DOT be> - 1.0.0-1
- Initial packaging
