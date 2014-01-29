%global svnrel 2788
%global rdate  20140128
%global upver  0.4

Name:        qelectrotech

Summary:     An electric diagrams editor
Summary(ar): مُحرّر مخططات كهربائية
Summary(ca): Editar esquemes elèctrics
Summary(cs): Editor výkresů elektrických obvodů
Summary(de): Zeichenprogramm für Schaltpläne
Summary(el): Επεξεργασία ηλεκτρικών διαγραμμάτων
Summary(es): Un editor de esquemas eléctricos
Summary(fr): Un éditeur de schémas électriques
Summary(hr): Uredi elektro sheme
Summary(it): Un programma per disegnare schemi elettrici
Summary(pl): Edytor schematów elektrycznych
Summary(pt): Um editor de esquemas eléctricos
Summary(ru): Редактор электрических схем

# Upstream version is a float so 0.11 < 0.2 < 0.21 < 0.3
# So use %.2f with upstream acknowledgment
# Remember to check rdate and upver macro on each update
Version:     0.40
%if %{?svnrel}
Release:     0.1.svn%{svnrel}%{?dist}
%else
Release:     1%{?dist}
%endif

Group:       Applications/Engineering

# Prog is GPLv2 - Symbols/Elements are Creative Commons Attribution
License:    GPLv2+

Url:        http://qelectrotech.org/
%if 0%{?svnrel}
# svn export -r 2287 svn://svn.tuxfamily.org/svnroot/qet/qet/trunk qelectrotech-0.3-svn2287
# tar czf qelectrotech-0.3a-svn2287.tgz qelectrotech-0.3a-svn2287
Source0:    qelectrotech-%{upver}-svn%{?svnrel}.tgz
%else
Source0:    http://download.tuxfamily.org/qet/tags/%{rdate}/qelectrotech-%{upver}-src.tar.gz
%endif

BuildRequires:    desktop-file-utils
Requires(post):   desktop-file-utils
Requires(postun): desktop-file-utils
BuildRequires:    qt4-devel >= 4.6.0
Requires:         qelectrotech-symbols = %{version}-%{release}
Requires:         electronics-menu


%description
QElectroTech is a Qt4 application to design electric diagrams. It uses XML  
files for elements and diagrams, and includes both a diagram editor and an 
element editor.

%description -l cs
QElectroTech je aplikací Qt4 určenou pro návrh nákresů elektrických obvodů.
Pro prvky a nákresy používá soubory XML, a zahrnuje v sobě jak editor nákresů,
tak editor prvků.

%description -l el
Το QElectroTech είναι μια εφαρμογή Qt4 για σχεδίαση ηλεκτρικών διαγραμμάτων.
Χρησιμοποιεί αρχεία XML για στοιχεία και διαγράμματα, και περιλαμβάνει
επεξεργαστή διαγραμμάτων καθώς και επεξεργαστή στοιχείων.

%description -l es
QElectroTech es una aplicación Qt4 para diseñar esquemas eléctricos.
Utiliza archivos XML para los elementos y esquemas, e incluye un editor 
de esquemas y un editor de elemento.

%description -l fr
QElectroTech est une application Qt4 pour réaliser des schémas électriques.
QET utilise le format XML pour ses éléments et ses schémas et inclut un
éditeur de schémas ainsi qu'un éditeur d'élément.

%description -l it
QElectroTech è una applicazione fatta in Qt4 per disegnare schemi elettrici.
QET usa il formato XML per i suoi elementi e schemi, includendo anche un
editor per gli stessi.

%description -l pl
QElectroTech to aplikacja napisana w Qt4, przeznaczona do tworzenia schematów
elektrycznych. Wykorzystuje XML do zapisywania plików elementów i projektów.
Posiada edytor schematów i elementów.

%description -l pt
QElectroTech é uma aplicação baseada em Qt4 para desenhar esquemas eléctricos.
QET utiliza ficheiros XML para os elementos e para os esquemas e inclui um
editor de esquemas e um editor de elementos.

%description -l ru
QElectroTech - приложение написанное на Qt4 и предназначенное для разработки
электрических схем. Оно использует XML-файлы для элементов и схем, и включает,
как редактор схем, так и редактор элементов.


%package symbols
Summary:     Elements collection for QElectroTech
Summary(cs): Sbírka prvků pro QElectroTech
Summary(el): Συλλογή στοιχείων του QElectroTech
Summary(es): Collección de elementos para QElectroTech
Summary(fr): Collection d'éléments pour QElectroTech
Summary(it): Collezione di elementi per QElectroTech
Summary(pl): Kolekcja elementów QElectroTech
Summary(pt): Colecção de elementos para QElectroTech
Summary(ru): Коллекция элементов для QElectroTech
Group:       Applications/Productivity
License:     CC-BY
BuildArch:   noarch
Requires:    qelectrotech = %{version}-%{release}


%description symbols
Elements collection for QElectroTech.

