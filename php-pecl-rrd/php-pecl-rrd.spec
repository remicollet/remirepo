%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

%global pecl_name rrd

Summary:      PHP Bindings for rrdtool
Name:         php-pecl-rrd
Version:      0.9.0
Release:      1%{?dist}
License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/rrd

Source:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source2:      xml2changelog
# svn co http://svn.php.net/repository/pecl/rrd
# tar cvzf rrd-tests.tgz --exclude .svn -C rrd/trunk tests
# See http://pecl.php.net/bugs/21133
Source3:      rrd-tests.tgz

# http://pecl.php.net/bugs/21132
Patch0:       rrd-libdir.patch
# http://pecl.php.net/bugs/21135
Patch1:       rrd-build.patch
Patch2:       rrd-v14x.patch

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel, rrdtool, rrdtool-devel, php-pear

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Obsoletes:    rrdtool-php < 1.4.5
Provides:     rrdtool-php = 1:%{version}-%{release}
Provides:     php-pecl(%{pecl_name}) = %{version}
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}


%{?filter_setup:
%filter_provides_in %{php_extdir}/.*\.so$
%filter_setup
}


%description
Procedural and simple OO wrapper for rrdtool - data logging and graphing
system for time series data.


%prep 
%setup -c -q
%{_bindir}/php -n %{SOURCE2} package.xml >CHANGELOG

cd %{pecl_name}-%{version}
%patch0 -p1 -b .libdir
%patch1 -p1 -b .build
%patch2 -p1 -b .v14x

# Test suite from SVN
%{__tar} xzf %{SOURCE3}

# generate test file according to tests/testData/readme.txt
fic=tests/testData/speed.rrd
%{_bindir}/rrdtool create $fic --start 920804400 \
  DS:speed:COUNTER:600:U:U \
  RRA:AVERAGE:0.5:1:24 \
  RRA:AVERAGE:0.5:6:10
%{_bindir}/rrdtool update $fic 920804700:12345 920805000:12357 920805300:12363
%{_bindir}/rrdtool update $fic 920805600:12363 920805900:12363 920806200:12373
%{_bindir}/rrdtool update $fic 920806500:12383 920806800:12393 920807100:12399
%{_bindir}/rrdtool update $fic 920807400:12405 920807700:12411 920808000:12415
%{_bindir}/rrdtool update $fic 920808300:12420 920808600:12422 920808900:12423
%{_bindir}/rrdtool graph tests/testData/speed.png \
  --start 920804400 --end 920808000 \
  --vertical-label m/s \
  DEF:myspeed=${fic}:speed:AVERAGE \
  CDEF:realspeed=myspeed,1000,* \
  LINE2:realspeed#FF0000


%build
cd %{pecl_name}-%{version}
phpize
%configure

%{__make} %{?_smp_mflags}


%install
cd %{pecl_name}-%{version}
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

# Install XML package description
# use 'name' rather than 'pecl_name' to avoid conflict with pear extensions
%{__mkdir_p} %{buildroot}%{pecl_xmldir}
%{__install} -m 644 ../package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%check
cd %{pecl_name}-%{version}
php --no-php-ini \
    --define extension_dir=modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

%{__make} test NO_INTERACTION=1


%clean
%{__rm} -rf %{buildroot}


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


%files
%defattr(-, root, root, -)
%doc CHANGELOG %{pecl_name}-%{version}/CREDITS
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Mon Jan 03 2011 Remi Collet <Fedora@FamilleCollet.com> 0.9.0-1
- initial RPM

