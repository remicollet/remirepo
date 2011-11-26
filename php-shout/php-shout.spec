%global php_apiver %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdi %(php-config --extension-dir 2>/dev/null || echo "undefined")

Name:           php-shout
Version:        0.9.2
Release:        8%{?dist}
Summary:        PHP module for communicating with Icecast servers

Group:          Development/Languages
License:        LGPLv2+
URL:            http://phpshout.sourceforge.net/

Source0:        http://downloads.sourceforge.net/phpshout/phpShout-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-devel
# Will hopefully go away once libogg-devel and/or libshout-devel specify this BR:
BuildRequires:  pkgconfig
BuildRequires:  libshout-devel >= 2.1

%if 0%{?php_zend_api:1}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
%else
Requires: php-api = %{php_apiver}
%endif

%{?filter_setup:
%filter_provides_in %{php_extdir}/.*\.so$
%filter_setup
}


%description
The php-shout package is an extension to the PHP Hypertext Preprocessor.
It wraps the libshout library available from http://icecast.org/ and
provides native Shout functions to the PHP runtime engine.  Libshout is
a streaming audio library that connects and sends properly formatted
audio data to an Icecast Streaming Media server (also http://icecast.org/).
Libshout "handles the socket connection, the timing of the data, and
prevents bad data from getting to the icecast server."  With php-shout, a
PHP developer can write PHP scripts that act as a streaming media source,
and focus on other robust features, without worrying about the
details of the server communication.


%prep
%setup -q -n phpShout-%{version}
chmod a-x *.[ch] TODO README INSTALL LICENSE


%build
phpize --clean
phpize
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
install -D -p -m 0755 modules/shout.so %{buildroot}%{php_extdir}/shout.so
install -D -p -m 0644 shout.ini %{buildroot}%{_sysconfdir}/php.d/shout.ini


%check
# simple module load test
php --no-php-ini \
    --define extension_dir=modules \
    --define extension=shout.so \
    --modules | grep shout


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README TODO
%config(noreplace) %{_sysconfdir}/php.d/shout.ini
%{php_extdir}/shout.so


%changelog
* Wed Jul  6 2011  Remi Collet <Fedora@FamilleCollet.com> - 0.9.2-8
- fix php_zend_api usage, fix FTBFS #715846
- add filter_provides to avoid private-shared-object-provides shout.so
- clean tabs from spec

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 07 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.9.2-6
- fix Source URL
- fix requires for PHP abi.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.9.2-4
- rebuild for new PHP 5.3.0 ABI (20090626)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.2-2
- fix license tag

* Fri Jan  5 2007 Brandon Holbrook <fedora at theholbrooks.org> 0.9.2-1
- Bump to 0.9.2

* Sun Oct 29 2006 Brandon Holbrook <fedora at theholbrooks.org> 0.9.1-1
- Bump to 0.9.1

* Thu Oct 26 2006 Brandon Holbrook <fedora at theholbrooks.org> 0.3.1-7
- Rebuild for new PHP

* Fri Aug 11 2006 Brandon Holbrook <fedora at theholbrooks.org> 0.3.1-6
- Mass Rebuild for FC6

* Fri Aug 11 2006 Brandon Holbrook <fedora at theholbrooks.org> 0.3.1-5
- New FE php macros
- Minor syntax / permission changes
- Added BR: pkgconfig for new buildroot
- New php_extdir and php_apiver from FE PHP Packaging Guidelines

* Fri Jun 30 2006 Brandon Holbrook <fedora at theholbrooks.org> 0.3.1-3
- New extdir and apiver to make mock happy

* Wed Jun 28 2006 Brandon Holbrook <fedora at theholbrooks.org> 0.3.1-1
- Upgraded to 0.3.1
- Removed unneded BuildRequires: pkgconfig

* Wed Mar 29 2006 Brandon Holbrook <fedora at theholbrooks.org> 0.3a-5
- Upgraded to 0.3a (tarball has not been phpize'd to save space)
- Minor %%define fixes
- spaces2tabs
- mkdir has been replaced with 'install -D'
- Moved the 'phpize' calls from %%prep to %%build

* Sat Mar 11 2006 Brandon Holbrook <fedora at theholbrooks.org>
- Upgraded to 0.3
- Bumped libshout requirement to 2.1

* Wed Feb 22 2006 Brandon Holbrook <fedora at theholbrooks.org>
- Upgraded to 0.1.5

* Thu Feb 16 2006 Brandon Holbrook <fedora at theholbrooks.org>
- Upgraded to 0.1.4
- Added 'phpize --clean; phpize' to setup phase
- Removed redundant 'Requires:' implied by BuildRequires
- Replaced $RPM_BUILD_ROOT with %%{buildroot}

* Mon Feb 13 2006 Brandon Holbrook <fedora at theholbrooks.org>
- Initial RPM release
