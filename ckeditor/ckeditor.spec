Name:		ckeditor
Version:	4.3.2
Release:	1%{?dist}
Summary:	WYSIWYG text editor to be used inside web pages

Group:		Applications/Internet
License:	GPLv2+ or LGPLv2+ or MPLv1.1+
URL:		http://ckeditor.com/
Source0:	http://download.cksource.com/CKEditor/CKEditor/CKEditor%20%{version}/ckeditor_%{version}_standard.tar.gz
Source1:	%{name}.conf

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

Requires:	httpd


%description
CKEditor is a text editor to be used inside web pages. It's a WYSIWYG editor,
which means that the text being edited on it looks as similar as possible to
the results users have when publishing it. It brings to the web common editing
features found on desktop editing applications like Microsoft Word and
OpenOffice.


%package samples
Summary:        Sample files for %{name}
Group:          Documentation

%description samples
%{summary}.


%prep
%setup -q -c

# documentation
mv %{name}/*.md .
mv %{name}/samples .

# Delete bundled flash files
rm -r samples/plugins/htmlwriter/{assets,outputforflash.html}

# fix library path in provided samples
find samples -name \*.html |
  xargs sed -i -e 's:src="\(../\)*ckeditor.js":src="/ckeditor/ckeditor.js":'


%build
# Nothing to build


%install
rm -rf %{buildroot}

# Javascript
mkdir -p %{buildroot}%{_datadir}
cp -rp %{name} %{buildroot}%{_datadir}/

# Hack for compatibility with 3.6 (used by horde)
ln -s ckeditor.js %{buildroot}%{_datadir}/ckeditor/ckeditor_basic.js

# Apache
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc *.md
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_datadir}/%{name}

%files samples
%defattr(-,root,root,-)
%doc LICENSE.md samples/*


%changelog
* Thu Jan 23 2014 Remi Collet <remi@fedoraproject.org> - 4.3.2-1
- Update to 4.3.2

* Thu Aug 15 2013 Orion Poplawski <orion@cora.nwra.com> 4.2-1
- Update to 4.2

* Thu Aug 15 2013 Orion Poplawski <orion@cora.nwra.com> 4.1-3
- Remove bundled flash code
- Move samples to sub-package

* Sun Apr  7 2013 Remi Collet <remi@fedoraproject.org> - 4.1-1
- Update to 4.1
- provided ckeditor_basic.js for compatibility with 3.6
- don't provide default alias, #910590

* Tue Mar 19 2013 Orion Poplawski <orion@cora.nwra.com> 4.0.2-1
- Update to 4.0.2

* Sat Jan 13 2013 Remi Collet <RPMS@FamilleCollet.com> - 3.6.6-1
- backport for remi repo
- update to 3.6.6
- move _samples in doc
- don't package _source
- move php library to /usr/share/php

* Fri Sep 14 2012 Orion Poplawski <orion@cora.nwra.com> 3.6.4-1
- Update to 3.6.4

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 27 2012 Orion Poplawski <orion@cora.nwra.com> 3.6.3-1
- Update to 3.6.3

* Mon Jan 23 2012 Orion Poplawski <orion@cora.nwra.com> 3.6.2-2
- Make %%doc line explicit

* Tue Oct 25 2011 Orion Poplawski <orion@cora.nwra.com> 3.6.2-1
- Update to 3.6.2

* Wed Aug 3 2011 Orion Poplawski <orion@cora.nwra.com> 3.6.1-1
- Update to 3.6.1

* Wed Oct 6 2010 Orion Poplawski <orion@cora.nwra.com> 3.4.1-1
- Initial package
