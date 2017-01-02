# spec file for perl-Gtk2-AppIndicator
#
# Copyright (c) 2014-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

Name:           perl-Gtk2-AppIndicator
Version:        0.15
Release:        2%{?dist}
Summary:        Perl extension for libappindicator
# From Copyright: Distributed under the same license as perl.
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Gtk2-AppIndicator/
Source0:        http://www.cpan.org/modules/by-module/Gtk2/Gtk2-AppIndicator-%{version}.tar.gz

BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Gtk2)
BuildRequires:  perl(XSLoader)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(appindicator-0.1)

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}


%description
%{summary}.


%prep
%setup -q -n Gtk2-AppIndicator-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \; -print
find %{buildroot} -type f -name '*.bs' -size 0 -exec rm -f {} \; -print

%{_fixperms} %{buildroot}/*


%check
: "make test disabled, requires a display"


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE COPYRIGHT
%doc Changes README
%{perl_vendorarch}/auto/Gtk2
%{perl_vendorarch}/Gtk2
%{_mandir}/man3/Gtk2*


%changelog
* Sun Sep  7 2014 Remi Collet <remi@fedoraproject.org> 0.15-2
- fix BR and cleaup from review #1138980

* Sun Sep  7 2014 Remi Collet <remi@fedoraproject.org> 0.15-1
- initial package