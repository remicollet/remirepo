%{!?__pecl:  %{expand: %%global __pecl %{_bindir}/pecl}}

%global pecl_name   imagick
%global prever      b2

# We don't really rely on upstream ABI
%global imbuildver %(pkg-config --silence-errors --modversion ImageMagick 2>/dev/null || echo 65536)

Summary:       Extension to create and modify images using ImageMagick
Name:          php-pecl-imagick
Version:       3.2.0
Release:       0.1.%{prever}%{?dist}%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/imagick
Source:        http://pecl.php.net/get/%{pecl_name}-%{version}%{?prever}.tgz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php-devel >= 5.1.3, php-pear
%if 0%{?fedora} >= 20
BuildRequires: ImageMagick-devel >= 6.7.5
Requires:      ImageMagick-libs%{?_isa}  >= %{imbuildver}
%else
BuildRequires: ImageMagick-last-devel >= 6.7.5
Requires:      ImageMagick-last-libs%{?_isa}  >= %{imbuildver}
%endif
Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}

Provides:      php-%{pecl_name} = %{version}%{?prever}
Provides:      php-%{pecl_name}%{?_isa} = %{version}%{?prever}
Provides:      php-pecl(%{pecl_name}) = %{version}%{?prever}
Provides:      php-pecl(%{pecl_name})%{?_isa} = %{version}%{?prever}
Conflicts:     php-pecl-gmagick

# Other third party repo stuff
Obsoletes:     php53-pecl-imagick
Obsoletes:     php53u-pecl-imagick
Obsoletes:     php54-pecl-imagick
%if "%{php_version}" > "5.5"
Obsoletes:     php55-pecl-imagick
%endif

# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
Imagick is a native php extension to create and modify images
using the ImageMagick API.


%prep
echo TARGET is %{name}-%{version}-%{release}
%setup -q -c 

mv %{pecl_name}-%{version}%{?prever} NTS

# don't install any font (and test using it)
# don't install empty file (d41d8cd98f00b204e9800998ecf8427e)
# fix tests role
# https://github.com/mkoppanen/imagick/commit/64ef2a7991c2cdc22b9b2275e732439dc21cede8
sed -e '/anonymous_pro_minus.ttf/d' \
    -e '/015-imagickdrawsetresolution.phpt/d' \
    -e '/OFL.txt/d' \
    -e '/INSTALL/d' \
    -e '/d41d8cd98f00b204e9800998ecf8427e/d' \
    -e '/name="tests/s/role="doc"/role="test"/' \
    -i package.xml

if grep '\.ttf' package.xml
then : "Font files detected!"
     exit 1
fi

cd NTS
extver=$(sed -n '/#define PHP_IMAGICK_VERSION/{s/.* "//;s/".*$//;p}' php_imagick.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi
cd ..

cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension = %{pecl_name}.so

; Documentation: http://php.net/imagick

; Fixes a drawing bug with locales that use ',' as float separators.
;imagick.locale_fix=0

; Used to enable the image progress monitor.
;imagick.progress_monitor=0
EOF

cp -r NTS ZTS


%build
cd ZTS
: ZTS build
%{_bindir}/zts-phpize
%configure --with-imagick=%{prefix} --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}

: Standard NTS build
cd ../NTS
%{_bindir}/phpize
%configure --with-imagick=%{prefix} --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot} -C NTS
make install INSTALL_ROOT=%{buildroot} -C ZTS

# Drop in the bit of configuration
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

