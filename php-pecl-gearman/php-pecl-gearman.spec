%{!?__pecl:	%{expand: %%global __pecl	%{_bindir}/pecl}}
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

%define pecl_name gearman

Name:		php-pecl-gearman
Version:	0.7.0
Release:	5%{?dist}
Summary:	PHP wrapper to libgearman

Group:		Development/Tools
License:	PHP
URL:		http://gearman.org
Source0:	http://pecl.php.net/get/gearman-0.7.0.tgz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	php-devel, libgearman-devel > 0.8, gearmand >= 0.12, re2c
BuildRequires:	php-pear
# Required by phpize
BuildRequires: autoconf, automake, libtool

Requires:	php(zend-abi) = %{php_zend_api}
Requires:	php(api) = %{php_core_api}
Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Requires:	php-common, gearmand >= 0.12, libgearman > 0.8

%description

This extension uses libgearman library to provide API for
communicating with gearmand, and writing clients and workers

%prep
%setup -q -n gearman-%{version}

%build
phpize
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_ROOT=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/php.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/gearman.ini << 'EOF'
; enable gearman extension
extension="gearman.so"
EOF
# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pecl_xmldir}
install -m 644 ../package.xml $RPM_BUILD_ROOT%{pecl_xmldir}/%{name}.xml


%clean
rm -rf $RPM_BUILD_ROOT

%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif

%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif

%{_sysconfdir}/php.d/gearman.ini
%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/php.d/gearman.ini
%{php_extdir}/gearman.so
%{pecl_xmldir}/%{name}.xml

%doc ChangeLog README CREDITS EXPERIMENTAL LICENSE


%changelog
* Fri Aug 12 2011 Jesse Keating <jkeating@redhat.com> - 0.7.0-5
- Rebuild for broken deps

* Mon Apr 11 2011 Paul Whalen <paul.whalen@senecac.on.ca> 0.7.0-4
- fix setup and package.xml install

* Mon Apr 11 2011 Paul Whalen <paul.whalen@senecac.on.ca> 0.7.0-3
- correct macros, add license to files

* Fri Apr 08 2011 Paul Whalen <paul.whalen@senecac.on.ca> 0.7.0-2
- correct package following pecl packaging guidelines

* Fri Mar 11 2011 Paul Whalen <paul.whalen@senecac.on.ca> 0.7.0-1
- Initial Packaging

