Name:           repoview
Version:        0.6.5
Release:        2%{?dist}
Summary:        Creates a set of static HTML pages in a yum repository

Group:          Applications/System
License:        GPLv2+
URL:            http://fedorahosted.org/repoview/
Source0:        http://icon.fedorapeople.org/repoview/%{name}-%{version}.tar.gz
Source1:        fedora-repoview-templates.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       python-kid >= 0.6.3, yum >= 3.0, python >= 2.5

%description
RepoView creates a set of static HTML pages in a yum repository for easy
browsing.


%prep
%setup -q
##
# Fix version and default templates dir.
#
sed -i -e \
    "s|^VERSION =.*|VERSION = '%{version}-%{release}'|g" repoview.py
sed -i -e \
    "s|^DEFAULT_TEMPLATEDIR =.*|DEFAULT_TEMPLATEDIR = '%{_datadir}/%{name}/templates'|g" \
    repoview.py


%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p -m 755                         \
    $RPM_BUILD_ROOT/%{_datadir}/%{name} \
    $RPM_BUILD_ROOT/%{_bindir}          \
    $RPM_BUILD_ROOT/%{_mandir}/man8
install -p -m 755 repoview.py  $RPM_BUILD_ROOT/%{_bindir}/repoview
install -p -m 644 repoview.8   $RPM_BUILD_ROOT/%{_mandir}/man8/
cp -rp templates               $RPM_BUILD_ROOT/%{_datadir}/%{name}/
tar xzf %{SOURCE1}
cp -rp fedora-repoview $RPM_BUILD_ROOT/%{_datadir}/%{name}/fedora


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README COPYING ChangeLog
%{_datadir}/%{name}
%{_bindir}/*
%{_mandir}/man*/*


%changelog
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 19 2010 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.6.5-1
- Update to 0.6.5 (bugfixes)

* Wed Jan 27 2010 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.6.4-1
- Update to 0.6.4 (bugfixes)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 27 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.6.3-1
- Upstream 0.6.3
- Upstream fix for mixed-case packages and md5 warnings (obsoletes patch)
- Minor fixes to functionality

* Thu Mar 26 2009 Seth Vidal <skvidal at fedoraproject.org>
- don't lowercase pkgnames
- stop md5 warning emit

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 02 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.6.2-1
- Upstream 0.6.2
- Modify URLs to point to the new repoview home

* Thu Oct 25 2007 Seth Vidal <skvidal at fedoraproject.org> - 0.6.1-2
- add fedora repoview templates

* Thu Sep 27 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.6.1-1
- Upstream 0.6.1
- Adjust license to GPLv2+

* Thu Jul 19 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.6.0-1
- Upstream 0.6.0
- Drop obsolete patch

* Tue Jul 04 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.5.2-1
- Version 0.5.2
- Use yum-2.9 API patch (Jesse Keating)

* Wed Feb 15 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.5.1-1
- Version 0.5.1

* Fri Jan 13 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.5-1
- Version 0.5

* Sun Oct 09 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.4.1-1
- Version 0.4.1

* Fri Sep 23 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.4-1
- Version 0.4
- Require yum >= 2.3
- Drop requirement for python-elementtree, since it's required by yum
- Disttagging.

* Mon Apr 04 2005 Konstantin Ryabitsev <icon@linux.duke.edu> 0.3-3
- Do not BuildRequire sed -- basic enough dependency, even for version 4.

* Tue Mar 29 2005 Konstantin Ryabitsev <icon@linux.duke.edu> 0.3-2
- Preserve timestamps on installed files
- Do not use macros in source tags
- Omit Epoch

* Fri Mar 25 2005 Konstantin Ryabitsev <icon@linux.duke.edu> 0.3-1
- Version 0.3

* Thu Mar 10 2005 Konstantin Ryabitsev <icon@linux.duke.edu> 0.2-1
- Version 0.2
- Fix URL
- Comply with fedora extras specfile format.
- Depend on python-elementtree and python-kid -- the names in extras.

* Thu Mar 03 2005 Konstantin Ryabitsev <icon@linux.duke.edu> 0.1-1
- Initial build
