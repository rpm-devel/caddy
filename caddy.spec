%global xcaddy_version 0.4.5

Name:           caddy
Version:        2.11.4
Release:        1%{?dist}
Summary:        Powerful, enterprise-ready, open source web server with automatic HTTPS
License:        Apache-2.0
URL:            https://caddyserver.com
Source0:        https://github.com/caddyserver/caddy/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        caddy.service
Source2:        Caddyfile
Source3:        default-web-pages.tar.gz

ExclusiveArch:  x86_64 aarch64
# EL7 ships Go 1.x which is too old for Caddy 2.x (requires Go 1.22+).
# Caddy 2.x cannot be built on EL7; use the pre-built binary or a newer
# Go toolchain from a third-party repo (e.g. golang-1.22 from COPR).
%if 0%{?rhel} == 7
BuildRequires:  golang >= 1.17
%else
BuildRequires:  golang >= 1.22
%endif
BuildRequires:  systemd-rpm-macros
Requires(pre):  shadow-utils
%{?systemd_requires}
Provides:       webserver

%description
Caddy is a powerful, enterprise-ready, open source web server with automatic
HTTPS written in Go. It is the most widely-used alternative web server in
the Go ecosystem.

Features include:
- Automatic HTTPS via Let's Encrypt and ZeroSSL
- HTTP/1.1, HTTP/2, and HTTP/3 support
- Reverse proxy with load balancing
- Static file server
- Extensible with plugins via xcaddy
- Admin API for live config reloads
- JSON and Caddyfile config formats

%package -n xcaddy
Summary:        Build tool for custom Caddy builds with plugins
License:        Apache-2.0
URL:            https://github.com/caddyserver/xcaddy
Source10:       https://github.com/caddyserver/xcaddy/archive/v%{xcaddy_version}/xcaddy-%{xcaddy_version}.tar.gz

%description -n xcaddy
xcaddy makes it easy to make custom builds of the Caddy web server with
plugins. It downloads the Caddy source code, adds the specified plugins
to it, and builds the binary.

%prep
%setup -q -n %{name}-%{version}
%setup -q -T -D -b 10 -n xcaddy-%{xcaddy_version}

%build
# Build caddy
# -trimpath: remove local paths from binary for reproducibility
# -s -w: strip debug info and DWARF tables (smaller binary)
# CGO_ENABLED=0: pure Go, static binary, no libc dependency
# Build tags: nobadger disables BadgerDB (not typically packaged for EL),
#             nomysql disables MySQL storage backend,
#             nopgx disables pgx/PostgreSQL storage backend.
#             These reduce unused optional dependencies while keeping all
#             core features: HTTP/1, HTTP/2, HTTP/3, TLS, reverse proxy,
#             file server, admin API, and all standard modules.
cd %{_builddir}/%{name}-%{version}
CGO_ENABLED=0 \
go build \
    -trimpath \
    -ldflags "-s -w -X github.com/caddyserver/caddy/v2.CustomVersion=%{version}" \
    -tags "nobadger nomysql nopgx" \
    -o caddy \
    ./cmd/caddy

# Build xcaddy
cd %{_builddir}/xcaddy-%{xcaddy_version}
CGO_ENABLED=0 \
go build \
    -trimpath \
    -ldflags "-s -w" \
    -o xcaddy \
    ./cmd/xcaddy

%install
# caddy binary
install -D -m 0755 %{_builddir}/%{name}-%{version}/caddy \
    %{buildroot}%{_bindir}/caddy

# xcaddy binary
install -D -m 0755 %{_builddir}/xcaddy-%{xcaddy_version}/xcaddy \
    %{buildroot}%{_bindir}/xcaddy

# systemd unit
install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/caddy.service

# default config
install -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/caddy/Caddyfile

# runtime directories
install -d -m 0750 %{buildroot}%{_sharedstatedir}/caddy
install -d -m 0750 %{buildroot}%{_sysconfdir}/caddy
install -d -m 0750 %{buildroot}%{_localstatedir}/log/caddy

# Install default web pages
install -d -m 0750 %{buildroot}%{_sharedstatedir}/caddy/www
tar xzf %{SOURCE3} -C %{buildroot}%{_sharedstatedir}/caddy/www/

%pre
getent group caddy > /dev/null || groupadd -r caddy
getent passwd caddy > /dev/null || \
    useradd -r -g caddy -d %{_sharedstatedir}/caddy \
        -s /sbin/nologin -c "Caddy web server" caddy
exit 0

%post
%systemd_post caddy.service

%preun
%systemd_preun caddy.service

%postun
%systemd_postun_with_restart caddy.service

%files
%license LICENSE
%doc README.md
%{_bindir}/caddy
%{_unitdir}/caddy.service
%dir %attr(0750,caddy,caddy) %{_sysconfdir}/caddy
%config(noreplace) %attr(0640,caddy,caddy) %{_sysconfdir}/caddy/Caddyfile
%dir %attr(0750,caddy,caddy) %{_sharedstatedir}/caddy
%dir %attr(0750,caddy,caddy) %{_sharedstatedir}/caddy/www
%{_sharedstatedir}/caddy/www/*.html
%dir %attr(0750,caddy,caddy) %{_localstatedir}/log/caddy

%files -n xcaddy
%license %{_builddir}/xcaddy-%{xcaddy_version}/LICENSE
%doc %{_builddir}/xcaddy-%{xcaddy_version}/README.md
%{_bindir}/xcaddy

%changelog
* Thu Jul 03 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 2.11.4-1
- Version: 2.11.2 → 2.11.4; xcaddy: 0.4.4 → 0.4.5
- Source0/Source10: GitHub archive URLs verified (200)
- ExclusiveArch: x86_64 aarch64; systemd-rpm-macros

* Thu Apr 24 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 2.11.2-1
- Complete rewrite for Caddy v2
- Add xcaddy subpackage for custom builds
- Add optimized build flags: CGO_ENABLED=0, trimpath, strip ldflags
- Add build tags: nobadger nomysql nopgx (disables optional storage backends)
- Embed version string via ldflags CustomVersion
- Update systemd unit for Caddy v2 CLI (caddy run/reload)
- Add log directory /var/log/caddy owned by caddy user
- Add Caddyfile default config as Source2
- Use xcaddy_version global for consistent subpackage versioning

* Tue Mar 27 2019 Carl George <carl@george.computer> - 0.11.4-1
- Initial Caddy v1 package
