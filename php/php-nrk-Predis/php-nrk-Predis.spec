# remirepo/fedora spec file for php-nrk-Predis
#
# Copyright (c) 2013-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear: %global __pear %{_bindir}/pear}
%global pear_name    Predis
%global pear_channel pear.nrk.io

%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%else
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%endif

Name:           php-nrk-Predis
Version:        1.1.0
Release:        1%{?dist}
Summary:        PHP client library for Redis

Group:          Development/Libraries
License:        MIT
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.9
BuildRequires:  php-pear(PEAR)
BuildRequires:  php-channel(%{pear_channel})
%if %{with_tests}
BuildRequires:  php-phpunit-PHPUnit
BuildRequires:  redis > 2.8
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.9
Requires:       php-reflection
Requires:       php-curl
Requires:       php-filter
Requires:       php-pcre
Requires:       php-session
Requires:       php-sockets
Requires:       php-spl
Requires:       php-pear(PEAR)
Requires:       php-channel(%{pear_channel})

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(predis/predis) = %{version}


%description
Flexible and feature-complete PHP client library for Redis.


%prep
%setup -q -c

cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}

# Relocate PATH so test suite can be run from install dir
sed -e 's:tests/::' \
    %{buildroot}%{pear_testdir}/%{pear_name}/phpunit.xml.dist \
  > %{buildroot}%{pear_testdir}/%{pear_name}/phpunit.xml


%check
%if %{with_tests}

: Launch redis server
pidfile=$PWD/run/redis/redis.pid
mkdir -p {run,log,lib}/redis
sed -e "s:/var:$PWD:" \
    /etc/redis.conf >redis.conf
%{_bindir}/redis-server \
    ./redis.conf \
    --daemonize yes \
    --pidfile $pidfile

: Run the installed test Suite against the installed library
pushd %{buildroot}%{pear_testdir}/%{pear_name}
ret=0
%{_bindir}/phpunit --include-path=%{buildroot}%{pear_phpdir} || ret=1

if which php70; then
   php70 %{_bindir}/phpunit --include-path=%{buildroot}%{pear_phpdir} || ret=1
fi
popd

: Cleanup
if [ -f $pidfile ]; then
   kill $(cat $pidfile)
fi

exit $ret
%else
: Test disabled
%endif


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/%{pear_name}
%{pear_testdir}/%{pear_name}


%changelog
* Tue Jun 07 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0

* Tue May 31 2016 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Fri Jul 31 2015 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Thu Jul 30 2015 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2

* Fri Jan 02 2015 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Mon Nov 03 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0
- upstream patch for tests

* Wed Jul 16 2014 Remi Collet <remi@fedoraproject.org> - 0.8.6-1
- Update to 0.8.6
- provides php-composer(predis/predis)
- enable test suite in EL-7

* Thu Jan 16 2014 Remi Collet <remi@fedoraproject.org> - 0.8.5-1
- Update to 0.8.5 (stable)

* Wed Jan  8 2014 Remi Collet <remi@fedoraproject.org> - 0.8.5-0
- Update to 0.8.5 (test build)

* Sun Jul 28 2013 Remi Collet <remi@fedoraproject.org> - 0.8.4-1
- Update to 0.8.4

* Wed Jul  3 2013 Remi Collet <remi@fedoraproject.org> - 0.8.3-2
- fixed sources, https://github.com/nrk/predis/issues/125

* Wed Jun  5 2013 Remi Collet <remi@fedoraproject.org> - 0.8.3-1
- initial package
