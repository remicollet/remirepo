%define debug_package          %{nil}

%define src_ver 0.50-0
%define languageenglazy Maltese
%define languagecode mt
%define lc_ctype mt_MT

Summary:       %{languageenglazy} files for aspell
Name:          aspell-%{languagecode}
Version:       0.50.0
Release:       1
Group:         System/Internationalization
Source:	       http://ftp.gnu.org/gnu/aspell/dict/%{languagecode}/aspell-%{languagecode}-%{src_ver}.tar.bz2
URL:		   http://aspell.net/
License:	   LGPL

Buildrequires: aspell >= 12:0.60
Requires: aspell >= 12:0.60

%description
A %{languageenglazy} dictionary for use with aspell, a spelling checker.

%prep
%setup -q -n %{name}-%{src_ver}

%build
./configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README* Copyright doc/*
%{_libdir}/aspell-0.60/*


%changelog
* Sat Apr 16 2016 Remi Collet <remi@remirepo.net> 0.50.0-1
- port from mageia to Fedora / RHEL / CentOS

* Fri Feb 05 2016 umeabot <umeabot> 0.50.0-16.mga6
+ Revision: 939937
- Mageia 6 Mass Rebuild

* Wed Oct 15 2014 umeabot <umeabot> 0.50.0-15.mga5
+ Revision: 743701
- Second Mageia 5 Mass Rebuild

* Tue Sep 16 2014 umeabot <umeabot> 0.50.0-14.mga5
+ Revision: 677965
- Mageia 5 Mass Rebuild

* Fri Oct 18 2013 umeabot <umeabot> 0.50.0-13.mga4
+ Revision: 502738
- Mageia 4 Mass Rebuild

* Fri Jan 11 2013 umeabot <umeabot> 0.50.0-12.mga3
+ Revision: 346326
- Mass Rebuild - https://wiki.mageia.org/en/Feature:Mageia3MassRebuild

* Thu Feb 16 2012 kamil <kamil> 0.50.0-11.mga2
+ Revision: 209535
- stop providing enchant-dictionary
- clean .spec a bit

  + dmorgan <dmorgan>
    - Remove mandriva occurencies

  + ahmad <ahmad>
    - imported package aspell-mt


* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 0.50.0-10mdv2011.0
+ Revision: 603445
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 0.50.0-9mdv2010.1
+ Revision: 518946
- rebuild

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 0.50.0-8mdv2010.0
+ Revision: 413089
- rebuild

* Fri Mar 06 2009 Antoine Ginies <aginies@mandriva.com> 0.50.0-7mdv2009.1
+ Revision: 350079
- 2009.1 rebuild

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 0.50.0-6mdv2009.0
+ Revision: 220423
- rebuild

* Sun Mar 09 2008 Anssi Hannula <anssi@mandriva.org> 0.50.0-5mdv2008.1
+ Revision: 182504
- provide enchant-dictionary

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 0.50.0-4mdv2008.1
+ Revision: 148831
- rebuild
- kill re-definition of %%buildroot on Pixel's request
- s/Mandrake/Mandriva/

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot


* Wed Feb 21 2007 Oden Eriksson <oeriksson@mandriva.com> 0.50.0-3mdv2007.0
+ Revision: 123335
- Import aspell-mt

* Wed Feb 21 2007 Oden Eriksson <oeriksson@mandriva.com> 0.50.0-3mdv2007.1
- use the mkrel macro
- disable debug packages

* Fri Dec 03 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.50.0-2mdk
- rebuild for new aspell

* Tue Jul 20 2004 Pablo Saratxaga <pablo@mandrakesoft.com> 0.50.0-1mdk
- first version

