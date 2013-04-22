%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}

# The project is pecl_http but the extension is only http
%global proj_name pecl_http
%global pecl_name http

Name:           php-pecl-http1
Version:        1.7.5
Release:        1%{?dist}.1
Summary:        Extended HTTP support

License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/pecl_http
Source0:        http://pecl.php.net/get/%{proj_name}-%{version}.tgz

# Change for package
Patch0:         %{pecl_name}-ini.patch
# http://svn.php.net/viewvc?view=revision&revision=329705
Patch1:         %{pecl_name}-php55.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-devel
BuildRequires:  php-hash
BuildRequires:  php-iconv
BuildRequires:  php-session
BuildRequires:  php-spl
BuildRequires:  php-pear
BuildRequires:  pcre-devel
BuildRequires:  zlib-devel
BuildRequires:  libevent-devel
BuildRequires:  curl-devel
# No yet available on fedora: BuildRequires:  libserf-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires:       php-hash
Requires:       php-iconv
Requires:       php-json
Requires:       php-spl
Conflicts:      php-pecl-event
Conflicts:      php-pecl-http

Provides:       php-pecl(%{proj_name})         = %{version}
Provides:       php-pecl(%{proj_name})%{?_isa} = %{version}
Provides:       php-pecl(%{pecl_name})         = %{version}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:       php-%{pecl_name}               = %{version}
Provides:       php-%{pecl_name}%{?_isa}       = %{version}

# Other third party repo stuff
Obsoletes:      php53-pecl-http1
Obsoletes:      php53u-pecl-http1
%if "%{php_version}" > "5.4"
Obsoletes:      php54-pecl-http1
%endif
%if "%{php_version}" > "5.5"
Obsoletes:      php55-pecl-http1
%endif

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
. php-pecl-http1 provides API version 1
. php-pecl-http  provides API version 2


%package devel
Summary:       Extended HTTP support developer files (header)
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      php-devel%{?_isa}
Conflicts:     php-pecl-http-devel

%description devel
These are the files needed to compile programs using HTTP extension.


%prep
%setup -c -q 

cd %{proj_name}-%{version}
%patch0 -p1 -b .rpmconf
%if "%{php_version}" > "5.5"
%patch1 -p3 -b .php55
%endif

extver=$(sed -n '/#define PHP_HTTP_VERSION/{s/.* "//;s/".*$//;p}' php_http.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream HTTP version is now ${extver}, expecting %{version}.
   : Update the pdover macro and rebuild.
   exit 1
fi
cd ..

cp -pr %{proj_name}-%{version} %{proj_name}-zts


%build
cd %{proj_name}-%{version}
%{_bindir}/phpize
%configure  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../%{proj_name}-zts
%{_bindir}/zts-phpize
%configure  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make -C %{proj_name}-%{version} \
     install INSTALL_ROOT=%{buildroot}

make -C %{proj_name}-zts \
     install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

cd %{proj_name}-%{version}
# install config file (z-http.ini to be loaded after json)
install -Dpm644 docs/%{pecl_name}.ini %{buildroot}%{php_inidir}/z-%{pecl_name}.ini
install -Dpm644 docs/%{pecl_name}.ini %{buildroot}%{php_ztsinidir}/z-%{pecl_name}.ini


%check
# Install needed extensions
modules=""
for mod in json hash iconv; do
  if [ -f %{php_extdir}/${mod}.so ]; then
    ln -sf %{php_extdir}/${mod}.so    %{proj_name}-%{version}/modules
    ln -sf %{php_ztsextdir}/${mod}.so %{proj_name}-zts/modules
    modules="$modules --define extension=${mod}.so"
  fi
done

# Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension_dir=%{proj_name}-%{version}/modules \
    $modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

# Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension_dir=%{proj_name}-zts/modules \
    $modules \
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
%doc %{proj_name}-%{version}/{CREDITS,LICENSE,ThanksTo.txt}
%doc %{proj_name}-%{version}/docs
%config(noreplace) %{php_inidir}/z-%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/z-%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%files devel
%defattr(-,root,root,-)
%{php_incldir}/ext/%{pecl_name}
%{php_ztsincldir}/ext/%{pecl_name}


%changelog
* Thu Mar 21 2013 Remi Collet <remi@fedoraproject.org> - 1.7.5-1
- initial package
