# Depending on what version of Fedora we're on, use a different php binary, different apr
# and also different handler.
%if 0%{?fedora}
   %if 0%{fedora} >= 5
      %define php /usr/bin/php-cgi
      %define handler php5-script
      %define apr /usr/bin/apr-1-config
   %endif
   %if 0%{fedora} == 4
      %define php /usr/bin/php-cgi
      %define handler x-httpd-php
      %define apr /usr/bin/apr-config
   %endif
   %if 0%{fedora} <= 3
      %define php /usr/bin/php
      %define handler x-httpd-php
      %define apr /usr/bin/apr-config
   %endif
%else
   %define php /usr/bin/php
      %define handler x-httpd-php
   %define apr /usr/bin/apr-config
%endif

%{!?_httpd_apxs: %{expand: %%global _httpd_apxs %%{_sbindir}/apxs}}
%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)}}

Summary: An apache2 module for executing PHP scripts with the permissions of their owners
Name: mod_suphp
Version: 0.6.3
Release: 9%{?dist}
License: GPLv2+
Group: System Environment/Daemons
Source0: http://www.suphp.org/download/suphp-%{version}.tar.gz
Source1: suphp.conf
Source2: mod_suphp.conf
Source3: README.fedora
Source4: mod_suphp.module.conf
Patch0: mod_suphp-0.6.3-userdir.patch
Patch1: mod_suphp-0.6.1-AddHandler.patch
Patch3: mod_suphp-0.6.1-chroot.patch
URL: http://www.suphp.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: httpd >= 2.0, php
Requires: httpd-mmn = %{_httpd_mmn}
BuildRequires: httpd-devel >= 2.0, apr-devel


%description
suPHP is an apache module for executing PHP scripts with the permissions of
their owners. It consists of an Apache module (mod_suphp) and a setuid root
binary (suphp) that is called by the Apache module to change the uid of the
process executing the PHP interpreter.

Please take a look at %{_docdir}/%{name}-%{version}/README.fedora for 
installation instructions.

%prep
%setup -q -n suphp-%{version}
%patch0 -p 1 -b .userdir
%patch1 -p 1 -b .AddHandler
%patch3 -p 1 -b .chroot


# fill placeholders
sed -e 's|###PHP-BIN###|%{php}|g; s|###HANDLER###|%{handler}|g;' %{SOURCE1} > suphp.conf
sed -e 's|###HANDLER###|%{handler}|g;' %{SOURCE2} > mod_suphp.conf
sed -e 's|###HANDLER###|%{handler}|g;' %{SOURCE3} > README.fedora
cp -a %{SOURCE4} mod_suphp.module.conf


%build
echo "Building mod_suphp with %{php} as PHP interpreter and %{apr} for the apr configuration script."
echo "%{handler} is used as a AddHandler."
%configure \
	--with-apr=%{apr} \
	--with-apxs=%{_httpd_apxs} \
	--with-apache-user=apache \
	--with-min-uid=500 \
	--with-min-gid=500 \
	--with-php=%{php} \
	--with-logfile=/var/log/httpd/suphp_log \
	--with-setid-mode=owner 

pushd src
make %{?_smp_mflags} suphp
popd

pushd src/apache2
%{_httpd_apxs} -c mod_suphp.c
mv .libs/mod_suphp.so .
popd


%install
rm -rf %{buildroot}

%{__install} -c -m 4755 -D src/suphp %{buildroot}%{_sbindir}/suphp
%{__install} -m 755 -D src/apache2/mod_suphp.so %{buildroot}%{_libdir}/httpd/modules/mod_suphp.so

# Install the config files
%{__install} -m 644 -D suphp.conf %{buildroot}%{_sysconfdir}/suphp.conf
%{__install} -m 644 -D mod_suphp.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/mod_suphp.conf
%{__install} -m 644 -D mod_suphp.module.conf %{buildroot}%{_sysconfdir}/httpd/conf.modules.d/02-mod_suphp.conf

# Rename docs
cp doc/CONFIG CONFIG.suphp
cp doc/apache/CONFIG CONFIG.apache


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README COPYING CONFIG.suphp CONFIG.apache README.fedora
%attr (4550, root, apache) %{_sbindir}/suphp
%{_libdir}/httpd/modules/*.so
%config(noreplace) %{_sysconfdir}/suphp.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_suphp.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/02-mod_suphp.conf


%changelog
* Thu Apr 05 2012 Jan Kaluza <jkaluza@redhat.com> - 0.6.3-9
- Fix compilation issues with httpd-2.4 (#809750)

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-8
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Sep 07 2008 Andreas Thienemann <andreas@bawue.net> - 0.6.3-3
- Fix conditionals, fix FTBFS #449578

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.6.3-2
- fix license tag

* Sun Mar 30 2008 Andreas Thienemann <andreas@bawue.net> - 0.6.3-1
- Updated to 0.6.3 fixing two security problems. #439687

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.6.2-2
- Autorebuild for GCC 4.3

* Sat Mar 10 2007 Andreas Thienemann <andreas@bawue.net> - 0.6.2-1
- Updated to 0.6.2
- Reverted our double free patch. Upstream fixed their SmartPointer
  implementation.
- Reverted our apr Patch, upstream is working correctly with Apache 2.2 now

* Fri Nov 10 2006 Andreas Thienemann <andreas@bawue.net> - 0.6.1-4
- Fix double free corruption. For real this time. :-/

* Fri Sep 08 2006 Andreas Thienemann <andreas@bawue.net> - 0.6.1-3
- Finally fixed double free corruption #192415
- Fixed up configuration creation

* Wed May 24 2006 Andreas Thienemann <andreas@bawue.net> - 0.6.1-2
- Corrected handler for mod_suphp.conf
- Minor cleanups and fixes

* Mon Feb 06 2006 Andreas Thienemann <andreas@bawue.net> 0.6.1-1
- Updated to 0.6.1

* Tue Jul 09 2005 Andreas Thienemann <andreas@bawue.net> 0.5.2-8
- Added a dependency on a specific httpd-mmn

* Tue Jul 05 2005 Andreas Thienemann <andreas@bawue.net> 0.5.2-7
- Bumped up the releasever

* Tue Jul 05 2005 Andreas Thienemann <andreas@bawue.net> 0.5.2-6
- Added correct name to %%setup macro

* Thu Jun 30 2005 Andreas Thienemann <andreas@bawue.net> 0.5.2-5
- Rollback of namechange. Now we're mod_suphp again.

* Thu Jun 30 2005 Andreas Thienemann <andreas@bawue.net> 0.5.2-4
- Cleanup of specfile, incorporated suggestions from "spot"
- Modified configure command to use cgi-php for FC4, php otherwise

* Sat Nov 13 2004 Andreas Thienemann <andreas@bawue.net> 0.5.2-3
- Added "--disable-checkpath" in order to allow /~user URLs

* Sat Nov 13 2004 Andreas Thienemann <andreas@bawue.net> 0.5.2-2
- Fixed the wrong path in the logfile directive

* Sat Nov 13 2004 Andreas Thienemann <andreas@bawue.net> 0.5.2-1
- initial package
