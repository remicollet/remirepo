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
%undefine py_auto_byte_compile

# NOTE: this package is not noarch because LibreOffice has no
# arch-independent extension location

Name:          libreoffice-%{extname}
Version:       0.5.14
Release:       1%{?dist}
Summary:       French grammar corrector
Summary(fr):   Correcteur grammatical Français
Group:         System Environment/Libraries

# *.py are MPLv2.0, extension is GPLv3 and later
License:       GPLv3+ and MPLv2.0
URL:           http://www.dicollecte.org/grammalecte/
Source0:       http://www.dicollecte.org/grammalecte/oxt/Grammalecte-fr-v%{version}.oxt

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:      libreoffice-writer


%description
French grammar corrector for Writer (LibreOffice).


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


%prep
%setup -q -c


%build
: Nothing to build


%install
rm -rf %{buildroot}

install -d -m 0755 %{buildroot}%{_libdir}/libreoffice/share/extensions/%{extname}
cp -pr * %{buildroot}%{_libdir}/libreoffice/share/extensions/%{extname}


%clean
rm -rf %{buildroot}



%files
%defattr (-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license README_fr.txt
%{_libdir}/libreoffice/share/extensions/%{extname}


%changelog
* Thu Dec 22 2016 Remi Collet <remi@fedoraproject.org> - 0.5.14-1
- initial package

