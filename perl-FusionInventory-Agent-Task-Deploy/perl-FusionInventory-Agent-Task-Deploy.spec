Name:           perl-FusionInventory-Agent-Task-Deploy
Version:        2.0.0
Release:        3%{?dist}
Summary:        Software deployment support for FusionInventory Agent
License:        GPLv2+
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/FusionInventory-Agent-Task-Deploy/
Source0:        http://search.cpan.org/CPAN/authors/id/F/FU/FUSINV/FusionInventory-Agent-Task-Deploy-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl >= 1:5.8.0
BuildRequires:  perl(base)
BuildRequires:  perl(inc::Module::Install)
BuildRequires:  perl(Archive::Extract)
BuildRequires:  perl(Archive::Tar)
BuildRequires:  perl(Compress::Zlib)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Digest::SHA)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Copy::Recursive)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Which)
BuildRequires:  perl(HTTP::Request)
BuildRequires:  perl(HTTP::Request::Common)
BuildRequires:  perl(HTTP::Server::Simple::CGI)
BuildRequires:  perl(JSON)
BuildRequires:  perl(LWP)
BuildRequires:  perl(Net::IP)
BuildRequires:  perl(POE)
BuildRequires:  perl(POE::Component::Client::Ping)
BuildRequires:  perl(POE::Component::Client::TCP)
BuildRequires:  perl(Test::Compile)
BuildRequires:  perl(Test::HTTP::Server::Simple)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(UNIVERSAL::require)
BuildRequires:  perl(URI::Escape)
BuildRequires:  fusioninventory-agent >= 2.2.0

Requires:       fusioninventory-agent >= 2.2.0
Requires:       perl(POE::Component::Client::Ping)
Requires:       perl(POE::Component::Client::TCP)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# RPM 4.8
%{?filter_from_provides: %filter_from_provides /perl(FusionInventory::/d}
%{?filter_from_requires: %filter_from_requires /perl(FusionInventory::/d}
%{?perl_default_filter}
# RPM 4.9
%global __provides_exclude %{?__provides_exclude:__provides_exclude|}^perl\\(FusionInventory::
%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(FusionInventory::


%description
With this module, FusionInventory can accept software deployment request
from an GLPI server with the FusionInventory plugin.


%prep
%setup -q -n FusionInventory-Agent-Task-Deploy-%{version}

# use system ones
rm -rf inc/*


%build
perl Makefile.PL \
     PREFIX=%{_prefix} \
     SYSCONFDIR=%{_sysconfdir}/fusioninventory \
     LOCALSTATEDIR=%{_localstatedir}/lib/%{name}

make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*


%check
make test


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{_datadir}/fusioninventory/lib/FusionInventory/Agent/Task/Deploy.pm
%{_datadir}/fusioninventory/lib/FusionInventory/Agent/Task/Deploy
%{_mandir}/man3/*


%changelog
* Wed May 30 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-3
- fix BuildRequires/Requires from review #812587

* Fri May 11 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-2
- filter private provides/requires

* Sun Apr 15 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- initial spec for Agent 2.2.0
- Specfile autogenerated by cpanspec 1.78.

