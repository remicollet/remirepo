Name:           php-geshi
Version:        1.0.8.10
Release:        1%{?dist}
Summary:        Generic syntax highlighter

Group:          Development/Libraries
License:        GPLv2+
URL:            http://qbnz.com/highlighter/
Source0:        http://downloads.sourceforge.net/geshi/GeSHi-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       php >= 4.3.0
Requires:       php-mbstring


%description
GeSHi aims to be a simple but powerful highlighting class, with the following
goals:
    * Support for a wide range of popular languages
    * Easy to add a new language for highlighting
    * Highly customisable output formats


%prep
%setup -q -n geshi
find docs -type f -exec chmod a-x {} ';'
find . -type f -name "*.php" -exec chmod a-x {} ';'


%build
# Nothing to build


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/php/
cp -a geshi geshi.php $RPM_BUILD_ROOT%{_datadir}/php/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc docs/* contrib/
%{_datadir}/php/geshi.php
%{_datadir}/php/geshi


%changelog
* Tue Jul 05 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.0.8.10-1
- rebuild for remi repository

* Tue Jun 28 2011 Xavier Bachelot <xavier@bachelot.org> 1.0.8.10-1
- Update to 1.0.8.10.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jun 23 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.0.8.8-1
- rebuild for remi repository

* Tue Jun 15 2010 Xavier Bachelot <xavier@bachelot.org> 1.0.8.8-1
- Update to 1.0.8.8.
- Fix Source0: URL, upstream changed tarball name.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 15 2009 Xavier Bachelot <xavier@bachelot.org> 1.0.8.3-1
- Update to 1.0.8.3.

* Thu Mar 26 2009 Xavier Bachelot <xavier@bachelot.org> 1.0.8.2-3
- License is actually GPLv2+.
- Remove implicit R: php-common.
- Fix URL:.

* Thu Mar 26 2009 Xavier Bachelot <xavier@bachelot.org> 1.0.8.2-2
- More Requires:.

* Thu Mar 19 2009 Xavier Bachelot <xavier@bachelot.org> 1.0.8.2-1
- Initial build.
