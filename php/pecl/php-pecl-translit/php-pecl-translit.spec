# remirepo spec file for php-pecl-translit
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%if "%{scl}" == "rh-php56"
%global sub_prefix more-php56-
%else
%global sub_prefix %{scl_prefix}
%endif
%scl_package       php-pecl-translit
%endif

%global pecl_name   translit
%global with_zts    0%{!?_without_zts:%{?__ztsphp:1}}
# see https://github.com/derickr/pecl-translit/releases
%global gh_commit   09efe930d4e73ca6f82e1195c2c0092f0dce96e5
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    derickr
%global gh_project  pecl-translit
%global with_tests  0%{!?_without_tests:1}
%if "%{php_version}" < "5.6"
# After json
%global ini_name    %{pecl_name}.ini
%else
# After 20-iconv
%global ini_name    40-%{pecl_name}.ini
%endif

Summary:      Transliterates non-latin character sets to latin
Name:         %{?sub_prefix}php-pecl-%{pecl_name}
Version:      0.6.2
Release:      4%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:      BSD
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{pecl_name}

# Pull sources from github to get tests
Source0:      https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?prever}-%{gh_short}.tar.gz

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{?scl_prefix}php-devel
BuildRequires: %{?scl_prefix}php-pear
%if %{with_tests}
BuildRequires: %{?scl_prefix}php-iconv
%endif

Requires:     %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:     %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:     %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:     %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:     %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:     %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:     %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:     %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
%endif

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php53u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php54-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php54w-pecl-%{pecl_name} <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php55w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.0"
Obsoletes:     php70u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.1"
Obsoletes:     php71u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php71w-pecl-%{pecl_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared provides
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This extension allows you to transliterate text in non-latin characters
(such as Chinese, Cyrillic, Greek etc) to latin characters.  Besides the
transliteration the extension also contains filters to upper- and lowercase
latin, cyrillic and greek, and perform special forms of transliteration such
as converting ligatures such as the Norwegian 'æ' to 'ae' and normalizing
punctuation and spacing.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -c -q

mv %{gh_project}-%{gh_commit} NTS
mv NTS/package.xml .

%{?_licensedir:sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml}

cd NTS

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_TRANSLIT_VERSION/{s/.* "//;s/".*$//;p}' php_translit.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi
cd ..

%if %{with_zts}
cp -pr NTS ZTS
%endif

# Create configuration file
cat << 'EOF' | tee %{ini_name}
; Enable '%{summary}' extension module
extension=%{pecl_name}.so
EOF


%build
cd NTS
%{_bindir}/phpize
%configure  \
  --enable-translit \
  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure  \
  --enable-translit \
  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%clean
rm -rf %{buildroot}


%if 0%{?fedora} < 24
# when pear installed alone, after us
%triggerin -- %{?scl_prefix}php-pear
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

# posttrans as pear can be installed after us
%posttrans
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

%postun
if [ $1 -eq 0 -a -x %{__pecl} ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%check
[ -f %{php_extdir}/iconv.so ] && DEPMOD="-d extension=iconv.so"

: Minimal load test for NTS extension
%{__php} -n \
    $DEPMOD \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    -m | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} -n \
    $DEPMOD \
    -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    -m | grep %{pecl_name}
%endif

%if %{with_tests}

: Upstream test suite NTS extension
cd NTS
TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n $DEPMOD -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php --show-diff

%if %{with_zts}
: Upstream test suite NTS extension
cd ../ZTS
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n $DEPMOD -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php --show-diff
%endif
%endif



%files
%defattr(-, root, root, -)
%{!?_licensedir:%doc %{pecl_docdir}/%{pecl_name}}
%{?_licensedir:%license NTS/LICENSE}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 0.6.2-4
- rebuild for PHP 7.1 new API version

* Thu Jun  9 2016 Remi Collet <remi@fedoraproject.org> - 0.6.2-3
- fix license installation on EL-6

* Sun Mar  6 2016 Remi Collet <remi@fedoraproject.org> - 0.6.2-2
- adapt for F24

* Sat Nov 28 2015 Remi Collet <remi@fedoraproject.org> - 0.6.2-1
- Initial package, version 0.6.2 (beta)

