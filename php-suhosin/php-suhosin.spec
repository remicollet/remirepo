%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)

Name:           php-suhosin
Version:        0.9.32.1
Release:        1%{?dist}
Summary:        Suhosin is an advanced protection system for PHP installations

Group:          Development/Languages
License:        PHP
URL:            http://www.hardened-php.net/suhosin/
Source0:        http://download.suhosin.org/suhosin-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  php-devel
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_apiver}

%description
Suhosin is an advanced protection system for PHP installations. It was designed 
to protect servers and users from known and unknown flaws in PHP applications 
and the PHP core.  


%prep
%setup -q -n suhosin-%{version}


%build
%{_bindir}/phpize
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_ROOT=$RPM_BUILD_ROOT


# install configuration
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/php.d
%{__cp} suhosin.ini $RPM_BUILD_ROOT%{_sysconfdir}/php.d/suhosin.ini


%check
NO_INTERACTION=1 make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changelog 
%doc CREDITS
%config(noreplace) %{_sysconfdir}/php.d/suhosin.ini
%{php_extdir}/suhosin.so


%changelog
* Tue Jul 27 2010 Remi Collet <rpms@famillecollet.com> 0.9.32.1-1
- update to 0.9.32.1

* Tue Mar  2 2010 Remi Collet <rpms@famillecollet.com> 0.9.29-3.el5.remi
- rebuild to have remi's EVR > epel's EVR

* Sat Oct 31 2009 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> - 0.9.29-1
Update to version 0.9.29
- Fixing crash bugs with PHP 5.3.0 caused by unexpected NULL in 
  EG(active_symbol_table)
- Added more compatible way to retrieve ext/session globals
- Increased default length and count limit for POST variables 
  (for people not reading docu)
- Fixed crash bug with PHP 5.2.10 caused by a change in extension 
  load order of ext/session
- Fixed harmless parameter order error in a bogus memset()
- Disable suhosin.session.cryptua by default because of 
  Internet Explorer 8 "features"
- Added suhosin.executor.include.allow_writable_files which can be 
  disabled to disallow inclusion of files writable by the webserver

* Thu Sep 18 2008 Remi Collet <rpms@famillecollet.com> 0.9.27-1.fc9.remi.1
- rebuild for php 5.3.0-dev

* Thu Sep 18 2008 Remi Collet <rpms@famillecollet.com> 0.9.27-1.###.remi
- rebuild for php 5.2.6 all FC/EL version

* Tue Aug 26 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.27-1
- Update to version 0.9.27

* Thu Aug 7 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.25-1
- Update to version 0.9.25

* Wed Jun 18 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.24-1
- Update to version 0.9.24

* Tue Apr 29 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.23-1
- Update to version 0.9.23
- Some specfile updates for review

* Fri Jan 4 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.22-2
- Use short name for license

* Wed Dec 5 2007 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.22-1
- Initial packaging of 0.9.22
