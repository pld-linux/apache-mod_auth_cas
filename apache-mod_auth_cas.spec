%define		mod_name	auth_cas
%define 	apxs		%{_sbindir}/apxs
Summary:	Apache module: CAS
Summary(pl.UTF-8):	Moduł Apache'a: CAS
Name:		apache-mod_%{mod_name}
Version:	1.0.8
Release:	0.1
License:	GPL v3+
Group:		Networking/Daemons/HTTP
# svn export https://www.ja-sig.org/svn/cas-clients/mod_auth_cas/tags/mod_auth_cas-1.0.8
Source0:	mod_%{mod_name}-%{version}.tar.bz2
# Source0-md5:	2bd4117f7a8b25ade77f53c59c66944a
Source1:	%{name}.conf
URL:		https://www.ja-sig.org/svn/cas-clients/mod_auth_cas/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.2
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
Apache CAS Authentication Module.

%description -l pl.UTF-8
Moduł Apache'a do uwierzytelniania poprzez CAS.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} -c src/mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

install src/.libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
