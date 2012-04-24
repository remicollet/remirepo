%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_mmn:        %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:     %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}

Name:           mod_annodex
Version:        0.2.2
Release:        16%{?dist}
Summary:        Apache module for server-side support of annodex media

Group:          System Environment/Daemons
License:        ASL 1.1
URL:		http://www.annodex.net/
Source:		http://www.annodex.net/software/mod_annodex/download/%{name}-ap20-%{version}.tar.gz
Source1:	annodex.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	libannodex-devel
BuildRequires:	libcmml-devel >= 0.8
BuildRequires:	httpd-devel >= 2.0.40
BuildRequires:  pkgconfig
BuildRequires:	sed

Requires:	httpd-mmn = %{_httpd_mmn}

%description
mod_annodex provides full support for Annodex.net media. For more details
about annodex format, see http://www.annodex.net/

mod_annodex is a handler for type application/x-annodex. It provides the
following features:

        * dynamic generation of Annodex media from CMML files.

        * handling of timed query offsets, such as

          http://media.example.com/fish.anx?t=npt:01:20.8
        or
          http://media.example.com/fish.anx?id=Preparation

        * dynamic retrieval of CMML summaries, if the Accept: header
          prefers type text/x-cmml over application/x-annodex.

%prep
%setup -q -n %{name}-ap20-%{version}

%build
%{_httpd_apxs} -c mod_annodex.c `pkg-config annodex cmml --cflags --libs`
mv .libs/%{name}.so .

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_httpd_moddir}
install -m755 %{name}.so $RPM_BUILD_ROOT%{_httpd_moddir}

# install config file
mkdir -p $RPM_BUILD_ROOT%{_httpd_confdir} \
         $RPM_BUILD_ROOT%{_httpd_modconfdir}

%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
# httpd >= 2.4.x
sed -n /^LoadModule/p %{SOURCE1} > 10-annodex.conf
sed /^LoadModule/d %{SOURCE1} > annodex.conf
touch -r %{SOURCE1} 10-annodex.conf annodex.conf
install -Dp -m 0644 annodex.conf $RPM_BUILD_ROOT%{_httpd_confdir}/annodex.conf
install -Dp -m 0644 10-annodex.conf $RPM_BUILD_ROOT%{_httpd_modconfdir}/10-annodex.conf
%else
# httpd <= 2.2.x
install -Dp -m 644 annodex.conf \
   $RPM_BUILD_ROOT%{_httpd_confdir}/annodex.conf
%endif

%clean
rm -rf $RPM_BUILD_ROOT
                                                                                
%files
%defattr(-,root,root)
%doc LICENSE README
%{_httpd_moddir}/mod_annodex.so
%config(noreplace) %{_httpd_confdir}/*.conf
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%config(noreplace) %{_httpd_modconfdir}/*.conf
%endif

%changelog
* Mon Apr 23 2012 Joe Orton <jorton@redhat.com> - 0.2.2-16
- add _httpd_moddir fallback

* Mon Apr 23 2012 Joe Orton <jorton@redhat.com> - 0.2.2-15
- update packaging (#803064)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 02 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 0.2.2-13
- Bump again for liboggz lib (because of libannodex-devel
  (which also depends upon liboggz)

* Wed Jun 02 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 0.2.2-12
- Bump for new liboggz lib

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.2.2-9
- fix license tag

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.2-8
- Autorebuild for GCC 4.3

* Tue Oct 16 2007 Joe Orton <jorton@redhat.com> 0.2.2-7
- rebuild against expat 2.x

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.2.2-6
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.2.2-5
- rebuilt

* Thu Jun 15 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.2.2-4
- remove strip, so -debuginfo is useful, thanks to Ville

* Sun Mar 05 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.2.2-3
- rebuild

* Mon Jun 13 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.2.2-2: rpmlint fixes

* Sat Jun 04 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.2.2-1: initial package
