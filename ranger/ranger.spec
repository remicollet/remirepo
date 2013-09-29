Name:           ranger
Version:        1.6.1
Release:        1%{?dist}
Summary:        A flexible console file manager

Group:          Development/Languages
License:        GPLv3+
URL:            http://savannah.nongnu.org/projects/ranger/
Source0:        http://git.savannah.gnu.org/cgit/%{name}.git/snapshot/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel

%description
Ranger is a free console file manager that gives you greater flexibility and a
good overview of your files without having to leave your *nix console. It
visualizes the directory tree in two dimensions: the directory hierarchy on
one, lists of files on the other, with a preview to the right so you know where
you'll be going.


%prep
%setup -q


%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
mv %{buildroot}%{_docdir}/%{name} rpmdocs


%files
%defattr(-,root,root,-)
%doc rpmdocs/*
%{_bindir}/ranger
%{_bindir}/rifle
%{python_sitelib}/*
%{_mandir}/man1/ranger.1.gz
%{_mandir}/man1/rifle.1.gz


%changelog
* Sun Sep 29 2013 Remi Collet <remi@fedoraproject.org> - 1.6.1-1
- Update to 1.6.1
- add rifle command

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Nov 04 2012 Ben Boeckel <mathstuf@gmail.com> - 1.4.2-1
- Update to 1.4.2

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 19 2010 Ben Boeckel <mathstuf@gmail.com> - 1.2.2-1
- Update to 1.2.2

* Sat Jul 24 2010 Ben Boeckel <mathstuf@gmail.com> - 1.1.2-2
- Add patch to remove shebang line
- BR python2-devel

* Fri Jul 23 2010 Ben Boeckel <mathstuf@gmail.com> - 1.1.2-1
- Initial package
