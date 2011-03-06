%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

%global pecl_name rrd

Summary:      PHP Bindings for rrdtool
Name:         php-pecl-rrd
Version:      0.10.0
Release:      2%{?dist}
License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/rrd

Source:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source2:      xml2changelog

# http://pecl.php.net/bugs/22576 - extension version
# http://pecl.php.net/bugs/22577 - long parameter
# http://pecl.php.net/bugs/22580 - rrdtool version check
Patch0:       rrd-build.patch

# http://pecl.php.net/bugs/22579 - tests are arch dependant
Patch1:       rrd-tests.patch

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel >= 5.3.2
BuildRequires: rrdtool
BuildRequires: rrdtool-devel >= 1.3.0
BuildRequires: php-pear

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Conflicts:    rrdtool-php
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
%{_bindir}/php -n %{SOURCE2} package.xml | tee CHANGELOG | head -n 10

cd %{pecl_name}-%{version}
%patch0 -p1 -b .build
%patch1 -p1 -b .tests

# generate test file according to tests/testData/readme.txt
# http://pecl.php.net/bugs/22578
dir=tests/testData
fic=$dir/speed.rrd
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

# %{_bindir}/rrdtool fetch $fic AVERAGE --start 920804400 --end 920809200 >$dir/rrd_updater_fetch.txt

fic=$dir/moreDS.rrd
%{_bindir}/rrdtool create $fic --start 920804400 \
  DS:speed1:COUNTER:600:U:U \
  DS:speed2:COUNTER:600:U:U \
  RRA:AVERAGE:0.5:1:24 \
  RRA:AVERAGE:0.5:6:10
%{_bindir}/rrdtool update $fic \
 920804700:12345:11340 920805000:12357:11357 920805300:12363:11363 \
 920805600:12363:11364 920805900:12363:11364 920806200:12373:11373 \
 920806500:12383:11373 920806800:12393:11393 920807100:12399:11399 \
 920807400:12405:11405 920807700:12411:11411 920808000:12415:11415 \
 920808300:12420:11420 920808600:12422:11422 920808900:12423:11423

# %{_bindir}/rrdtool fetch moreDS.rrd AVERAGE --start 920804400 --end 920808000 >$dir/moreDS_fetch.txt


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

%{__make} test NO_INTERACTION=1 | tee rpmtests.log

if  grep -q "FAILED TEST" rpmtests.log; then
  for t in tests/*diff; do
     echo "*** FAILED: $(basename $t .diff)"
     diff -u tests/$(basename $t .diff).exp tests/$(basename $t .diff).out || :
  done
  # tests only succeed with rrdtool 1.4.x
%if %{?fedora} >= 14
  exit 1
%endif
fi

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
* Sat Mar 05 2011 Remi Collet <Fedora@FamilleCollet.com> 0.10.0-2
- improved patches

* Fri Mar 04 2011 Remi Collet <Fedora@FamilleCollet.com> 0.10.0-1
- Version 0.10.0 (stable) - API 0.10.0 (beta)
- remove patches, merged upstream
- add links to 5 new upstream bugs

* Mon Jan 03 2011 Remi Collet <Fedora@FamilleCollet.com> 0.9.0-1
- Version 0.9.0 (beta) - API 0.9.0 (beta)
- initial RPM