%description -l cs symbols
Sbírka prvků pro QElectroTech.

%description -l el symbols
Συλλογή στοιχείων του QElectroTech.

%description -l es symbols
Collección de elementos para QElectroTech.

%description -l fr symbols
Collection d'éléments pour QElectroTech.

%description -l it symbols
Collezione di elementi per QElectroTech.

%description -l pl symbols
Kolekcja elementów QElectroTech.

%description -l pt symbols
Colecção de elementos para QElectroTech.

%description -l ru symbols
Коллекция элементов для QElectroTech.


%prep
%if 0%{?svnrel}
%setup -q -n %{name}-%{upver}-svn%{svnrel}
%else
%setup -q -n %{name}-%{upver}-src
%endif

sed -e s,/usr/local/,%{_prefix}/, \
    -e /QET_MAN_PATH/s,'man/','share/man', \
    -e /QET_MIME/s,../,, \
    -i %{name}.pro

qmake-qt4 %{name}.pro


%build
make %{?_smp_mflags}


%install
rm -f *.lang
INSTALL_ROOT=%{buildroot} make install

# We only provides UTF-8 files
rm -rf %{buildroot}/usr/doc/%{name} \
       %{buildroot}%{_datadir}/%{name}/examples \
       %{buildroot}%{_mandir}/fr.ISO8859-1 \
       %{buildroot}%{_mandir}/fr

mv %{buildroot}%{_mandir}/fr.UTF-8 %{buildroot}%{_mandir}/fr

desktop-file-install --vendor="" \
   --add-category=Electronics \
   --dir=%{buildroot}%{_datadir}/applications/ \
         %{buildroot}%{_datadir}/applications/%{name}.desktop

# QT translation provided by QT.
rm -f %{buildroot}%{_datadir}/%{name}/lang/qt_*.qm

%find_lang qet          --with-qt
%find_lang qelectrotech --with-man
cat qet.lang >>qelectrotech.lang


%post
/usr/bin/update-desktop-database &>/dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &>/dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor

%postun
/usr/bin/update-desktop-database &>/dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &>/dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%doc CREDIT LICENSE examples
%{_bindir}/%{name}
%if 0%{?fedora} < 20
%exclude %{_datadir}/appdata/%{name}.appdata.xml
%else
%{_datadir}/appdata/%{name}.appdata.xml
%endif
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/application/x-qet-*.xml
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/mimelnk/application/x-qet-*.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/lang
%{_mandir}/man1/%{name}.*


%files symbols
%doc ELEMENTS.LICENSE
%{_datadir}/%{name}/elements
%{_datadir}/%{name}/titleblocks


%changelog
* Wed Jan 29 2014 Remi Collet <remi@fedoraproject.org> - 0.40-0.1.svn2788
- Update to 0.4 snapshot revision 2788

* Tue Jan 28 2014 Remi Collet <remi@fedoraproject.org> - 0.30-2.svn2786
- Update to 0.3 snapshot revision 2786

* Sat Sep 28 2013 Remi Collet <remi@fedoraproject.org> - 0.30-1
- Version 0.3 finale

* Tue Sep 10 2013 Remi Collet <remi@fedoraproject.org> - 0.30-0.10.rc
- 0.3 Release Candidate

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-0.9.beta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 18 2013 Remi Collet <remi@fedoraproject.org> - 0.30-0.8.beta
- 0.3beta

* Tue Apr 16 2013 Remi Collet <remi@fedoraproject.org> - 0.30-0.7.svn2116
- pull latest changes from SVN

* Sun Feb 24 2013 Remi Collet <remi@fedoraproject.org> - 0.30-0.6.svn2045
- pull latest changes from SVN (gcc 4.8 fixes)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-0.5.svn1844
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-0.4.svn1844
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Remi Collet <remi@fedoraproject.org> - 0.30-0.3.svn1844
- pull latest change (packaging request) from SVN
- preserve timestamps on elements collection
- add missing titleblocks
- add cs + pl summary and description

* Sun May 13 2012 Remi Collet <remi@fedoraproject.org> - 0.30-0.2.alpha
- modernize scriptlets

* Sun May 13 2012 Remi Collet <remi@fedoraproject.org> - 0.30-0.1.alpha
- update to 0.3a

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-4.1
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 07 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.22-1.1
- set symbols as noarch on EL-6

* Sat Mar 13 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.22-1
- update to 0.22

* Sat Mar 06 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.21-1
- update to 0.21
- more translations (sumnary and description)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 27 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.20-1
- update to 0.2 finale

* Sat Jun 20 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.20-0.2.rc2
- update to RC2

* Thu Jun 18 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.20-0.2.rc1
- changes from review (#505867)
- add multi-lang sumnary (taken from .desktop)
- add multi-lang description (taken from README)
- rename qlectrotech-elements to -symbols
- use electronics-menu

* Sun Jun 14 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.20-0.1.rc1
- initial RPM for fedora

