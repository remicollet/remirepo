# remirepo spec file for libreoffice-grammalecte
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global   extname grammalecte
# data-only package
%global   debug_package %{nil}
%global   _python_bytecompile_errors_terminate_build 0

# NOTE: this package is not noarch because LibreOffice has no
# arch-independent extension location

Name:          libreoffice-%{extname}
Version:       0.4.10.7
Release:       1%{?dist}
Summary:       French grammar corrector
Summary(fr):   Correcteur grammatical Français
Group:         System Environment/Libraries

# *.py from Lightproof are MPLv2.0, extension is GPLv3 and later
License:       GPLv3+ and MPLv2.0
URL:           http://www.dicollecte.org/grammalecte/
Source0:       http://www.dicollecte.org/grammalecte/oxt/Grammalecte-v%{version}-py27.oxt

BuildRequires: python2-devel > 2.7
BuildRequires: python2-devel < 3

Requires:      libreoffice-writer
Requires:      libreoffice-langpack-fr
Requires:      libreoffice-pyuno
Requires:      python(abi) = 2.7


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


%files
%{!?_licensedir:%global license %%doc}
%license README_fr.txt
%{_libdir}/libreoffice/share/extensions/%{extname}


%changelog
* Fri Dec 23 2016 Remi Collet <remi@fedoraproject.org> - 0.4.10.7-1
- initial package

