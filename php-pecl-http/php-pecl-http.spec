%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}

# The project is pecl_http but the extension is only http
%global proj_name pecl_http
%global pecl_name http
%global prever    dev4
%global devver    dev

Name:           php-pecl-http
Version:        2.0.0
Release:        0.3.%{prever}%{?dist}
Summary:        Extended HTTP support

License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/pecl_http
Source0:        http://pecl.php.net/get/%{proj_name}-%{version}%{?prever}.tgz

# From http://www.php.net/manual/en/http.configuration.php
Source1:        %{proj_name}.ini

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-devel >= 5.4.0
BuildRequires:  php-pear
BuildRequires:  pcre-devel
BuildRequires:  zlib-devel >= 1.2.0.4
BuildRequires:  libevent-devel >= 1.4
BuildRequires:  curl-devel >= 7.18.2
# No yet available on fedora: BuildRequires:  libserf-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Provides:       php-pecl(%{proj_name}) = %{version}%{devver}
Provides:       php-pecl(%{pecl_name}) = %{version}%{devver}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

%{?filter_setup}


%description
The HTTP extension aims to provide a convenient and powerful set of
functionality for major applications.

The HTTP extension eases handling of HTTP URLs, dates, redirects, headers
and messages in a HTTP context (both incoming and outgoing). It also provides
means for client negotiation of preferred language and charset, as well as
a convenient way to exchange arbitrary data with caching and resuming
capabilities.

Also provided is a powerful request and parallel interface.

Version 2 is completely incompatible to previous version.

Documentation : http://php.net/http


%package devel
Summary:       Extended HTTP support developer files (header)
Group:         Development/Libraries
Requires:      php-pecl-http%{?_isa} = %{version}-%{release}
Requires:      php-devel%{?_isa} >= 5.4.0

%description devel
These are the files needed to compile programs using HTTP extension.


%prep
%setup -c -q 

extver=$(sed -n '/#define PHP_HTTP_EXT_VERSION/{s/.* "//;s/".*$//;p}' %{proj_name}-%{version}%{?prever}/php_http.h)
if test "x${extver}" != "x%{version}%{?devver}"; then
   : Error: Upstream HTTP version is now ${extver}, expecting %{version}%{?devver}.
   : Update the pdover macro and rebuild.
   exit 1
fi

cp %{SOURCE1} %{pecl_name}.ini

cp -pr %{proj_name}-%{version}%{?prever} %{proj_name}-zts


%build
cd %{proj_name}-%{version}%{?prever}
%{_bindir}/phpize
%configure  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../%{proj_name}-zts
%{_bindir}/phpize-zts
%configure  --with-php-config=%{_bindir}/php-config-zts
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make -C %{proj_name}-%{version}%{?prever} \
     install INSTALL_ROOT=%{buildroot}

make -C %{proj_name}-zts \
     install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini


%check
# Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension_dir=%{proj_name}-%{version}%{?prever}/modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

# Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension_dir=%{proj_name}-zts/modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{proj_name} >/dev/null || :
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc %{proj_name}-%{version}%{?prever}/{CREDITS,LICENSE,ThanksTo.txt}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%files devel
%defattr(-,root,root,-)
%{php_incldir}/ext/%{pecl_name}
%{php_ztsincldir}/ext/%{pecl_name}


%changelog
* Wed Jan 25 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.3.dev4
- zts binary in /usr/bin with -zts suffix

* Mon Jan 23 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.2.dev4
- update to 2.0.0dev4
- fix missing file https://bugs.php.net/60839

* Sun Jan 22 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.1.dev3
- initial package

