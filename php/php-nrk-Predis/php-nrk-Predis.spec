# spec file for php-nrk-Predis
#
# Copyright (c) 2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Predis
%global pear_channel pear.nrk.io

%if 0%{?fedora} >= 18
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%else
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%endif

Name:           php-nrk-Predis
Version:        0.8.3
Release:        1%{?dist}
Summary:        PHP client library for Redis

Group:          Development/Libraries
License:        MIT
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz
# https://github.com/nrk/predis/issues/124
Source1:        https://raw.github.com/nrk/predis/master/LICENSE
# https://github.com/nrk/predis/issues/126
Source2:        https://raw.github.com/nrk/predis/master/autoload.php
Source3:        https://raw.github.com/nrk/predis/master/phpunit.xml.dist
# https://github.com/nrk/predis/issues/127
Patch0:         %{name}-tests.patch

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
# https://github.com/nrk/predis/issues/125
%setup -q -c -T
tar xif %{SOURCE0}

cd %{pear_name}-%{version}
%patch0 -p1
sed -e '/role="test"/s/md5sum.*name=/name=/' \
    ../package.xml >%{name}.xml


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

# Missing in package.xml
install -pm 644 %{SOURCE1} %{buildroot}%{pear_docdir}/%{pear_name}


%check
%if %{with_tests}
cd %{pear_name}-%{version}
cp %{SOURCE2} %{SOURCE3} .

# Launch redis server
mkdir -p {run,log,lib}/redis
sed -e "s:/var:$PWD:" \
    -e "/daemonize/s/no/yes/" \
    /etc/redis.conf >redis.conf
%{_sbindir}/redis-server ./redis.conf

# Run the test Suite
ret=0
phpunit . || ret=1

# Cleanup
if [ -f run/redis/redis.pid ]; then
   kill $(cat run/redis/redis.pid)
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
%{pear_testdir}/Predis


%changelog
* Wed Jun  5 2013 Remi Collet <remi@fedoraproject.org> - 0.8.3-1
- initial package
