# spec file for php-nrk-Predis
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Predis
%global pear_channel pear.nrk.io

%if 0%{?fedora} >= 18
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%else
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%endif

Name:           php-nrk-Predis
Version:        0.8.5
Release:        1%{?dist}
Summary:        PHP client library for Redis

Group:          Development/Libraries
License:        MIT
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.2
BuildRequires:  php-pear(PEAR)
BuildRequires:  php-channel(%{pear_channel})
%if %{with_tests}
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit)
BuildRequires:  redis > 2.6
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.2
Requires:       php-curl
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-session
Requires:       php-sockets
Requires:       php-spl
Requires:       php-pear(PEAR)
Requires:       php-channel(%{pear_channel})

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
Flexible and feature-complete PHP client library for Redis.


%prep
%setup -q -c

cd %{pear_name}-%{version}
cp ../package.xml %{name}.xml


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


%check
%if %{with_tests}

: Launch redis server
pidfile=$PWD/run/redis/redis.pid
mkdir -p {run,log,lib}/redis
sed -e "s:/var:$PWD:" \
    /etc/redis.conf >redis.conf
%{_sbindir}/redis-server \
    ./redis.conf \
    --daemonize yes \
    --pidfile $pidfile

: Run the installed test Suite against the installed library
pushd %{buildroot}%{pear_testdir}/%{pear_name}
ret=0
phpunit --include-path=%{buildroot}%{pear_phpdir} || ret=1
popd

: Cleanup
if [ -f $pidfile ]; then
   kill $(cat $pidfile)
fi

exit $ret
%else
%if 0%{?_without_tests:1}
: Test disabled, by '--without tests' option.
%else
: Test disabled, missing '--with tests' option.
%endif
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
