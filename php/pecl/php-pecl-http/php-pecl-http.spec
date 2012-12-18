%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}

# The project is pecl_http but the extension is only http
%global proj_name pecl_http
%global pecl_name http
%global prever    beta3

Name:           php-pecl-http
Version:        2.0.0
Release:        0.13.%{prever}%{?dist}.2
Summary:        Extended HTTP support

License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/pecl_http
Source0:        http://pecl.php.net/get/%{proj_name}-%{version}%{?prever}.tgz

# From http://www.php.net/manual/en/http.configuration.php
Source1:        %{proj_name}.ini

# Fix for curl version older than 7.21.3
# http://svn.php.net/viewvc?view=revision&revision=328773
Patch0:         %{pecl_name}-curl.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-devel >= 5.3.0
BuildRequires:  php-hash
BuildRequires:  php-iconv
BuildRequires:  php-json
BuildRequires:  php-spl
BuildRequires:  php-pear
BuildRequires:  pcre-devel
BuildRequires:  zlib-devel >= 1.2.0.4
BuildRequires:  libevent-devel >= 1.4
BuildRequires:  curl-devel >= 7.18.2
# No yet available on fedora: BuildRequires:  libserf-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires:       php-hash
Requires:       php-iconv
Requires:       php-json
Requires:       php-spl
Conflicts:      php-event

Provides:       php-pecl(%{proj_name})         = %{version}%{?prever}
Provides:       php-pecl(%{proj_name})%{?_isa} = %{version}%{?prever}
Provides:       php-pecl(%{pecl_name})         = %{version}%{?prever}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}%{?prever}
Provides:       php-%{pecl_name}               = %{version}%{?prever}
Provides:       php-%{pecl_name}%{?_isa}       = %{version}%{?prever}

# Other third party repo stuff
Obsoletes:     php53-pecl-http
Obsoletes:     php53u-pecl-http
%if "%{php_version}" > "5.4"
Obsoletes:     php54-pecl-http
%endif
%if "%{php_version}" > "5.5"
Obsoletes:     php55-pecl-http
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

Also provided is a powerful request and parallel interface.

Version 2 is completely incompatible to previous version.

Documentation : http://php.net/http


%package devel
Summary:       Extended HTTP support developer files (header)
Group:         Development/Libraries
Requires:      php-pecl-http%{?_isa} = %{version}-%{release}
Requires:      php-devel%{?_isa} >= 5.3.0

%description devel
These are the files needed to compile programs using HTTP extension.


%prep
%setup -c -q 

cd %{proj_name}-%{version}%{?prever}
%patch0 -p1 -b .oldcurl

extver=$(sed -n '/#define PHP_HTTP_EXT_VERSION/{s/.* "//;s/".*$//;p}' php_http.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream HTTP version is now ${extver}, expecting %{version}%{?prever}.
   : Update the pdover macro and rebuild.
   exit 1
fi
cd ..

cp %{SOURCE1} %{pecl_name}.ini

cp -pr %{proj_name}-%{version}%{?prever} %{proj_name}-zts


%build
cd %{proj_name}-%{version}%{?prever}
%{_bindir}/phpize
%configure  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../%{proj_name}-zts
%{_bindir}/zts-phpize
%configure  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make -C %{proj_name}-%{version}%{?prever} \
     install INSTALL_ROOT=%{buildroot}

make -C %{proj_name}-zts \
     install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file (z-http.ini to be loaded after json)
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_inidir}/z-%{pecl_name}.ini
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/z-%{pecl_name}.ini


%check
# Install needed extensions
modules=""
for mod in json hash iconv; do
  if [ -f %{php_extdir}/${mod}.so ]; then
    ln -sf %{php_extdir}/${mod}.so    %{proj_name}-%{version}%{?prever}/modules
    ln -sf %{php_ztsextdir}/${mod}.so %{proj_name}-zts/modules
    modules="$modules --define extension=${mod}.so"
  fi
done

# Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension_dir=%{proj_name}-%{version}%{?prever}/modules \
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
%doc %{proj_name}-%{version}%{?prever}/{CREDITS,LICENSE,ThanksTo.txt}
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
* Thu Dec 13 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.13.beta3
- update to 2.0.0beta3

* Thu Nov 29 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.12.beta2
- update to 2.0.0beta2
- also provides php-http
- remove old directives from configuration file

* Fri Oct 12 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.11.beta1
- update to 2.0.0beta1
- must be load after json, to rename config to z-http.ini

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-0.10.alpha1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 21 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.9.alpha1
- update to 2.0.0alpha1

* Sat Mar 31 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.8.dev10
- update to 2.0.0dev10

* Fri Mar 16 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.7.dev8
- update to 2.0.0dev8

* Fri Mar 09 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.6.dev7
- update to 2.0.0dev7

* Fri Mar 02 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.5.dev6
- update to 2.0.0dev6

* Sat Feb 18 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.4.dev5
- update to 2.0.0dev5
- fix filters

* Wed Jan 25 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.3.dev4
- zts binary in /usr/bin with zts prefix

* Mon Jan 23 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.2.dev4
- update to 2.0.0dev4
- fix missing file https://bugs.php.net/60839

* Sun Jan 22 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.1.dev3
- initial package

