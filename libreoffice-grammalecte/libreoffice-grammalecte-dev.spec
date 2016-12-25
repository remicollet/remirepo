# remirepo spec file for libreoffice-grammalecte
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global   extname grammalecte
# data-only package
%global   debug_package %{nil}
%global   __python %{_bindir}/python3

# NOTE: this package is not noarch because LibreOffice has no
# arch-independent extension location

Name:          libreoffice-%{extname}
Version:       0.5.14
Release:       4%{?dist}
Summary:       French grammar corrector
Summary(fr):   Correcteur grammatical Français
Group:         System Environment/Libraries

# *.py from Lightproof are MPLv2.0, extension is GPLv3 and later
License:       GPLv3+ and MPLv2.0
URL:           http://www.dicollecte.org/grammalecte/
Source0:       http://www.dicollecte.org/grammalecte/oxt/Grammalecte-fr-v%{version}.oxt
Source1:       %{name}.metainfo.xml

BuildRequires: python3-devel
BuildRequires: libappstream-glib

Supplements:   libreoffice-langpack-fr

Requires:      libreoffice-writer
Requires:      libreoffice-langpack-fr
Requires:      libreoffice-pyuno
Requires:      python(abi) >= 3


%description
Grammalecte is a open source grammar corrector dedicated to French,
for Writer (LibreOffice, OpenOffice) and Firefox.
It is based on Lightproof, which was written for Hungarian.

Grammalecte is under development.

This package provides the LibreOffice Writer extension.


%description -l fr
Grammalecte est un correcteur grammatical open source dédié à la langue
française, pour Writer (LibreOffice, OpenOffice) et Firefox.
Il est dérivé de Lightproof, qui a été écrit pour le hongrois.

Grammalecte essaie d’apporter une aide à l’écriture du français sans
parasiter l’attention des utilisateurs avec de fausses alertes. 
Ce correcteur suit donc le principe suivant : le moins de « faux positifs »
possible ; s’il n’est pas possible de déterminer avec de fortes chances qu’une
suite de mots douteuse est erronée, le correcteur ne signalera rien.

Grammalecte est en cours de développement.

Ce paquet fournit l'extension pour LibreOffice Writer.


%prep
%setup -q -c


%build
: Nothing to build


%install
install -d -m 0755 %{buildroot}%{_libdir}/libreoffice/share/extensions/%{extname}
cp -pr * %{buildroot}%{_libdir}/libreoffice/share/extensions/%{extname}

DESTDIR=%{buildroot} appstream-util install %{SOURCE1}


%check
appstream-util validate-relax -v %{buildroot}%{_datadir}/appdata/%{name}.metainfo.xml


%files
%license README_fr.txt
%{_libdir}/libreoffice/share/extensions/%{extname}
%{_datadir}/appdata/%{name}.metainfo.xml


%changelog
* Sun Dec 25 2016 Remi Collet <remi@fedoraproject.org> - 0.5.14-4
- Add Appstream metadata

* Fri Dec 23 2016 Remi Collet <remi@fedoraproject.org> - 0.5.14-3
- add Supplements libreoffice-langpack-fr

* Fri Dec 23 2016 Remi Collet <remi@fedoraproject.org> - 0.5.14-2
- add dependencies on libreoffice-langpack-fr and libreoffice-pyuno
- enable byte compile

* Thu Dec 22 2016 Remi Collet <remi@fedoraproject.org> - 0.5.14-1
- initial package

