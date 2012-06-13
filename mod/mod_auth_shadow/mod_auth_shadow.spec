%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)}}
Name:		mod_auth_shadow
Version:	2.3
Release:	1%{?dist}
Source:		http://downloads.sourceforge.net/mod-auth-shadow/%{name}-%{version}.tar.gz
Source1:	mod_auth_shadow.conf
URL:		http://mod-auth-shadow.sourceforge.net
License:	GPLv2+
Group:		System Environment/Daemons
Summary:	An Apache module for authentication using /etc/shadow
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	httpd-devel
Requires:	httpd-mmn = %{_httpd_mmn}
%description

When performing this task one encounters one fundamental
difficulty: The /etc/shadow file is supposed to be
read/writable only by root.  However, the web server is
supposed to run under a non-root user, such as "nobody".

mod_auth_shadow addresses this difficulty by opening a pipe
to an suid root program, validate, which does the actual
validation.  When there is a failure, validate writes an
error message to the system log, and waits three seconds
before exiting.

%prep
%setup -q -n %{name}_%{version}

sed -i 's#/usr/local#/usr#' makefile
sed -i 's/chown/#chown/' makefile
sed -i 's/chmod/#chmod/' makefile

%build
gcc -o validate validate.c -lcrypt
%{_httpd_apxs} -D INSTBINDIR=\\\"%{_sbindir}\\\" -c mod_auth_shadow.c

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/httpd/modules
mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
install validate $RPM_BUILD_ROOT/%{_sbindir}
install .libs/mod_auth_shadow.so $RPM_BUILD_ROOT/%{_httpd_moddir}
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/conf.d/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(4755,root,root) %{_sbindir}/validate
%{_httpd_moddir}/*
%attr(0644,root,root) %config(noreplace) /etc/httpd/conf.d/%{name}.conf
%doc CHANGES README COPYING

%changelog
* Tue Apr 10 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.3-1
- rebuild for remi repo and httpd 2.4

* Mon Apr 09 2012 Jan Klepek <jan.klepek at gmail.com> - 2.3-1
- updated to latest version

* Sat Mar 17 2012 Jan Klepek <jan.klepek at gmail.com> - 2.2-11
- updated requires

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Apr 09 2010 Jaroslav Reznik <jreznik@redhat.com> - 2.2-8
- CVE-2010-1151: bad wait(2) call causes randomized authorization (#578168)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.2-5
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.2-4
- Autorebuild for GCC 4.3

* Tue Apr 03 2007 David Anderson <fedora-packaging@dw-perspective.org.uk> 2.2-3
- Removed chmod/chown from makefile (sometimes caused root builds to fail)

* Mon Apr 02 2007 David Anderson <fedora-packaging@dw-perspective.org.uk> 2.2-1
- Upstream new release (includes license file)

* Sat Mar 24 2007 David Anderson <fedora-packaging@dw-perspective.org.uk> 2.1-3
- First packaging for Fedora Extras (modified from upstream spec file)
