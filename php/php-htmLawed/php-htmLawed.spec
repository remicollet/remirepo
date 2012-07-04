%global libname htmLawed

Name:           php-%{libname}
Version:        1.1.11
Release:        2%{?dist}
Summary:        PHP code to purify and filter HTML
Group:          Development/Libraries
License:        LGPLv3 and GPLv2+
URL:            http://www.bioinformatics.org/phplabware/internal_utilities/htmLawed/

# Latest archive is not versionned
# No license included
# see http://www.bioinformatics.org/phplabware/forum/viewtopic.php?id=220
Source0:        http://www.bioinformatics.org/phplabware/downloads/%{libname}.zip

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       php-ctype
Requires:       php-pcre


%description
PHP code to purify and filter HTML

* make HTML markup in text secure and standard-compliant
* process text for use in HTML, XHTML or XML documents
* restrict HTML elements, attributes or URL protocols
  using black or white-lists
* balance tags, check element nesting, transform deprecated
  attributes and tags, make relative URLs absolute, etc.
* fast, highly customizable, well-documented
* single, 48 kb file
* simple HTML Tidy alternative
* free and licensed under LGPL v3 and GPL v2+
* use to filter, secure and sanitize HTML in blog comments or
  forum posts, generate XML-compatible feed items from web-page
  excerpts, convert HTML to XHTML, pretty-print HTML, scrape
  web-pages, reduce spam, remove XSS code, etc.


%prep
%setup -qc

chmod -x htm*


%build
# nothing to build


%install
rm -rf %{buildroot}
install -d %{buildroot}%{_datadir}/php/%{libname}
install -pm 0644 %{libname}.php %{buildroot}%{_datadir}/php/%{libname}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc *README* *TESTCASE* htmLawedTest.php
%{_datadir}/php/%{libname}


%changelog
* Wed Jul 04 2012 Remi Collet <remi@fedoraproject.org> - 1.1.11-2
- fix License per review comment (#836587)

* Fri Jun 29 2012 Remi Collet <remi@fedoraproject.org> - 1.1.11-1
- initial package

