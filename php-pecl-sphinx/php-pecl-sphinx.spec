%global php_apiver	%((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?__pecl:		%{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?php_extdir:		%{expand: %%global php_extdir %(php-config --extension-dir)}}

%define pecl_name sphinx

Name:		php-pecl-sphinx
Version:	1.0.0
Release:	2%{?dist}
Summary:	PECL extension for Sphinx SQL full-text search engine
Group:		Development/Languages
License:	PHP
URL:		http://pecl.php.net/package/%{pecl_name}
Source0:	http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	libsphinxclient-devel php-pear
BuildRequires:	php-devel >= 5.1.3
Requires(post):	%{__pecl}
Requires(postun):	%{__pecl}
Provides:	php-pecl(%{pecl_name}) = %{version}

%if %{?php_zend_api}0
Requires:	php(zend-abi) = %{php_zend_api}
Requires:	php(api) = %{php_core_api}
%else
Requires:	php-api = %{php_apiver}
%endif


%description
This extension provides PHP bindings for libsphinxclient, 
client library for Sphinx the SQL full-text search engine.

%prep
%setup -q -c
[ -f package2.xml ] || %{__mv} package.xml package2.xml
%{__mv} package2.xml %{pecl_name}-%{version}/%{pecl_name}.xml


%build
cd %{pecl_name}-%{version}
phpize
%configure
%{__make} %{?_smp_mflags}

%check
# simple module load test
cd %{pecl_name}-%{version}
php --no-php-ini \
    --define extension_dir=modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}


%install
cd %{pecl_name}-%{version}
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot} INSTALL="install -p"

%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

%{__mkdir_p} %{buildroot}%{pecl_xmldir}
%{__install} -p -m 644 %{pecl_name}.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%clean
%{__rm} -rf %{buildroot}

%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif


%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 ]; then
%{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}/CREDITS
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Sat Sep 12 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.0.0-2
- rebuild for remi repository and PHP 5.3

* Sun Sep 06 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.0.0-2
- Add checks
- Add php-devel version requirement

* Mon Aug 05 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.0.0-1
- Initial package
