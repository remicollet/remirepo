%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_mmn:        %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:    %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}


Name:           mod_auth_cas
Version:        1.0.8.1
Release:        5%{?dist}
Summary:        Apache 2.0/2.2 compliant module that supports the CASv1 and CASv2 protocols

Group:          System Environment/Daemons
License:        GPLv3+ with exceptions
URL:            http://www.ja-sig.org/wiki/display/CASC/mod_auth_cas
# The source for this package was pulled from the upstream's vcs. Their 
# releases are stored in SVN instead of exported to a tar.gz, I used the 
# following commands to do so:
#  svn export https://source.jasig.org/cas-clients/mod_auth_cas/tags/mod_auth_cas-1.0.8.1 mod_auth_cas-1.0.8.1

#  tar -czvf mod_auth_cas-1.0.8.1.tar.gz mod_auth_cas-1.0.8.1/
Source0:        mod_auth_cas-1.0.8.1.tar.gz
Source1:        auth_cas.conf

Patch0:         mod_auth_cas-1.0.8.1-fixbuild.patch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  openssl-devel
BuildRequires:  httpd-devel

Requires:       httpd

%description
mod_auth_cas is an Apache 2.0/2.2 compliant module that supports the CASv1
and CASv2 protocols

%prep
%setup -q

%patch0 -p1 -b .fixbuild

%build
%configure --with-apxs=%{_httpd_apxs}
make %{?_smp_mflags}



%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} LIBEXECDIR=%{_httpd_moddir}
%if "%{_httpd_modconfdir}" == "%{_httpd_confdir}"
# httpd <= 2.2.x
install -Dp -m 644 %{SOURCE1} %{buildroot}%{_httpd_modconfdir}/auth_cas.conf
%else
# httpd >= 2.4.x
install -Dp -m 644 %{SOURCE1} %{buildroot}%{_httpd_modconfdir}/10-auth_cas.conf
%endif

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README
%{_libdir}/httpd/modules/*.so
%config(noreplace) %{_httpd_modconfdir}/*.conf

%changelog
* Wed May  2 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.8.1-5
- sync with rawhide, rebuild for remi repo

* Wed May  2 2012 Joe Orton <jorton@redhat.com> - 1.0.8.1-5
- update packaging (#803065)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun 29 2010 Adam Miller <maxamillion@fedoraproject.org> - 1.0.8.1-2
- Fixed svn export link, upstream changed canonical URL names.

* Wed Apr 28 2010 Adam Miller <maxamillion@fedoraproject.org> - 1.0.8.1-1
- added requires of httpd 
- fixed mixed use of macros
- updated to latest version

* Fri Aug 07 2009 Adam Miller <maxamillion@fedoraproject.org> - 1.0.8-1
- First attempt to package mod_auth_cas for Fedora

