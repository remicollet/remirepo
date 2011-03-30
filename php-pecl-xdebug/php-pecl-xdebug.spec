%{!?phpname:		%{expand: %%global phpname     php}}

%if %{phpname} == php
%global phpbindir      %{_bindir}
%global phpconfdir     %{_sysconfdir}
%global phpincldir     %{_includedir}
%else
%global phpbindir      %{_bindir}/%{phpname}
%global phpconfdir     %{_sysconfdir}/%{phpname}
%global phpincldir     %{_includedir}/%{phpname}
%endif

%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%global php_extdir %(%{phpbindir}/php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)

%global pecl_name xdebug

Name:           %{phpname}-pecl-xdebug
Version:        2.1.1
Release:        1%{?dist}
Summary:        PECL package for debugging PHP scripts

License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/xdebug
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{phpname}-pear  >= 1:1.4.9-1.2
BuildRequires:  %{phpname}-devel >= 5.1.0
BuildRequires:  libedit-devel

%if 0%{?pecl_install:1}
Requires(post): %{__pecl}
%endif
%if 0%{?pecl_uninstall:1}
Requires(postun): %{__pecl}
%endif
Provides:       %{phpname}-pecl(Xdebug) = %{version}
Provides:       %{phpname}-pecl(Xdebug)%{?_isa} = %{version}

%if 0%{?php_zend_api:1}
Requires:       %{phpname}(zend-abi) = %{php_zend_api}
Requires:       %{phpname}(api) = %{php_core_api}
%else
Requires:       php-api = %{php_apiver}
%endif


%if 0%{?fedora}%{?rhel} > 4
%{?filter_setup:
%filter_provides_in %{php_extdir}/.*\.so$
%filter_setup
}
%endif


%description
The Xdebug extension helps you debugging your script by providing a lot
of valuable debug information.


%prep
%setup -qc
cd %{pecl_name}-%{version}
# package.xml is V1, package2.xml is V2
mv ../package2.xml %{pecl_name}.xml

# fix rpmlint warnings
iconv -f iso8859-1 -t utf-8 Changelog > Changelog.conv && mv -f Changelog.conv Changelog
chmod -x *.[ch]

# http://bugs.xdebug.org/view.php?id=674
sed -i -e "/XDEBUG_VERSION/s/2.1.2dev/%{version}/" php_xdebug.h

# Check extension version
ver=$(sed -n '/XDEBUG_VERSION/{s/.* "//;s/".*$//;p}' php_xdebug.h)
if test "$ver" != "%{version}"; then
   : Error: Upstream XDEBUG_VERSION version is ${ver}, expecting %{version}.
   exit 1
fi

%build
cd %{pecl_name}-%{version}
%{phpbindir}/phpize
%configure --enable-xdebug  --with-php-config=%{phpbindir}/php-config
%{__make} %{?_smp_mflags}

# Build debugclient
pushd debugclient
#cp %{_datadir}/automake-1.??/depcomp .
%configure --with-libedit
%{__make} %{?_smp_mflags}
popd


%install
cd %{pecl_name}-%{version}
rm -rf $RPM_BUILD_ROOT docs
make install INSTALL_ROOT=$RPM_BUILD_ROOT

# install debugclient
install -d $RPM_BUILD_ROOT%{phpbindir}
install -pm 755 debugclient/debugclient $RPM_BUILD_ROOT%{phpbindir}

# install config file
install -d $RPM_BUILD_ROOT%{phpconfdir}/php.d
cat > $RPM_BUILD_ROOT%{phpconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable xdebug extension module
zend_extension=%{php_extdir}/%{pecl_name}.so
EOF

# install doc files
install -d ../docs
install -pm 644 Changelog CREDITS LICENSE NEWS README ../docs

# Install XML package description
install -d $RPM_BUILD_ROOT%{pecl_xmldir}
install -pm 644 %{pecl_name}.xml $RPM_BUILD_ROOT%{pecl_xmldir}/%{name}.xml


%check
cd %{pecl_name}-%{version}
# only check if build extension can be loaded
%{phpbindir}/php \
    --no-php-ini \
    --define zend_extension=modules/%{pecl_name}.so \
    --modules | grep Xdebug


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


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc docs/*
%config(noreplace) %{phpconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{phpbindir}/debugclient
%{pecl_xmldir}/%{name}.xml


%changelog
* Wed Mar 30 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.1.1-1
- allow relocation

* Wed Mar 30 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.1.1-1
- update to 2.1.1
- patch reported version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 23 2010 Remi Collet <Fedora@FamilleCollet.com> - 2.1.0-2
- add filter_provides to avoid private-shared-object-provides xdebug.so
- add %%check section (minimal load test)
- always use libedit

* Tue Jun 29 2010 Remi Collet <Fedora@FamilleCollet.com> - 2.1.0-1
- update to 2.1.0

* Mon Sep 14 2009 Christopher Stone <chris.stone@gmail.com> 2.0.5-1
- Upstream sync

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <Fedora@FamilleCollet.com> - 2.0.4-1
- update to 2.0.4 (bugfix + Basic PHP 5.3 support)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 09 2008 Christopher Stone <chris.stone@gmail.com> 2.0.3-4
- Add code coverage patch (bz #460348)
- http://bugs.xdebug.org/bug_view_page.php?bug_id=0000344

* Thu Oct 09 2008 Christopher Stone <chris.stone@gmail.com> 2.0.3-3
- Revert last change

* Thu Oct 09 2008 Christopher Stone <chris.stone@gmail.com> 2.0.3-2
- Add php-xml to Requires (bz #464758)

* Thu May 22 2008 Christopher Stone <chris.stone@gmail.com> 2.0.3-1
- Upstream sync
- Clean up libedit usage
- Minor rpmlint fix

* Sun Mar 02 2008 Christopher Stone <chris.stone@gmail.com> 2.0.2-4
- Add %%{__pecl} to post/postun Requires

* Fri Feb 22 2008 Christopher Stone <chris.stone@gmail.com> 2.0.2-3
- %%define %%pecl_name to properly register package
- Install xml package description
- Add debugclient
- Many thanks to Edward Rudd (eddie@omegaware.com) (bz #432681)

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.2-2
- Autorebuild for GCC 4.3

* Sun Nov 25 2007 Christopher Stone <chris.stone@gmail.com> 2.0.2-1
- Upstream sync

* Sun Sep 30 2007 Christopher Stone <chris.stone@gmail.com> 2.0.0-2
- Update to latest standards
- Fix encoding on Changelog

* Sat Sep 08 2007 Christopher Stone <chris.stone@gmail.com> 2.0.0-1
- Upstream sync
- Remove %%{?beta} tags

* Sun Mar 11 2007 Christopher Stone <chris.stone@gmail.com> 2.0.0-0.5.RC2
- Create directory to untar sources
- Use new ABI check for FC6
- Remove %%{release} from Provides

* Mon Jan 29 2007 Christopher Stone <chris.stone@gmail.com> 2.0.0-0.4.RC2
- Compile with $RPM_OPT_FLAGS
- Use $RPM_BUILD_ROOT instead of %%{buildroot}
- Fix license tag

* Mon Jan 15 2007 Christopher Stone <chris.stone@gmail.com> 2.0.0-0.3.RC2
- Upstream sync

* Sun Oct 29 2006 Christopher Stone <chris.stone@gmail.com> 2.0.0-0.2.RC1
- Upstream sync

* Wed Sep 06 2006 Christopher Stone <chris.stone@gmail.com> 2.0.0-0.1.beta6
- Remove Provides php-xdebug
- Fix Release
- Remove prior changelog due to Release number change
