%{!?__pecl: %{expand: %%global __pecl %{_bindir}/pecl}}

%global pecl_name bbcode
%global pre       b1

Summary:      BBCode parsing Extension
Name:         php-pecl-bbcode
Version:      1.0.3
Release:      0.1.%{pre}%{?dist}
# pecl extension is PHP, bbcode2 is BSD, bstrlib (from bstring) is BSD
License:      PHP and BSD
Group:        Development/Languages
URL:          http://pecl.php.net/package/bbcode

Source:       http://pecl.php.net/get/%{pecl_name}-%{version}%{?pre}.tgz

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel >= 5.2.0
BuildRequires: php-pear

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Provides:     php-pecl(%{pecl_name}) = %{version}%{?pre}
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}


# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$


%description
This is a quick and efficient BBCode Parsing Library.
It provides various tag types, high speed tree based parsing,
callback system, tag position restriction, Smiley Handling,
Subparsing

It will force closing BBCode tags in the good order, and closing
terminating tags at the end of the string this is in order to ensure
HTML Validity in all case.


%prep 
%setup -c -q

FIC=%{pecl_name}-%{version}%{?pre}/php_bbcode.h
sed -i -e '/PHP_BBCODE_VERSION/s/1.1.0-dev/1.0.3b1/' $FIC

extver=$(sed -n '/#define PHP_BBCODE_VERSION/{s/.* "//;s/".*$//;p}' $FIC)
if test "x${extver}" != "x%{version}%{?pre}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?pre}.
   exit 1
fi

cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF


%build
cd %{pecl_name}-%{version}%{?pre}
phpize
%configure

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make  -C %{pecl_name}-%{version}%{?pre} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -Dpm 644 %{pecl_name}.ini %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini

# Install XML package description
mkdir -p %{buildroot}%{pecl_xmldir}
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%check
cd %{pecl_name}-%{version}%{?pre}
php --no-php-ini \
    --define extension_dir=modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

make test NO_INTERACTION=1 | tee rpmtests.log
grep -q "FAILED TEST" rpmtests.log && exit 1


%clean
rm -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%defattr(-, root, root, -)
%doc %{pecl_name}-%{version}%{?pre}/{CREDITS,LICENSE}
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Wed Oct 05 2011 Remi Collet <remi@fedoraproject.org> 1.0.3-0.1.b1
- initial RPM

