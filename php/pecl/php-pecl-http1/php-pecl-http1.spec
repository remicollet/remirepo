# spec file for php-pecl-http1
#
# Copyright (c) 2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%scl_package php-pecl-http1
%else
%global pkg_name %{name}
%endif
%{!?php_inidir:  %{expand: %%global php_inidir  %{_sysconfdir}/php.d}}
%{!?php_incldir: %{expand: %%global php_incldir %{_includedir}/php}}
%{!?__php:       %{expand: %%global __php       %{_bindir}/php}}
%{!?__pecl:      %{expand: %%global __pecl      %{_bindir}/pecl}}

# The project is pecl_http but the extension is only http
%global proj_name pecl_http
%global pecl_name http
%global with_zts  0%{?__ztsphp:1}

# php-pecl-http exists and is version 2
Name:           %{?scl_prefix}php-pecl-http1
Version:        1.7.6
Release:        2%{?dist}
Summary:        Extended HTTP support

License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/pecl_http
Source0:        http://pecl.php.net/get/%{proj_name}-%{version}.tgz

# Change for package
Patch0:         %{pecl_name}-ini.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  %{?scl_prefix}php-hash
BuildRequires:  %{?scl_prefix}php-iconv
BuildRequires:  %{?scl_prefix}php-session
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  pcre-devel
BuildRequires:  zlib-devel
BuildRequires:  libevent-devel
BuildRequires:  curl-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       %{?scl_prefix}php-hash%{?_isa}
Requires:       %{?scl_prefix}php-iconv%{?_isa}
Requires:       %{?scl_prefix}php-session%{?_isa}
# From upstream documentation
Conflicts:      %{?scl_prefix}php-pecl-event
# Can install both version of the same extension
Conflicts:      %{?scl_prefix}php-pecl-http

Provides:       %{?scl_prefix}php-pecl(%{proj_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{proj_name})%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}


# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
The HTTP extension aims to provide a convenient and powerful set of
functionality for major applications.

The HTTP extension eases handling of HTTP URLs, dates, redirects, headers
and messages in a HTTP context (both incoming and outgoing). It also provides
means for client negotiation of preferred language and charset, as well as
a convenient way to exchange arbitrary data with caching and resuming
capabilities.

It provides powerful request functionality, if built with CURL
support. Parallel requests are available for PHP 5 and greater.

Note:
. %{?scl_prefix}php-pecl-http1 provides API version 1
. %{?scl_prefix}php-pecl-http  provides API version 2


%package devel
Summary:       Extended HTTP support developer files (header)
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      %{?scl_prefix}php-devel%{?_isa}
# Can install both version of the same extension
Conflicts:     %{?scl_prefix}php-pecl-http-devel

%description devel
These are the files needed to compile programs using HTTP extension.


%prep
%setup -c -q 

cd %{proj_name}-%{version}
%patch0 -p1 -b .rpmconf

extver=$(sed -n '/#define PHP_HTTP_VERSION/{s/.* "//;s/".*$//;p}' php_http.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream HTTP version is now ${extver}, expecting %{version}.
   : Update the pdover macro and rebuild.
   exit 1
fi
cd ..

%if %{with_zts}
cp -pr %{proj_name}-%{version} %{proj_name}-zts
%endif


%build
cd %{proj_name}-%{version}
%{_bindir}/phpize
%configure  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../%{proj_name}-zts
%{_bindir}/zts-phpize
%configure  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C %{proj_name}-%{version} \
     install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file (z-http.ini to be loaded after hash/iconv/session)
install -Dpm644 %{proj_name}-%{version}/docs/%{pecl_name}.ini \
        %{buildroot}%{php_inidir}/z-%{pecl_name}.ini

%if %{with_zts}
make -C %{proj_name}-zts \
     install INSTALL_ROOT=%{buildroot}

install -Dpm644 %{proj_name}-zts/docs/%{pecl_name}.ini \
        %{buildroot}%{php_ztsinidir}/z-%{pecl_name}.ini
%endif


%check
# Add needed extensions
modules=""
for mod in hash iconv session; do
  if [ -f %{php_extdir}/${mod}.so ]; then
    modules="$modules --define extension=${mod}.so"
  fi
done

# Minimal load test for NTS extension
%{__php} --no-php-ini \
    $modules \
    --define extension=$PWD/%{proj_name}-%{version}/modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
# Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    $modules \
    --define extension=$PWD/%{proj_name}-zts/modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


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
%doc %{proj_name}-%{version}/{CREDITS,LICENSE,ThanksTo.txt}
%doc %{proj_name}-%{version}/docs
%config(noreplace) %{php_inidir}/z-%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml
%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/z-%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif

%files devel
%defattr(-,root,root,-)
%{php_incldir}/ext/%{pecl_name}
%if %{with_zts}
%{php_ztsincldir}/ext/%{pecl_name}
%endif


%changelog
* Thu Aug  1 2013 Remi Collet <remi@fedoraproject.org> - 1.7.6-2
- cleanups, adapt for SCL, make ZTS optional

* Thu Jun 20 2013 Remi Collet <remi@fedoraproject.org> - 1.7.6-1
- Update to 1.7.6

* Thu Mar 21 2013 Remi Collet <remi@fedoraproject.org> - 1.7.5-1
- initial package
