Name:           php-deepend-Mockery
Version:        0.9.1
Release:        2%{?dist}
Summary:        Mockery is a simple but flexible PHP mock object framework

Group:          Development/Libraries
License:        BSD
URL:            http://github.com/padraic/mockery
Source0:        https://github.com/padraic/mockery/archive/%{version}/mockery-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
# TODO: enable tests
# TODO: make hamcrest as dependency for additional features
Requires:       php(language) >= 5.3.2
#Requires:       pcre >= 7.0
Requires:       php-pcre
Requires:       php-spl
Requires:       php-reflection

Provides:       php-composer(mockery/mockery) = %{version}
Provides:       php-pear(pear.survivethedeepend.com/Mockery) = %{version}
Obsoletes:      php-channel-deepend <= 1.3


%description
Mockery is a simple but flexible PHP mock object framework for use in unit 
testing. It is inspired by Ruby's flexmock and Java's Mockito, borrowing 
elements from both of their APIs.

%prep
%setup -q -n mockery-%{version}


%build
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/php
cp -rp library/* %{buildroot}/%{_datadir}/php/


%clean
rm -rf %{buildroot}


%check
# We need this packages to pass tests
# hamcrest/hamcrest-php: ~1.1
# satooshi/php-coveralls: ~0.7@dev
# phpunit --include-path ./library:./tests -d date.timezone="UTC"


%post
if [ -x %{_bindir}/pear ]; then
  %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
    pear.survivethedeepend.com/Mockery >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc LICENSE README.md docs/*
%{_datadir}/php/Mockery/
%{_datadir}/php/Mockery.php


%changelog
* Wed Jul 16 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.9.1-2
- fixed requires (Remi)
- add script which will delete older pear package if installed (Remi)
- fix provides/obsoletes (Remi)

* Tue Jul 15 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.9.1-1
- update to 0.9.1 (RHBZ #1119451)

* Tue Feb 11 2014 Remi Collet <remi@fedoraproject.org> - 0.9.0-1
- Update to 0.9.0

* Fri Apr 19 2013 Remi Collet <remi@fedoraproject.org> - 0.8.0-1
- Update to 0.8.0 (backport)

* Thu Apr 18 2013 Christof Damian <christof@damian.net> - 0.8.0-1
- upstream 0.8.0

* Sun Mar 04 2012 Remi Collet <RPMS@FamilleCollet.com> - 0.7.2-1
- upstream 0.7.2, rebuild for remi repository

* Sun Mar  4 2012 Christof Damian <christof@damian.net> - 0.7.2-1
- upstream 0.7.2

* Tue Jul 27 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.6.3-2
- rebuild for remi repository

* Tue Jul 27 2010 Christof Damian <christof@damian.net> - 0.6.3-2
- add license and readme file from github

* Fri May 28 2010 Christof Damian <christof@damian.net> - 0.6.0-1
- initial packaging


