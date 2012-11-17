%{!?_httpd_apxs: %{expand: %%global _httpd_apxs %%{_sbindir}/apxs}}
%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:     %{expand: %%global _httpd_moddir     %%{_libdir}/httpd/modules}}

%global gitver	48bb878

Summary:	FLV progressive download streaming for the Apache HTTP Server
Name:		mod_flvx
Version:	0
Release:	0.5.20100525git%{?dist}
Group:		System Environment/Daemons
License:	ASL 2.0
URL:		http://tperspective.blogspot.com/2009/02/apache-flv-streaming-done-right.html
# https://github.com/osantana/mod_flvx/tarball/48bb8781945dfa2e94b2814e9bae5e7d0cc8f29d
Source0:	osantana-%{name}-%{gitver}.tar.gz
Source1:	flvx.conf
BuildRequires:	httpd-devel >= 2.0.39
Requires:	httpd-mmn = %{_httpd_mmn}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
FLV streaming means it can be sought to any position during video, and
browser (Flash player) will buffer only from this position to the end.
Thus streaming allows to skip boring parts or see video ending without
loading the whole file, which simply saves bandwidth. Even H264 is more
efficient, FLV is still a common container format for videos, because
H264 is supported by Flash since version 9.115.

For using FLV streaming on the web, a pseudo-streaming compliant Flash
player, such as Flowplayer, is needed. Streaming requires that the FLV
has embedded key-frame markers (meta-data), that can be injected by any
supported tool, e.g. flvtool2.

%prep
%setup -q -n osantana-%{name}-%{gitver}

%build
%{_httpd_apxs} -Wc,-Wall -c %{name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -D -p -m 755 .libs/%{name}.so $RPM_BUILD_ROOT%{_httpd_moddir}/%{name}.so

%if "%{_httpd_modconfdir}" == "%{_httpd_confdir}"
# httpd <= 2.2.x
install -D -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_confdir}/flvx.conf
%else
# httpd >= 2.4.x
head -n 5 %{SOURCE1} > 10-flvx.conf
sed -e '4,5d' %{SOURCE1} > flvx.conf
touch -c -r %{SOURCE1} 10-flvx.conf flvx.conf
install -D -p -m 644 10-flvx.conf $RPM_BUILD_ROOT%{_httpd_modconfdir}/10-flvx.conf
install -D -p -m 644 flvx.conf $RPM_BUILD_ROOT%{_httpd_confdir}/flvx.conf
%endif

# Fix incorrect end-of-line encoding
sed -e 's/\r//' README.md > README
touch -c -r README.md README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README
%{_httpd_moddir}/%{name}.so
%config(noreplace) %{_httpd_confdir}/flvx.conf
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%config(noreplace) %{_httpd_modconfdir}/10-flvx.conf
%endif

%changelog
* Sat Nov 17 2012 Remi Collet <RPMS@FamilleCollet.com> - 0-0.5.20100525git
- rebuild for remi repo and httpd 2.4

* Sat Nov 17 2012 Robert Scheck <robert@fedoraproject.org> 0-0.5.20100525git
- Updated spec file to match with Apache 2.4 policy (#808560)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.4.20100525git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jul  7 2012 Remi Collet <RPMS@FamilleCollet.com> - 0-0.3.20100525git
- rebuild for remi repo and httpd 2.4

* Thu Jul  5 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0-0.3.20100525git
- Bump build so rawhide is higher than F-17

* Sat Mar 31 2012 Remi Collet <RPMS@FamilleCollet.com> - 0-0.1.20100525git
- rebuild for remi repo and httpd 2.4

* Fri Mar 30 2012 Joe Orton <jorton@redhat.com> - 0-0.1.20100525git
- fix build with httpd 2.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.2.20100525git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 15 2011 Robert Scheck <robert@fedoraproject.org> 0-0.1.20100525git
- Upgrade to GIT 20100525
- Initial spec file for Fedora and Red Hat Enterprise Linux