# Install XML package description
mkdir -p %{buildroot}%{pecl_xmldir}
install -pm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Test & Documentation
for i in $(grep 'role="test"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
: simple module load test for NTS extension
cd NTS
%{__php} --no-php-ini \
    --define extension_dir=%{buildroot}%{php_extdir} \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

: upstream test suite for NTS extension
export TEST_PHP_EXECUTABLE=%{__php}
export REPORT_EXIT_STATUS=1
export NO_INTERACTION=1
if ! %{__php} run-tests.php \
    -n -q \
    -d extension_dir=%{buildroot}%{php_extdir} \
    -d extension=%{pecl_name}.so
then
  for i in tests/*diff
  do
    echo "---- FAILURE in $i"
    cat $i
    echo -n "\n----"
  done
  exit 1
fi

: simple module load test for ZTS extension
cd ../ZTS
%{__ztsphp} --no-php-ini \
    --define extension_dir=%{buildroot}%{php_ztsextdir} \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

: upstream test suite for ZTS extension
export TEST_PHP_EXECUTABLE=%{__ztsphp}
%{__ztsphp} run-tests.php \
    -n -q \
    -d extension_dir=%{buildroot}%{php_ztsextdir} \
    -d extension=%{pecl_name}.so


%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc %{pecl_docdir}/%{pecl_name}
%doc %{pecl_testdir}/%{pecl_name}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml
# should be in devel
%{php_incldir}/ext/%{pecl_name}
%{php_ztsincldir}/ext/%{pecl_name}


%changelog
* Sun Oct 20 2013 Remi Collet <remi@fedoraproject.org> - 3.2.0-0.1.b2
- Update to 3.2.0b2
- install doc in pecl doc_dir
- install tests in pecl test_dir

* Wed Sep 25 2013 Remi Collet <remi@fedoraproject.org> - 3.1.2-1
- Update to 3.1.2
- add LICENSE to doc

* Sun Sep 22 2013 Remi Collet <remi@fedoraproject.org> - 3.1.1-1
- Update to 3.1.1
- open some upstream bugs
  https://bugs.php.net/65734 - Please Provides LICENSE file
  https://bugs.php.net/65736 - Link to sources
  https://bugs.php.net/65736 - Broken ZTS build

* Sun Sep  8 2013 Remi Collet <rpms@famillecollet.com> - 3.1.0-1
- update to 3.1.0 (beta)

* Sun Jun  2 2013 Remi Collet <rpms@famillecollet.com> - 3.1.0-0.10.RC2
- rebuild against new ImageMagick-last version 6.8.5-9

* Sat Apr  6 2013 Remi Collet <rpms@famillecollet.com> - 3.1.0-0.9.RC2
- rebuild against new ImageMagick-last version 6.8.4-6
- improve dependency on ImageMagick library

* Wed Mar 13 2013 Remi Collet <rpms@famillecollet.com> - 3.1.0-0.8.RC2
- rebuild against new ImageMagick-last version 6.8.3.9

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> - 3.1.0-0.5.RC2
- also provides php-imagick

* Sat Sep  8 2012 Remi Collet <remi@fedoraproject.org> - 3.1.0-0.4.RC2
- Obsoletes php53*, php54* on EL

* Thu Aug 16 2012 Remi Collet <rpms@famillecollet.com> - 3.1.0-0.3.RC2
- rebuild against new ImageMagick-last version 6.7.8.10

* Sat Jun 02 2012 Remi Collet <Fedora@FamilleCollet.com> - 3.1.0-0.2.RC2
- update to 3.1.0RC1

* Fri Nov 18 2011 Remi Collet <Fedora@FamilleCollet.com> - 3.1.0-0.1.RC1
- update to 3.1.0RC1 for php 5.4

* Mon Oct 03 2011 Remi Collet <Fedora@FamilleCollet.com> - 3.0.1-3.1
- spec cleanup

* Wed Aug 24 2011 Remi Collet <Fedora@FamilleCollet.com> - 3.0.1-3
- build zts extension

* Mon Dec 27 2010 Remi Collet <rpms@famillecollet.com> 3.0.1-2
- relocate using phpname macro

* Fri Nov 26 2010 Remi Collet <rpms@famillecollet.com> 3.0.1-1.1
- rebuild against latest ImageMagick 6.6.5.10

* Thu Nov 25 2010 Remi Collet <rpms@famillecollet.com> 3.0.1-1
- update to 3.0.1

* Mon Jul 26 2010 Remi Collet <rpms@famillecollet.com> 3.0.0-1
- update to 3.0.0

* Wed Aug 26 2009 Remi Collet <rpms@famillecollet.com> 2.3.0-2
- build against ImageMagick2 6.5.x

* Mon Aug 24 2009 Remi Collet <rpms@famillecollet.com> 2.3.0-1
- update to 2.3.0

* Tue Jun 30 2009 Remi Collet <rpms@famillecollet.com> 2.2.2-3.###.remi
- rebuild for PHP 5.3.0 (API = 20090626)

* Sat Apr 25 2009 Remi Collet <rpms@famillecollet.com> 2.2.2-2.fc11.remi
- F11 rebuild for PHP 5.3.0RC1

* Wed Feb 25 2009 Remi Collet <rpms@famillecollet.com> 2.2.2-1.fc10.remi
- update to 2.2.2 for php 5.3.0beta1

* Thu Jan 29 2009 Remi Collet <rpms@famillecollet.com> 2.2.1-1.fc10.remi.2
- rebuild for php 5.3.0beta1

* Sat Dec 13 2008 Remi Collet <rpms@famillecollet.com> 2.2.1-1.fc#.remi.1
- rebuild with php 5.3.0-dev
- add imagick-2.2.1-php53.patch

* Sat Dec 13 2008 Remi Collet <rpms@famillecollet.com> 2.2.1-1
- update to 2.2.1

* Sat Jul 19 2008 Remi Collet <rpms@famillecollet.com> 2.2.0-1.fc9.remi.1
- rebuild with php 5.3.0-dev

* Sat Jul 19 2008 Remi Collet <rpms@famillecollet.com> 2.2.0-1
- update to 2.2.0

* Thu Apr 24 2008 Remi Collet <rpms@famillecollet.com> 2.1.1-1
- Initial package

