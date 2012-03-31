%{!?_httpd_apxs: %{expand: %%global _httpd_apxs %%{_sbindir}/apxs}}
%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir: %{expand: %%global _httpd_moddir %%{_libdir}/httpd/modules}}

Summary: Output filter to rewrite HTML links in a proxy situation
Name: mod_proxy_html
Version: 3.1.2
Release: 10%{?dist}
License: GPLv2
Group: System Environment/Libraries
URL: http://apache.webthing.com/mod_proxy_html/
Source: http://apache.webthing.com/mod_proxy_html/mod_proxy_html-%{version}.tar.bz2
Source1: README.selinux
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: httpd-mmn = %{_httpd_mmn}
BuildRequires: libxml2-devel httpd-devel

%description
mod_proxy_html is an output filter to rewrite HTML links in a proxy situation,
to ensure that links work for users outside the proxy. It serves the same
purpose as Apache's ProxyPassReverse directive does for HTTP headers, and is
an essential component of a reverse proxy.


%prep
%setup -q -n %{name}

cp %{SOURCE1} README.selinux

%build
%{_httpd_apxs} -c -I . -I %{_includedir}/libxml2 -lxml2 mod_proxy_html.c
%{_httpd_apxs} -c -I . -I %{_includedir}/libxml2 -lxml2 mod_xml2enc.c


%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_httpd_moddir} %{buildroot}/%{_docdir}/%{name}-%{version}
%{_httpd_apxs} -i -S LIBEXECDIR=%{buildroot}%{_httpd_moddir} -n mod_proxy_html mod_proxy_html.la
%{_httpd_apxs} -i -S LIBEXECDIR=%{buildroot}%{_httpd_moddir} -n mod_xml2enc mod_xml2enc.la
install -m 644 -D proxy_html.conf %{buildroot}%{_httpd_confdir}/proxy_html.conf
%if "%{_httpd_modconfdir}" == "%{_httpd_confdir}"
# apache < 2.4
%{__sed} -i \
	-e '/^# LoadFile	\/usr\/lib\/libxml2\.so/d' \
	-e '1,/Windows/s@^# \(LoadModule		*proxy_html_module		*modules/mod_proxy_html\.so\)$@\1@' \
	-e '1,/Windows/s@^# \(LoadModule		*xml2enc_module		*modules/mod_xml2enc\.so\)$@\1@' \
%ifarch x86_64
	-e 's@/usr/lib/@%{_libdir}/@' \
%endif
	%{buildroot}%{_httpd_confdir}/proxy_html.conf
%else
# apache > 2.4
%{__sed} -i \
	-e '1,/HTML/d' \
	%{buildroot}%{_httpd_confdir}/proxy_html.conf
cat >modconf <<EOF
LoadModule      proxy_html_module       modules/mod_proxy_html.so
LoadModule      xml2enc_module          modules/mod_xml2enc.so
EOF
install -m 644 -D modconf %{buildroot}%{_httpd_modconfdir}/10-proxy_html.conf

%endif


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root)
%{_httpd_moddir}/mod_proxy_html.so
%{_httpd_moddir}/mod_xml2enc.so
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%config(noreplace) %{_httpd_modconfdir}/10-proxy_html.conf
%endif
%config(noreplace) %{_httpd_confdir}/proxy_html.conf
%doc COPYING README README.selinux


%changelog
* Sat Mar 31 2012 Remi Collet <RPMS@FamilleCollet.com> - 3.1.2-10
- more macros and split conf

* Sat Mar 31 2012 Remi Collet <RPMS@FamilleCollet.com> - 3.1.2-9
- rebuild httpd 2.4, use new macros.

* Sat Jan 28 2012 Philip Prindeville <philipp@fedoraproject.org> - 3.1.2-9
- Add README about settings required for running under selinux.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 16 2009 Philip Prindeville <philipp@fedoraproject.org> 3.1.2-6
- Include mod_xml2enc.  Fix sed script to properly uncomment LoadModule lines.

* Wed Dec 16 2009 Philip Prindeville <philipp@fedoraproject.org> 3.1.2-2
- Initial commit.

* Wed Dec 09 2009 Philip Prindeville <http://www.redfish-solutions.com> 3.1.2-1
- Version bump to 3.1.2

* Fri Sep 18 2008 Philip Prindeville <http://www.redfish-solutions.com> 3.0.1-9
- Put back BuildRequires...

* Tue Sep  7 2008 Philip Prindeville <http://www.redfish-solutions.com> 3.0.1-8
- Not being enabled by default (uncomment the "LoadModule" line from the
  config).

* Tue Sep  2 2008 Philip Prindeville <http://www.redfish-solutions.com> 3.0.1-7
- Fixed "Source:" to point to numbered version of tarball.  Thanks Nick!

* Tue Aug 12 2008 Philip Prindeville <http://www.redfish-solutions.com> 3.0.1-6
- Fixed BuildRequires: and BuildRoot: as per code review comments.

* Sun Jul 13 2008 Philip Prindeville <http://www.redfish-solutions.com> 3.0.1-5
- Fixed gcc warning on missing braces/ambiguous "else".

* Thu Jul 10 2008 Philip Prindeville <http://www.redfish-solutions.com> 3.0.1-4
- Fixed conditional edit of path to libs in .conf file based on architecture
  type.

* Mon Jun 30 2008 Philip Prindeville <http://www.redfish-solutions.com> 3.0.1-3
- Added "--with xml" for those wanting implicit load of libxml2 via ld.so
  instead of via explicit "LoadFile" in configs.

* Sat Jun 28 2008 Philip Prindeville <http://www.redfish-solutions.com> 3.0.1-2
- Merged with comments from reviewers (especially Ray).

* Wed Jun 18 2008 Philip Prindeville <http://www.redfish-solutions.com> 3.0.1-1
- Initial RPM release.

