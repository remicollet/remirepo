%global perlname AnyEvent-HTTP

Name:      perl-AnyEvent-HTTP
Version:   1.46
Release:   1%{?dist}
Summary:   Simple but non-blocking HTTP/HTTPS client  

Group:     Development/Libraries
License:   GPL+ or Artistic
URL:       http://search.cpan.org/dist/AnyEvent-HTTP/
Source:    http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/%{perlname}-%{version}.tar.gz

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: perl
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(AnyEvent) >= 5.0

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}


%description
This module is an AnyEvent user, you need to make sure that you use and
run a supported event loop.

This module implements a simple, stateless and non-blocking HTTP client.
It supports GET, POST and other request methods, cookies and more, all
on a very low level. It can follow redirects supports proxies and
automatically limits the number of connections to the values specified
in the RFC.

It should generally be a "good client" that is enough for most HTTP
tasks. Simple tasks should be simple, but complex tasks should still be
possible as the user retains control over request and response headers.

The caller is responsible for authentication management, cookies (if the
simplistic implementation in this module doesn't suffice), referrer and
other high-level protocol details for which this module offers only
limited support.


%prep
%setup -q -n %{perlname}-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';' -print
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';' -print
chmod -R u+rwX,go+rX,go-w %{buildroot}/*


%clean
rm -rf %{buildroot}


%check
make test


%files
%defattr(-, root, root, -)
%doc Changes COPYING README
%{_mandir}/man3/Any*
%{perl_vendorlib}/AnyEvent


%changelog
* Sun Dec 26 2010 Remi Collet <Fedora@famillecollet.com> 1.46-1
- initial spec for Extras

