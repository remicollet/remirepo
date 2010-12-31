%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

%global    extname   igbinary


Summary:        Replacement for the standard PHP serializer
Name:           php-igbinary
Version:        1.0.2
Release:        3%{?dist}
License:        BSD
Group:          System Environment/Libraries

URL:            http://opensource.dynamoid.com/
Source0:        http://opensource.dynamoid.com/%{extname}-%{version}.tar.gz

# git clone https://github.com/phadej/igbinary.git
# tar czf igbinary-tests.tgz -C igbinary tests
Source1:        %{extname}-tests.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
BuildRequires:  php-devel php-pear

%if %{?php_zend_api}0
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
%else
Requires:       php-api = %{php_apiver}
%endif


%{?filter_setup:
%filter_from_provides /%{extname}.so/d
%filter_setup
}


%description
Igbinary is a drop in replacement for the standard PHP serializer.

Instead of time and space consuming textual representation, 
igbinary stores PHP data structures in a compact binary form. 
Savings are significant when using memcached or similar memory
based storages for serialized data.


%package devel
Summary:       Igbinary developer files (header)
Group:         Development/Libraries
Requires:      php-igbinary = %{version}-%{release}
Requires:      php-devel

%description devel
These are the files needed to compile programs using Igbinary


%prep
%setup -q -n %{extname}-%{version}

# Take tests directory from SVN which have some php 5.3 fixes
%{__tar} xzf %{SOURCE1}


%build
%{_bindir}/phpize
%{configure}
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

%{__mkdir} -p %{buildroot}%{_sysconfdir}/php.d/
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{extname}.ini <<EOF
; Enable %{extname} extension module
extension=%{extname}.so

; Enable or disable compacting of duplicate strings
; The default is On.
;igbinary.compact_strings=On

; Use igbinary as session serializer
;session.serialize_handler=igbinary
EOF


%check
# simple module load test
%{_bindir}/php --no-php-ini \
    --define extension_dir=modules \
    --define extension=%{extname}.so \
    --modules | grep %{extname}

# For now : Tests failed: 3, Tests passed: 35
NO_INTERACTION=1 %{__make} test

%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING CREDITS ChangeLog NEWS README
%config(noreplace) %{_sysconfdir}/php.d/%{extname}.ini
%{php_extdir}/%{extname}.so


%files devel
%defattr(-,root,root,-)
%{_includedir}/php/ext/%{extname}/%{extname}.h


%changelog
* Fri Dec 31 2010 Remi Collet <rpms@famillecollet.com> 1.0.2-3
- updated tests from Git.

* Sat Oct 23 2010 Remi Collet <rpms@famillecollet.com> 1.0.2-2
- filter provides to avoid igbinary.so
- add missing %%dist

* Wed Sep 29 2010 Remi Collet <rpms@famillecollet.com> 1.0.2-1
- initital RPM

