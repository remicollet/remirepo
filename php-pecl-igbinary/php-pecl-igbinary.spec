%{!?phpname: %{expand: %%global phpname php}}

%if %{phpname} == php
%global phpbindir      %{_bindir}
%global phpconfdir     %{_sysconfdir}
%global phpincldir     %{_includedir}
%else
%global phpbindir      %{_bindir}/%{phpname}
%global phpconfdir     %{_sysconfdir}/%{phpname}
%global phpincldir     %{_includedir}/%{phpname}
%endif

%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

%global    extname   igbinary


Summary:        Replacement for the standard PHP serializer
Name:           %{phpname}-pecl-igbinary
Version:        1.1.1
Release:        1%{?dist}
# http://pecl.php.net/bugs/22599
License:        BSD
Group:          System Environment/Libraries

URL:            http://pecl.php.net/package/igbinary
Source0:        http://pecl.php.net/get/%{extname}-%{version}.tgz
# http://pecl.php.net/bugs/22598
Source1:        %{extname}-tests.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
BuildRequires:  %{phpname}-pecl-apc-devel >= 3.1.7
BuildRequires:  %{phpname}-pear
BuildRequires:  %{phpname}-devel >= 5.2.0

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       %{phpname}(zend-abi) = %{php_zend_api}
Requires:       %{phpname}(api) = %{php_core_api}
Obsoletes:      %{phpname}-%{extname} <= 1.1.1
Provides:       %{phpname}-%{extname} = %{version}-%{release}
Provides:       %{phpname}-%{extname}%{?_isa} = %{version}-%{release}
Provides:       %{phpname}-pecl(%{extname}) = %{version}


%if 0%{?fedora}%{?rhel} > 4
%{?filter_setup:
%filter_from_provides /%{extname}.so/d
%filter_setup
}
%endif


%description
Igbinary is a drop in replacement for the standard PHP serializer.

Instead of time and space consuming textual representation, 
igbinary stores PHP data structures in a compact binary form. 
Savings are significant when using memcached or similar memory
based storages for serialized data.


%package devel
Summary:       Igbinary developer files (header)
Group:         Development/Libraries
Requires:      %{phpname}-pecl-%{extname}%{?_isa} = %{version}-%{release}
Requires:      %{phpname}-devel%{?_isa}
Obsoletes:     %{phpname}-%{extname}-devel <= 1.1.1
Provides:      %{phpname}-%{extname}-devel = %{version}-%{release}
Provides:      %{phpname}-%{extname}-devel%{?_isa} = %{version}-%{release}

%description devel
These are the files needed to compile programs using Igbinary


%prep
%setup -q -c
cd %{extname}-%{version}
%{__tar} xzf %{SOURCE1}

%build
cd %{extname}-%{version}
%{phpbindir}/phpize
%{configure} --with-php-config=%{phpbindir}/php-config
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{pecl_xmldir}
%{__install} -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

cd %{extname}-%{version}
%{__make} install INSTALL_ROOT=%{buildroot}

%{__mkdir} -p %{buildroot}%{phpconfdir}/php.d/
%{__cat} > %{buildroot}%{phpconfdir}/php.d/%{extname}.ini <<EOF
; Enable %{extname} extension module
extension=%{extname}.so

; Enable or disable compacting of duplicate strings
; The default is On.
;igbinary.compact_strings=On

; Use igbinary as session serializer
;session.serialize_handler=igbinary

; Use igbinary as APC serializer
;apc.serializer=igbinary
EOF


%check
cd %{extname}-%{version}

# simple module load test
# (without APC to ensure than can run without)
%{phpbindir}/php --no-php-ini \
    --define extension_dir=modules \
    --define extension=%{extname}.so \
    --modules | grep %{extname}

# APC required for test 045
%{__ln_s} %{php_extdir}/apc.so modules/

NO_INTERACTION=1 %{__make} test | tee rpmtests.log
grep -q "FAILED TEST" rpmtests.log && exit 1


%clean
%{__rm} -rf %{buildroot}


%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif


%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{extname} >/dev/null || :
fi
%endif



%files
%defattr(-,root,root,-)
%doc %{extname}-%{version}/COPYING
%doc %{extname}-%{version}/CREDITS
%doc %{extname}-%{version}/ChangeLog
%doc %{extname}-%{version}/NEWS
%doc %{extname}-%{version}/README
%config(noreplace) %{phpconfdir}/php.d/%{extname}.ini
%{php_extdir}/%{extname}.so
%{pecl_xmldir}/%{name}.xml


%files devel
%defattr(-,root,root,-)
%{phpincldir}/php/ext/%{extname}


%changelog
* Mon Mar 14 2011 Remi Collet <rpms@famillecollet.com> 1.1.1-1
- version 1.1.1 published on pecl.php.net
- rename to php-pecl-igbinary

* Mon Jan 17 2011 Remi Collet <rpms@famillecollet.com> 1.1.1-2
- allow relocation using phpname macro

* Mon Jan 17 2011 Remi Collet <rpms@famillecollet.com> 1.1.1-1
- update to 1.1.1

* Fri Dec 31 2010 Remi Collet <rpms@famillecollet.com> 1.0.2-3
- updated tests from Git.

* Sat Oct 23 2010 Remi Collet <rpms@famillecollet.com> 1.0.2-2
- filter provides to avoid igbinary.so
- add missing %%dist

* Wed Sep 29 2010 Remi Collet <rpms@famillecollet.com> 1.0.2-1
- initital RPM

