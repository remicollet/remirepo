Summary: Output filter to rewrite HTML links in a proxy situation
Name: mod_proxy_html
Version: 3.1.2
Release: 9%{?dist}
License: GPLv2
Group: System Environment/Libraries
URL: http://apache.webthing.com/mod_proxy_html/
Source: http://apache.webthing.com/mod_proxy_html/mod_proxy_html-%{version}.tar.bz2
Source1: README.selinux
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing)
BuildRequires: libxml2-devel httpd-devel

%description
mod_proxy_html is an output filter to rewrite HTML links in a proxy situation,
to ensure that links work for users outside the proxy. It serves the same
purpose as Apache's ProxyPassReverse directive does for HTTP headers, and is
an essential component of a reverse proxy.

%define modulesdir %{_libdir}/httpd/modules
%define confdir %{_sysconfdir}/httpd/conf

%prep
%setup -q -n %{name}


%build
%{_sbindir}/apxs -c -I . -I %{_includedir}/libxml2 -lxml2 mod_proxy_html.c
%{_sbindir}/apxs -c -I . -I %{_includedir}/libxml2 -lxml2 mod_xml2enc.c


%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}/%{modulesdir} %{buildroot}/%{_docdir}/%{name}-%{version}
%{_sbindir}/apxs -i -S LIBEXECDIR=%{buildroot}/%{modulesdir} -n mod_proxy_html mod_proxy_html.la
%{_sbindir}/apxs -i -S LIBEXECDIR=%{buildroot}/%{modulesdir} -n mod_xml2enc mod_xml2enc.la
install -m 644 -D proxy_html.conf %{buildroot}/%{confdir}.d/proxy_html.conf
%{__sed} -i \
	-e '/^# LoadFile	\/usr\/lib\/libxml2\.so/d' \
	-e '1,/Windows/s@^# \(LoadModule		*proxy_html_module		*modules/mod_proxy_html\.so\)$@\1@' \
	-e '1,/Windows/s@^# \(LoadModule		*xml2enc_module		*modules/mod_xml2enc\.so\)$@\1@' \
%ifarch x86_64
	-e 's@/usr/lib/@%{_libdir}/@' \
%endif
	%{buildroot}/%{confdir}.d/proxy_html.conf

install -m 444 -D %{SOURCE1} %{buildroot}/%{_docdir}/%{name}-%{version}/


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root)
%{modulesdir}/mod_proxy_html.so
%{modulesdir}/mod_xml2enc.so
%config(noreplace) %lang(en) %{confdir}.d/proxy_html.conf
%doc COPYING README
%doc %{_docdir}/%{name}-%{version}/README.selinux


%changelog
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

