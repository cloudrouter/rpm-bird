%global _hardened_build 1

Summary: BIRD Internet Routing Daemon
Name: bird
Version: 1.5.0
Release: 2%{?dist}
License: GPLv2+
Group: System Environment/Daemons
URL: http://bird.network.cz

Source0: ftp://bird.network.cz/pub/bird/bird-%{version}.tar.gz
Source1: bird.service
Source2: bird.sysconfig

BuildRequires: gcc
BuildRequires: make
BuildRequires: flex
BuildRequires: bison
BuildRequires: ncurses-devel
BuildRequires: readline-devel
BuildRequires: sed
BuildRequires: systemd

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
BIRD is a dynamic routing daemon supporting IPv4 and IPv6 versions of the routing
protocols BGP, RIP and OSPF.

%prep
%autosetup

%build
%configure --prefix=%{_prefix} \
           --sysconfdir=%{_sysconfdir} \
           --localstatedir=%{_localstatedir} \
           --enable-ipv6
make %{?_smp_mflags}
mv bird bird6
mv birdc birdc6
mv birdcl birdcl6
make clean
%configure --prefix=%{_prefix} \
           --sysconfdir=%{_sysconfdir} \
           --localstatedir=%{_localstatedir}
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
install bird6 %{buildroot}/usr/sbin
install birdc6 %{buildroot}/usr/sbin
install birdcl6 %{buildroot}/usr/sbin

install doc/bird.conf.example %{buildroot}/etc/bird.conf
install doc/bird.conf.example %{buildroot}/etc/bird6.conf

install -D %{SOURCE1} %{buildroot}%{_unitdir}/bird.service
install -D %{SOURCE1} %{buildroot}%{_unitdir}/bird6.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/bird
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/bird6

%post
%systemd_post bird.service
%systemd_post bird6.service

%preun
%systemd_preun bird.service
%systemd_preun bird6.service

%postun
%systemd_postun_with_restart bird.service
%systemd_postun_with_restart bird6.service

%files
%defattr(-,root,root,-)
%doc NEWS README TODO
%doc doc/bird*.html
%config(noreplace) %{_sysconfdir}/bird.conf
%config(noreplace) %{_sysconfdir}/bird6.conf
%config(noreplace) %{_sysconfdir}/sysconfig/bird
%config(noreplace) %{_sysconfdir}/sysconfig/bird6
%{_unitdir}/bird.service
%{_sbindir}/bird
%{_sbindir}/birdc
%{_sbindir}/birdcl
%{_unitdir}/bird6.service
%{_sbindir}/bird6
%{_sbindir}/birdc6
%{_sbindir}/birdcl6

%changelog
* Sat Jan 16 2016 Arun Babu Neelicattu <arun.neelicattu@gmail.com> - 1.5.0-2
- Fix systemd unit to reload service correctly
- Use unit name in systemd unit as an alternative to sed patching
- Introduce use of environment file in systemd unit with empty defaults
- Add missing default IPv4 config file
- Clean up specfile

* Thu Jul 02 2015 John Siegrist <jsiegrist@iix.net> - 1.5.0-1
- Added dist macro to Release

* Fri May 22 2015 David Jorm <djorm@iix.net> - 1.5.0-1
- Rebase on bird 1.5.0

* Fri May 22 2015 David Jorm <djorm@iix.net> - 1.4.5-2
- Update service file to use -R flag to reload bird process

* Thu Feb 26 2015 David Jorm <djorm@iix.net> - 1.4.5-1
- Initial release
