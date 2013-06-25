%global extname ioncube_loader
%global debug_package %{nil}

Name:          php-ioncube-loader
Summary:       Loader for ionCube Encoded Files
Version:       4.4.1
Release:       1%{?dist}
License:       Distribuable
Group:         Development/Languages

URL:           http://www.ioncube.com
Source0:       http://downloads2.ioncube.com/loader_downloads/%{extname}s_lin_x86.tar.bz2
Source1:       http://downloads2.ioncube.com/loader_downloads/%{extname}s_lin_x86-64.tar.bz2

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php-devel

# ABI check
Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}

# Other third party repo stuff
Obsoletes:     php53-ioncube-loader
Obsoletes:     php53u-ioncube-loader
Obsoletes:     php54-ioncube-loader
%if "%{php_version}" > "5.5"
Obsoletes:     php55-ioncube-loader
%endif

# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
Loader for ionCube Encoded Files.


%prep
%setup -q -T -c

%ifarch x86_64
tar xvf %{SOURCE1}
%else
tar xvf %{SOURCE0}
%endif

# Drop in the bit of configuration
cat > %{extname}.nts << 'EOF'
; Enable %{extname} extension module
zend_extension = %{php_extdir}/%{extname}.so
EOF

cat > %{extname}.zts << 'EOF'
; Enable %{extname} extension module
zend_extension = %{php_ztsextdir}/%{extname}.so
EOF


%build
# tarball provides binaries


%install
rm -rf %{buildroot}
ver=$(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')

if [ ! -f ioncube/%{extname}_lin_${ver}.so ]; then
  : Module for %{php_version} not provied
  exit 1
fi

install -D -pm 755 ioncube/%{extname}_lin_${ver}.so    %{buildroot}%{php_extdir}/%{extname}.so
install -D -m 644  %{extname}.nts                      %{buildroot}%{php_inidir}/%{extname}.ini

install -D -pm 755 ioncube/%{extname}_lin_${ver}_ts.so %{buildroot}%{php_ztsextdir}/%{extname}.so
install -D -m 644  %{extname}.zts                      %{buildroot}%{php_ztsinidir}/%{extname}.ini


%check
# simple module load test
%{__php} --no-php-ini \
    --define zend_extension=%{buildroot}%{php_extdir}/%{extname}.so \
    --modules | grep ionCube

%{__ztsphp} --no-php-ini \
    --define zend_extension=%{buildroot}%{php_ztsextdir}/%{extname}.so \
    --modules | grep ionCube


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc ioncube/*txt

%config(noreplace) %{php_inidir}/%{extname}.ini
%{php_extdir}/%{extname}.so

%config(noreplace) %{php_ztsinidir}/%{extname}.ini
%{php_ztsextdir}/%{extname}.so


%changelog
* Mon Jun 24 2013 Remi Collet <RPMS@famillecollet.com> - 4.4.1-1
- update to 4.4.1

* Mon Sep  3 2012 Remi Collet <RPMS@famillecollet.com> - 4.2.2-1
- initial package

