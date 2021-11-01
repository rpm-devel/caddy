# plugins
%bcond_without geoip
%bcond_without realip
%bcond_without cloudflare
%bcond_without digitalocean
%bcond_without dyn
%bcond_without gandi
%bcond_without namecheap
%bcond_without pdns
%bcond_without rackspace
%bcond_without rfc2136
%bcond_without googlecloud
%bcond_without route53
%bcond_without azure

%if %{with azure}%{with cloudflare}%{with digitalocean}%{with dyn}%{with gandi}%{with googlecloud}%{with namecheap}%{with pdns}%{with rackspace}%{with rfc2136}%{with route53}
%bcond_without dnsproviders
%endif

%bcond_with debug

%if %{with debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif

%if %{undefined gobuild}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%endif

Name: caddy
Version: 0.11.4
Release: 1%{?dist}
Summary: HTTP/2 web server with automatic HTTPS
License: ASL 2.0 and MIT
URL: https://caddyserver.com
ExclusiveArch: %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm} aarch64 ppc64le s390x %{mips}}
%{?go_compiler:BuildRequires: compiler(go-compiler)}
# https://github.com/mholt/caddy/pull/2267
BuildRequires: golang >= 1.10
BuildRequires: systemd
%{?systemd_requires}
Provides: webserver

# caddy
%global import_path github.com/mholt/caddy
Source0: https://%{import_path}/archive/v%{version}/caddy-%{version}.tar.gz
Source1: caddy.conf
Source2: caddy.service
Source3: index.html

# dnsproviders
%global import_path_dnsproviders github.com/caddyserver/dnsproviders
%global version_dnsproviders 0.1.3
Source10: https://%{import_path_dnsproviders}/archive/v%{version_dnsproviders}/dnsproviders-%{version_dnsproviders}.tar.gz

# lego
%global import_path_lego github.com/xenolf/lego
%global version_lego 2.2.0
Source11: https://%{import_path_lego}/archive/v%{version_lego}/lego-%{version_lego}.tar.gz

%if %{with azure}
Provides: bundled(golang(%{import_path_dnsproviders}/azure)) = %{version_dnsproviders}
Provides: bundled(golang(%{import_path_lego}/providers/dns/azure)) = %{version_lego}
%endif
%if %{with cloudflare}
Provides: bundled(golang(%{import_path_dnsproviders}/cloudflare)) = %{version_dnsproviders}
Provides: bundled(golang(%{import_path_lego}/providers/dns/cloudflare)) = %{version_lego}
%endif
%if %{with digitalocean}
Provides: bundled(golang(%{import_path_dnsproviders}/digitalocean)) = %{version_dnsproviders}
Provides: bundled(golang(%{import_path_lego}/providers/dns/digitalocean)) = %{version_lego}
%endif
%if %{with dyn}
Provides: bundled(golang(%{import_path_dnsproviders}/dyn)) = %{version_dnsproviders}
Provides: bundled(golang(%{import_path_lego}/providers/dns/dyn)) = %{version_lego}
%endif
%if %{with gandi}
Provides: bundled(golang(%{import_path_dnsproviders}/gandi)) = %{version_dnsproviders}
Provides: bundled(golang(%{import_path_lego}/providers/dns/gandi)) = %{version_lego}
%endif
%if %{with googlecloud}
Provides: bundled(golang(%{import_path_dnsproviders}/googlecloud)) = %{version_dnsproviders}
Provides: bundled(golang(%{import_path_lego}/providers/dns/googlecloud)) = %{version_lego}
%endif
%if %{with namecheap}
Provides: bundled(golang(%{import_path_dnsproviders}/namecheap)) = %{version_dnsproviders}
Provides: bundled(golang(%{import_path_lego}/providers/dns/namecheap)) = %{version_lego}
%endif
%if %{with pdns}
Provides: bundled(golang(%{import_path_dnsproviders}/pdns)) = %{version_dnsproviders}
Provides: bundled(golang(%{import_path_lego}/providers/dns/pdns)) = %{version_lego}
%endif
%if %{with rackspace}
Provides: bundled(golang(%{import_path_dnsproviders}/rackspace)) = %{version_dnsproviders}
Provides: bundled(golang(%{import_path_lego}/providers/dns/rackspace)) = %{version_lego}
%endif
%if %{with rfc2136}
Provides: bundled(golang(%{import_path_dnsproviders}/rfc2136)) = %{version_dnsproviders}
Provides: bundled(golang(%{import_path_lego}/providers/dns/rfc2136)) = %{version_lego}
%endif
%if %{with route53}
Provides: bundled(golang(%{import_path_dnsproviders}/route53)) = %{version_dnsproviders}
Provides: bundled(golang(%{import_path_lego}/providers/dns/route53)) = %{version_lego}
%endif

# geoip
%global import_path_geoip github.com/kodnaplakal/caddy-geoip
%global commit_geoip 6af15b436fdcb08a743c30f9bad044ad32b53b49
Source20: https://%{import_path_geoip}/archive/%{commit_geoip}/geoip-%{commit_geoip}.tar.gz
%if %{with geoip}
Provides: bundled(golang(%{import_path_geoip})) = %{commit_geoip}
BuildRequires: golang(github.com/oschwald/maxminddb-golang)
%endif

# realip
%global import_path_realip github.com/captncraig/caddy-realip
%global commit_realip 5dd1f4047d0f649f21ba9f8d7e491d712be9a5b0
Source21: https://%{import_path_realip}/archive/%{commit_realip}/realip-%{commit_realip}.tar.gz
%if %{with realip}
Provides: bundled(golang(%{import_path_realip})) = %{commit_realip}
%endif

# vendored libraries (Source0)
Provides: bundled(golang(cloud.google.com/go/compute/metadata)) = 7a4ba9f439fbc50061834a4063b57cf7222ba83f
Provides: bundled(golang(github.com/aead/chacha20)) = 8b13a72661dae6e9e5dea04f344f0dc95ea29547
Provides: bundled(golang(github.com/alecthomas/template)) = a0175ee3bccc567396460bf5acd36800cb10c49c
Provides: bundled(golang(github.com/alecthomas/units)) = 2efee857e7cfd4f3d0138cc3cbb1b4966962b93a
Provides: bundled(golang(github.com/codahale/aesnicheck)) = 349fcc471aaccc29cd074e1275f1a494323826cd
Provides: bundled(golang(github.com/dustin/go-humanize)) = 259d2a102b871d17f30e3cd9881a642961a1e486
Provides: bundled(golang(github.com/flynn/go-shlex)) = 3f9db97f856818214da2e1057f8ad84803971cff
Provides: bundled(golang(github.com/golang/mock/gomock)) = 600781dde9cca80734169b9e969d9054ccc57937
Provides: bundled(golang(github.com/golang/protobuf/proto)) = 748d386b5c1ea99658fd69fe9f03991ce86a90c1
Provides: bundled(golang(github.com/golang/protobuf/ptypes/any)) = 748d386b5c1ea99658fd69fe9f03991ce86a90c1
Provides: bundled(golang(github.com/google/uuid)) = dec09d789f3dba190787f8b4454c7d3c936fed9e
Provides: bundled(golang(github.com/gorilla/websocket)) = a69d9f6de432e2c6b296a947d8a5ee88f68522cf
Provides: bundled(golang(github.com/hashicorp/go-syslog)) = 326bf4a7f709d263f964a6a96558676b103f3534
Provides: bundled(golang(github.com/jimstudt/http-authentication/basic)) = 3eca13d6893afd7ecabe15f4445f5d2872a1b012
Provides: bundled(golang(github.com/klauspost/cpuid)) = ae832f27941af41db13bd6d8efd2493e3b22415a
Provides: bundled(golang(github.com/lucas-clemente/quic-go)) = f90751eabaa39364e3861ee5a8b179f140847d7e
Provides: bundled(golang(github.com/mholt/certmagic)) = a7f18a937c080b88693cd4e14d48e42cc067b268
Provides: bundled(golang(github.com/miekg/dns)) = 0f3adef2e2201d72e50309a36fc99d8a9d1a4960
Provides: bundled(golang(github.com/naoina/go-stringutil)) = 6b638e95a32d0c1131db0e7fe83775cbea4a0d0b
Provides: bundled(golang(github.com/naoina/toml)) = e6f5723bf2a66af014955e0888881314cf294129
Provides: bundled(golang(github.com/russross/blackfriday)) = 067529f716f4c3f5e37c8c95ddd59df1007290ae
Provides: bundled(golang(github.com/xenolf/lego/acme)) = a43ec709e8034f388aab28d14b97aeed0e7aa98c
Provides: bundled(golang(github.com/xenolf/lego/certcrypto)) = a43ec709e8034f388aab28d14b97aeed0e7aa98c
Provides: bundled(golang(github.com/xenolf/lego/certificate)) = a43ec709e8034f388aab28d14b97aeed0e7aa98c
Provides: bundled(golang(github.com/xenolf/lego/challenge)) = a43ec709e8034f388aab28d14b97aeed0e7aa98c
Provides: bundled(golang(github.com/xenolf/lego/lego)) = f05aa4c241fd8b43da9dc8cab8c8965e5b3c1b55
Provides: bundled(golang(github.com/xenolf/lego/log)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/platform/wait)) = a43ec709e8034f388aab28d14b97aeed0e7aa98c
Provides: bundled(golang(github.com/xenolf/lego/registration)) = a43ec709e8034f388aab28d14b97aeed0e7aa98c
Provides: bundled(golang(github.com/xenolf/lego/vendor/github.com/miekg/dns)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/crypto/ed25519)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/crypto/ocsp)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/crypto/pbkdf2)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/net/bpf)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/net/idna)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/net/internal/iana)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/net/internal/socket)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/net/ipv4)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/net/ipv6)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/sys/unix)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/text/collate)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/text/internal/colltab)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/text/internal/gen)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/text/internal/tag)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/text/internal/triegen)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/text/internal/ucd)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/text/language)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/text/secure/bidirule)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/text/transform)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/text/unicode/bidi)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/text/unicode/cldr)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/text/unicode/norm)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/golang.org/x/text/unicode/rangetable)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(github.com/xenolf/lego/vendor/gopkg.in/square/go-jose.v2)) = b05b54d1f69a31ceed92e2995243c5b17821c9e4
Provides: bundled(golang(go4.org/syncutil/singleflight)) = 034d17a462f7b2dcd1a4a73553ec5357ff6e6c6e
Provides: bundled(golang(golang.org/x/crypto/curve25519)) = 94eea52f7b742c7cbe0b03b22f0c4c8631ece122
Provides: bundled(golang(golang.org/x/crypto/ed25519)) = c4a91bd4f524f10d064139674cf55852e055ad01
Provides: bundled(golang(golang.org/x/crypto/hkdf)) = 2faea1465de239e4babd8f5905cc25b781712442
Provides: bundled(golang(golang.org/x/crypto/ocsp)) = 2faea1465de239e4babd8f5905cc25b781712442
Provides: bundled(golang(golang.org/x/crypto/ssh/terminal)) = 2faea1465de239e4babd8f5905cc25b781712442
Provides: bundled(golang(golang.org/x/net/context)) = f5079bd7f6f74e23c4d65efa0f4ce14cbd6a3c0f
Provides: bundled(golang(golang.org/x/net/http/httpguts)) = 8a410e7b638dca158bf9e766925842f6651ff828
Provides: bundled(golang(golang.org/x/net/http2)) = f5079bd7f6f74e23c4d65efa0f4ce14cbd6a3c0f
Provides: bundled(golang(golang.org/x/net/idna)) = f5079bd7f6f74e23c4d65efa0f4ce14cbd6a3c0f
Provides: bundled(golang(golang.org/x/net/lex/httplex)) = f5079bd7f6f74e23c4d65efa0f4ce14cbd6a3c0f
Provides: bundled(golang(golang.org/x/net/publicsuffix)) = f5079bd7f6f74e23c4d65efa0f4ce14cbd6a3c0f
Provides: bundled(golang(golang.org/x/oauth2)) = b53b38ad8a6435bd399ea76d0fa74f23149cca4e
Provides: bundled(golang(golang.org/x/sys/cpu)) = 49385e6e15226593f68b26af201feec29d5bba22
Provides: bundled(golang(golang.org/x/sys/unix)) = 35ef4487ce0a1ea5d4b616ffe71e34febe723695
Provides: bundled(golang(golang.org/x/text/internal/gen)) = 836efe42bb4aa16aaa17b9c155d8813d336ed720
Provides: bundled(golang(golang.org/x/text/internal/triegen)) = 836efe42bb4aa16aaa17b9c155d8813d336ed720
Provides: bundled(golang(golang.org/x/text/internal/ucd)) = 836efe42bb4aa16aaa17b9c155d8813d336ed720
Provides: bundled(golang(golang.org/x/text/secure/bidirule)) = 836efe42bb4aa16aaa17b9c155d8813d336ed720
Provides: bundled(golang(golang.org/x/text/transform)) = 836efe42bb4aa16aaa17b9c155d8813d336ed720
Provides: bundled(golang(golang.org/x/text/unicode/bidi)) = 836efe42bb4aa16aaa17b9c155d8813d336ed720
Provides: bundled(golang(golang.org/x/text/unicode/cldr)) = 836efe42bb4aa16aaa17b9c155d8813d336ed720
Provides: bundled(golang(golang.org/x/text/unicode/norm)) = 836efe42bb4aa16aaa17b9c155d8813d336ed720
Provides: bundled(golang(golang.org/x/text/unicode/rangetable)) = 836efe42bb4aa16aaa17b9c155d8813d336ed720
Provides: bundled(golang(google.golang.org/api/compute/v1)) = 66dba45b06824cbfe030e696b156d562994531e1
Provides: bundled(golang(google.golang.org/api/gensupport)) = 66dba45b06824cbfe030e696b156d562994531e1
Provides: bundled(golang(google.golang.org/api/googleapi)) = 66dba45b06824cbfe030e696b156d562994531e1
Provides: bundled(golang(google.golang.org/appengine)) = ad2570cd3913654e00c5f0183b39d2f998e54046
Provides: bundled(golang(gopkg.in/alecthomas/kingpin.v2)) = 1087e65c9441605df944fb12c33f0fe7072d18ca
Provides: bundled(golang(gopkg.in/natefinch/lumberjack.v2)) = 7d6a1875575e09256dc552b4c0e450dcd02bd10e
Provides: bundled(golang(gopkg.in/square/go-jose.v2)) = 6ee92191fea850cdcab9a18867abf5f521cdbadb
Provides: bundled(golang(gopkg.in/yaml.v2)) = 25c4ec802a7d637f88d584ab26798e94ad14c13b

# vendored libraries (Source11)
Provides:       bundled(golang(cloud.google.com/go/compute/metadata)) = 0.26.0
Provides:       bundled(golang(github.com/Azure/azure-sdk-for-go/services/dns/mgmt/2017-09-01/dns)) = 19.1.0
Provides:       bundled(golang(github.com/Azure/azure-sdk-for-go/version)) = 19.1.0
Provides:       bundled(golang(github.com/Azure/go-autorest/autorest)) = 10.15.2
Provides:       bundled(golang(github.com/Azure/go-autorest/autorest/adal)) = 10.15.2
Provides:       bundled(golang(github.com/Azure/go-autorest/autorest/azure)) = 10.15.2
Provides:       bundled(golang(github.com/Azure/go-autorest/autorest/azure/auth)) = 10.15.2
Provides:       bundled(golang(github.com/Azure/go-autorest/autorest/date)) = 10.15.2
Provides:       bundled(golang(github.com/Azure/go-autorest/autorest/to)) = 10.15.2
Provides:       bundled(golang(github.com/Azure/go-autorest/autorest/validation)) = 10.15.2
Provides:       bundled(golang(github.com/Azure/go-autorest/logger)) = 10.15.2
Provides:       bundled(golang(github.com/Azure/go-autorest/version)) = 10.15.2
Provides:       bundled(golang(github.com/JamesClonk/vultr/lib)) = 1.15.0
Provides:       bundled(golang(github.com/OpenDNS/vegadns2client)) = a3fa4a771d87bda2514a90a157e1fed1b6897d2e
Provides:       bundled(golang(github.com/akamai/AkamaiOPEN-edgegrid-golang/client-v1)) = 0.7.3
Provides:       bundled(golang(github.com/akamai/AkamaiOPEN-edgegrid-golang/configdns-v1)) = 0.7.3
Provides:       bundled(golang(github.com/akamai/AkamaiOPEN-edgegrid-golang/edgegrid)) = 0.7.3
Provides:       bundled(golang(github.com/akamai/AkamaiOPEN-edgegrid-golang/jsonhooks-v1)) = 0.7.3
Provides:       bundled(golang(github.com/aliyun/alibaba-cloud-sdk-go/sdk)) = 1.27.7
Provides:       bundled(golang(github.com/aliyun/alibaba-cloud-sdk-go/sdk/auth)) = 1.27.7
Provides:       bundled(golang(github.com/aliyun/alibaba-cloud-sdk-go/sdk/auth/credentials)) = 1.27.7
Provides:       bundled(golang(github.com/aliyun/alibaba-cloud-sdk-go/sdk/auth/signers)) = 1.27.7
Provides:       bundled(golang(github.com/aliyun/alibaba-cloud-sdk-go/sdk/endpoints)) = 1.27.7
Provides:       bundled(golang(github.com/aliyun/alibaba-cloud-sdk-go/sdk/errors)) = 1.27.7
Provides:       bundled(golang(github.com/aliyun/alibaba-cloud-sdk-go/sdk/requests)) = 1.27.7
Provides:       bundled(golang(github.com/aliyun/alibaba-cloud-sdk-go/sdk/responses)) = 1.27.7
Provides:       bundled(golang(github.com/aliyun/alibaba-cloud-sdk-go/sdk/utils)) = 1.27.7
Provides:       bundled(golang(github.com/aliyun/alibaba-cloud-sdk-go/services/alidns)) = 1.27.7
Provides:       bundled(golang(github.com/aws/aws-sdk-go/aws)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/aws/awserr)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/aws/awsutil)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/aws/client)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/aws/client/metadata)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/aws/corehandlers)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/aws/credentials)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/aws/credentials/ec2rolecreds)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/aws/credentials/endpointcreds)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/aws/credentials/stscreds)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/aws/csm)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/aws/defaults)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/aws/ec2metadata)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/aws/endpoints)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/aws/request)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/aws/session)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/aws/signer/v4)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/internal/sdkio)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/internal/sdkrand)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/internal/sdkuri)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/internal/shareddefaults)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/private/protocol)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/private/protocol/json/jsonutil)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/private/protocol/jsonrpc)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/private/protocol/query)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/private/protocol/query/queryutil)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/private/protocol/rest)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/private/protocol/restxml)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/private/protocol/xml/xmlutil)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/service/lightsail)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/service/route53)) = 1.15.23
Provides:       bundled(golang(github.com/aws/aws-sdk-go/service/sts)) = 1.15.23
Provides:       bundled(golang(github.com/cenkalti/backoff)) = 2.1.1
Provides:       bundled(golang(github.com/cloudflare/cloudflare-go)) = 0.8.5
Provides:       bundled(golang(github.com/cpu/goacmedns)) = 565ecf2a84df654865cc102705ac160a3b04fc01
Provides:       bundled(golang(github.com/davecgh/go-spew/spew)) = 1.1.1
Provides:       bundled(golang(github.com/decker502/dnspod-go)) = 83a3ba562b048c9fc88229408e593494b7774684
Provides:       bundled(golang(github.com/dgrijalva/jwt-go)) = 3.2.0
Provides:       bundled(golang(github.com/dimchansky/utfbom)) = 5448fe645cb1964ba70ac8f9f2ffe975e61a536c
Provides:       bundled(golang(github.com/dnsimple/dnsimple-go/dnsimple)) = 0.21.0
Provides:       bundled(golang(github.com/exoscale/egoscale)) = 0.11.6
Provides:       bundled(golang(github.com/fatih/structs)) = 1.1.0
Provides:       bundled(golang(github.com/go-ini/ini)) = 1.38.2
Provides:       bundled(golang(github.com/go-resty/resty)) = 1.8.0
Provides:       bundled(golang(github.com/golang/protobuf/proto)) = 1.2.0
Provides:       bundled(golang(github.com/google/go-querystring/query)) = 53e6ce116135b80d037921a7fdd5138cf32d7a8a
Provides:       bundled(golang(github.com/google/uuid)) = 0.2
Provides:       bundled(golang(github.com/gophercloud/gophercloud)) = a2b0ad6ce68c8302027db1a5f9dbb03b0c8ab072
Provides:       bundled(golang(github.com/gophercloud/gophercloud/openstack)) = a2b0ad6ce68c8302027db1a5f9dbb03b0c8ab072
Provides:       bundled(golang(github.com/gophercloud/gophercloud/openstack/dns/v2/recordsets)) = a2b0ad6ce68c8302027db1a5f9dbb03b0c8ab072
Provides:       bundled(golang(github.com/gophercloud/gophercloud/openstack/dns/v2/zones)) = a2b0ad6ce68c8302027db1a5f9dbb03b0c8ab072
Provides:       bundled(golang(github.com/gophercloud/gophercloud/openstack/identity/v2/tenants)) = a2b0ad6ce68c8302027db1a5f9dbb03b0c8ab072
Provides:       bundled(golang(github.com/gophercloud/gophercloud/openstack/identity/v2/tokens)) = a2b0ad6ce68c8302027db1a5f9dbb03b0c8ab072
Provides:       bundled(golang(github.com/gophercloud/gophercloud/openstack/identity/v3/tokens)) = a2b0ad6ce68c8302027db1a5f9dbb03b0c8ab072
Provides:       bundled(golang(github.com/gophercloud/gophercloud/openstack/utils)) = a2b0ad6ce68c8302027db1a5f9dbb03b0c8ab072
Provides:       bundled(golang(github.com/gophercloud/gophercloud/pagination)) = a2b0ad6ce68c8302027db1a5f9dbb03b0c8ab072
Provides:       bundled(golang(github.com/iij/doapi)) = 8803795a9b7b938fa88ddbd63a77893beee14cd8
Provides:       bundled(golang(github.com/iij/doapi/protocol)) = 8803795a9b7b938fa88ddbd63a77893beee14cd8
Provides:       bundled(golang(github.com/jmespath/go-jmespath)) = 0b12d6b5
Provides:       bundled(golang(github.com/json-iterator/go)) = 1.1.5
Provides:       bundled(golang(github.com/juju/ratelimit)) = 1.0.1
Provides:       bundled(golang(github.com/kolo/xmlrpc)) = 16bdd962781df9696f40cc2bab924f1a855a7f89
Provides:       bundled(golang(github.com/linode/linodego)) = 0.5.1
Provides:       bundled(golang(github.com/miekg/dns)) = 1.1.0
Provides:       bundled(golang(github.com/mitchellh/go-homedir)) = 1.0.0
Provides:       bundled(golang(github.com/mitchellh/mapstructure)) = 1.1.2
Provides:       bundled(golang(github.com/modern-go/concurrent)) = 1.0.3
Provides:       bundled(golang(github.com/modern-go/reflect2)) = 1.0.1
Provides:       bundled(golang(github.com/namedotcom/go/namecom)) = 08470befbe04613bd4b44cb6978b05d50294c4d4
Provides:       bundled(golang(github.com/nrdcg/auroradns)) = 1.0.0
Provides:       bundled(golang(github.com/nrdcg/goinwx)) = 0.6.0
Provides:       bundled(golang(github.com/ovh/go-ovh/ovh)) = c3e61035ea66f5c637719c90140da4e3ac3b1bf0
Provides:       bundled(golang(github.com/pkg/errors)) = 0.8.0
Provides:       bundled(golang(github.com/pmezard/go-difflib/difflib)) = 1.0.0
Provides:       bundled(golang(github.com/rainycape/memcache)) = 1031fa0ce2f20c1c0e1e1b51951d8ea02c84fa05
Provides:       bundled(golang(github.com/sacloud/libsacloud)) = 108b1efe4b4d106fee6760bdf1847c4f92e1a92e
Provides:       bundled(golang(github.com/sacloud/libsacloud/api)) = 108b1efe4b4d106fee6760bdf1847c4f92e1a92e
Provides:       bundled(golang(github.com/sacloud/libsacloud/sacloud)) = 108b1efe4b4d106fee6760bdf1847c4f92e1a92e
Provides:       bundled(golang(github.com/sacloud/libsacloud/sacloud/ostype)) = 108b1efe4b4d106fee6760bdf1847c4f92e1a92e
Provides:       bundled(golang(github.com/satori/go.uuid)) = 1.2.0
Provides:       bundled(golang(github.com/sirupsen/logrus)) = 1.0.6
Provides:       bundled(golang(github.com/stretchr/objx)) = 0.1.1
Provides:       bundled(golang(github.com/stretchr/testify/assert)) = 1.2.2
Provides:       bundled(golang(github.com/stretchr/testify/mock)) = 1.2.2
Provides:       bundled(golang(github.com/stretchr/testify/require)) = 1.2.2
Provides:       bundled(golang(github.com/stretchr/testify/suite)) = 1.2.2
Provides:       bundled(golang(github.com/timewasted/linode)) = 37e84520dcf74488f67654f9c775b9752c232dc1
Provides:       bundled(golang(github.com/timewasted/linode/dns)) = 37e84520dcf74488f67654f9c775b9752c232dc1
Provides:       bundled(golang(github.com/transip/gotransip)) = 1dc93a7db3567a5ccf865106afac88278ba940cf
Provides:       bundled(golang(github.com/transip/gotransip/domain)) = 1dc93a7db3567a5ccf865106afac88278ba940cf
Provides:       bundled(golang(github.com/transip/gotransip/util)) = 1dc93a7db3567a5ccf865106afac88278ba940cf
Provides:       bundled(golang(github.com/urfave/cli)) = 1.20.0
Provides:       bundled(golang(golang.org/x/crypto/ed25519)) = 614d502a4dac94afa3a6ce146bd1736da82514c6
Provides:       bundled(golang(golang.org/x/crypto/ed25519/internal/edwards25519)) = 614d502a4dac94afa3a6ce146bd1736da82514c6
Provides:       bundled(golang(golang.org/x/crypto/ocsp)) = 614d502a4dac94afa3a6ce146bd1736da82514c6
Provides:       bundled(golang(golang.org/x/crypto/pbkdf2)) = 614d502a4dac94afa3a6ce146bd1736da82514c6
Provides:       bundled(golang(golang.org/x/crypto/pkcs12)) = 614d502a4dac94afa3a6ce146bd1736da82514c6
Provides:       bundled(golang(golang.org/x/crypto/pkcs12/internal/rc2)) = 614d502a4dac94afa3a6ce146bd1736da82514c6
Provides:       bundled(golang(golang.org/x/crypto/ssh/terminal)) = 614d502a4dac94afa3a6ce146bd1736da82514c6
Provides:       bundled(golang(golang.org/x/net/bpf)) = 8a410e7b638dca158bf9e766925842f6651ff828
Provides:       bundled(golang(golang.org/x/net/context)) = 8a410e7b638dca158bf9e766925842f6651ff828
Provides:       bundled(golang(golang.org/x/net/context/ctxhttp)) = 8a410e7b638dca158bf9e766925842f6651ff828
Provides:       bundled(golang(golang.org/x/net/idna)) = 8a410e7b638dca158bf9e766925842f6651ff828
Provides:       bundled(golang(golang.org/x/net/internal/iana)) = 8a410e7b638dca158bf9e766925842f6651ff828
Provides:       bundled(golang(golang.org/x/net/internal/socket)) = 8a410e7b638dca158bf9e766925842f6651ff828
Provides:       bundled(golang(golang.org/x/net/ipv4)) = 8a410e7b638dca158bf9e766925842f6651ff828
Provides:       bundled(golang(golang.org/x/net/ipv6)) = 8a410e7b638dca158bf9e766925842f6651ff828
Provides:       bundled(golang(golang.org/x/net/publicsuffix)) = 8a410e7b638dca158bf9e766925842f6651ff828
Provides:       bundled(golang(golang.org/x/oauth2)) = d2e6202438beef2727060aa7cabdd924d92ebfd9
Provides:       bundled(golang(golang.org/x/oauth2/clientcredentials)) = d2e6202438beef2727060aa7cabdd924d92ebfd9
Provides:       bundled(golang(golang.org/x/oauth2/google)) = d2e6202438beef2727060aa7cabdd924d92ebfd9
Provides:       bundled(golang(golang.org/x/oauth2/internal)) = d2e6202438beef2727060aa7cabdd924d92ebfd9
Provides:       bundled(golang(golang.org/x/oauth2/jws)) = d2e6202438beef2727060aa7cabdd924d92ebfd9
Provides:       bundled(golang(golang.org/x/oauth2/jwt)) = d2e6202438beef2727060aa7cabdd924d92ebfd9
Provides:       bundled(golang(golang.org/x/sys/unix)) = d99a578cf41bfccdeaf48b0845c823a4b8b0ad5e
Provides:       bundled(golang(golang.org/x/sys/windows)) = d99a578cf41bfccdeaf48b0845c823a4b8b0ad5e
Provides:       bundled(golang(golang.org/x/text/collate)) = 0.3.0
Provides:       bundled(golang(golang.org/x/text/collate/build)) = 0.3.0
Provides:       bundled(golang(golang.org/x/text/internal/colltab)) = 0.3.0
Provides:       bundled(golang(golang.org/x/text/internal/gen)) = 0.3.0
Provides:       bundled(golang(golang.org/x/text/internal/tag)) = 0.3.0
Provides:       bundled(golang(golang.org/x/text/internal/triegen)) = 0.3.0
Provides:       bundled(golang(golang.org/x/text/internal/ucd)) = 0.3.0
Provides:       bundled(golang(golang.org/x/text/language)) = 0.3.0
Provides:       bundled(golang(golang.org/x/text/secure/bidirule)) = 0.3.0
Provides:       bundled(golang(golang.org/x/text/transform)) = 0.3.0
Provides:       bundled(golang(golang.org/x/text/unicode/bidi)) = 0.3.0
Provides:       bundled(golang(golang.org/x/text/unicode/cldr)) = 0.3.0
Provides:       bundled(golang(golang.org/x/text/unicode/norm)) = 0.3.0
Provides:       bundled(golang(golang.org/x/text/unicode/rangetable)) = 0.3.0
Provides:       bundled(golang(golang.org/x/time/rate)) = fbb02b2291d28baffd63558aa44b4b56f178d650
Provides:       bundled(golang(google.golang.org/api/dns/v1)) = 087779f1d2c96357d4c45bd04c4d10d7b5f22736
Provides:       bundled(golang(google.golang.org/api/gensupport)) = 087779f1d2c96357d4c45bd04c4d10d7b5f22736
Provides:       bundled(golang(google.golang.org/api/googleapi)) = 087779f1d2c96357d4c45bd04c4d10d7b5f22736
Provides:       bundled(golang(google.golang.org/api/googleapi/internal/uritemplates)) = 087779f1d2c96357d4c45bd04c4d10d7b5f22736
Provides:       bundled(golang(google.golang.org/appengine)) = 1.1.0
Provides:       bundled(golang(google.golang.org/appengine/internal)) = 1.1.0
Provides:       bundled(golang(google.golang.org/appengine/internal/app_identity)) = 1.1.0
Provides:       bundled(golang(google.golang.org/appengine/internal/base)) = 1.1.0
Provides:       bundled(golang(google.golang.org/appengine/internal/datastore)) = 1.1.0
Provides:       bundled(golang(google.golang.org/appengine/internal/log)) = 1.1.0
Provides:       bundled(golang(google.golang.org/appengine/internal/modules)) = 1.1.0
Provides:       bundled(golang(google.golang.org/appengine/internal/remote_api)) = 1.1.0
Provides:       bundled(golang(google.golang.org/appengine/internal/urlfetch)) = 1.1.0
Provides:       bundled(golang(google.golang.org/appengine/urlfetch)) = 1.1.0
Provides:       bundled(golang(gopkg.in/ini.v1)) = 1.38.2
Provides:       bundled(golang(gopkg.in/ns1/ns1-go.v2/rest)) = 028658c6d9be774b6d103a923d8c4b2715135c3f
Provides:       bundled(golang(gopkg.in/ns1/ns1-go.v2/rest/model/account)) = 028658c6d9be774b6d103a923d8c4b2715135c3f
Provides:       bundled(golang(gopkg.in/ns1/ns1-go.v2/rest/model/data)) = 028658c6d9be774b6d103a923d8c4b2715135c3f
Provides:       bundled(golang(gopkg.in/ns1/ns1-go.v2/rest/model/dns)) = 028658c6d9be774b6d103a923d8c4b2715135c3f
Provides:       bundled(golang(gopkg.in/ns1/ns1-go.v2/rest/model/filter)) = 028658c6d9be774b6d103a923d8c4b2715135c3f
Provides:       bundled(golang(gopkg.in/ns1/ns1-go.v2/rest/model/monitor)) = 028658c6d9be774b6d103a923d8c4b2715135c3f
Provides:       bundled(golang(gopkg.in/square/go-jose.v2)) = 2.1.9
Provides:       bundled(golang(gopkg.in/square/go-jose.v2/cipher)) = 2.1.9
Provides:       bundled(golang(gopkg.in/square/go-jose.v2/json)) = 2.1.9


%description
Caddy is the HTTP/2 web server with automatic HTTPS.  Official Caddy builds
with customized plugins can be downloaded from https://caddyserver.com.  This
package is an unofficial build with the following plugins:

%{?with_geoip:  http.geoip
}%{?with_realip:  http.realip
}%{?with_azure:  tls.dns.azure
}%{?with_cloudflare:  tls.dns.cloudflare
}%{?with_digitalocean:  tls.dns.digitalocean
}%{?with_dyn:  tls.dns.dyn
}%{?with_gandi:  tls.dns.gandi
}%{?with_googlecloud:  tls.dns.googlecloud
}%{?with_namecheap:  tls.dns.namecheap
}%{?with_pdns:  tls.dns.powerdns
}%{?with_rackspace:  tls.dns.rackspace
}%{?with_rfc2136:  tls.dns.rfc2136
}%{?with_route53:  tls.dns.route53
}


%prep
%setup -q -c -a 10 -a 11 -a 20 -a 21

cp caddy-%{version}/LICENSE.txt LICENSE.txt
cp caddy-%{version}/dist/README.txt README.txt
mkdir -p $(dirname _build/src/%{import_path})
mv caddy-%{version} _build/src/%{import_path}

%if %{with dnsproviders}
cp dnsproviders-%{version_dnsproviders}/LICENSE LICENSE-dnsproviders
mkdir -p $(dirname _build/src/%{import_path_dnsproviders})
mv dnsproviders-%{version_dnsproviders} _build/src/%{import_path_dnsproviders}
cp lego-%{version_lego}/LICENSE LICENSE-lego
mkdir -p $(dirname _build/src/%{import_path_lego})
mv lego-%{version_lego} _build/src/%{import_path_lego}
%endif

%if %{with geoip}
cp caddy-geoip-%{commit_geoip}/LICENSE LICENSE-geoip
mkdir -p $(dirname _build/src/%{import_path_geoip})
mv caddy-geoip-%{commit_geoip} _build/src/%{import_path_geoip}
%endif

%if %{with realip}
cp caddy-realip-%{commit_realip}/LICENSE LICENSE-realip
mkdir -p $(dirname _build/src/%{import_path_realip})
mv caddy-realip-%{commit_realip} _build/src/%{import_path_realip}
%endif

sed -e '/other plugins/ a \\t// plugins added during rpmbuild' \
%{?with_geoip:          -e '/other plugins/ a \\t_ "%{import_path_geoip}"'} \
%{?with_realip:         -e '/other plugins/ a \\t_ "%{import_path_realip}"'} \
%{?with_azure:          -e '/other plugins/ a \\t_ "%{import_path_dnsproviders}/azure"'} \
%{?with_cloudflare:     -e '/other plugins/ a \\t_ "%{import_path_dnsproviders}/cloudflare"'} \
%{?with_digitalocean:   -e '/other plugins/ a \\t_ "%{import_path_dnsproviders}/digitalocean"'} \
%{?with_dyn:            -e '/other plugins/ a \\t_ "%{import_path_dnsproviders}/dyn"'} \
%{?with_gandi:          -e '/other plugins/ a \\t_ "%{import_path_dnsproviders}/gandi"'} \
%{?with_googlecloud:    -e '/other plugins/ a \\t_ "%{import_path_dnsproviders}/googlecloud"'} \
%{?with_namecheap:      -e '/other plugins/ a \\t_ "%{import_path_dnsproviders}/namecheap"'} \
%{?with_pdns:           -e '/other plugins/ a \\t_ "%{import_path_dnsproviders}/pdns"'} \
%{?with_rackspace:      -e '/other plugins/ a \\t_ "%{import_path_dnsproviders}/rackspace"'} \
%{?with_rfc2136:        -e '/other plugins/ a \\t_ "%{import_path_dnsproviders}/rfc2136"'} \
%{?with_route53:        -e '/other plugins/ a \\t_ "%{import_path_dnsproviders}/route53"'} \
                        -i _build/src/%{import_path}/caddy/caddymain/run.go


%build
export GOPATH="$PWD/_build:%{gopath}"
export LDFLAGS="${LDFLAGS:-} -X %{import_path}/caddy/caddymain.appVersion=%{version}"
%gobuild -o _bin/caddy %{import_path}/caddy


%install
install -D -m 0755 _bin/caddy %{buildroot}%{_bindir}/caddy
install -D -m 0644 %{S:1} %{buildroot}%{_sysconfdir}/caddy/caddy.conf
install -D -m 0644 %{S:2} %{buildroot}%{_unitdir}/caddy.service
%if %{defined rhel}
sed -e '/ProtectSystem/ s/strict/full/' -i %{buildroot}%{_unitdir}/caddy.service
%endif
install -D -m 0644 %{S:3} %{buildroot}%{_datadir}/caddy/index.html
install -d -m 0755 %{buildroot}%{_sysconfdir}/caddy/conf.d
install -d -m 0750 %{buildroot}%{_sharedstatedir}/caddy


%pre
getent group caddy &> /dev/null || \
groupadd -r caddy &> /dev/null
getent passwd caddy &> /dev/null || \
useradd -r -g caddy -d %{_sharedstatedir}/caddy -s /sbin/nologin -c 'Caddy web server' caddy &> /dev/null
exit 0


%post
%systemd_post caddy.service

if [ -x /usr/sbin/getsebool ]; then
    # connect to ACME endpoint to request certificates
    setsebool -P httpd_can_network_connect on
fi
if [ -x /usr/sbin/semanage -a -x /usr/sbin/restorecon ]; then
    # file contexts
    semanage fcontext --add --type httpd_exec_t        '%{_bindir}/caddy'               2> /dev/null || :
    semanage fcontext --add --type httpd_sys_content_t '%{_datadir}/caddy(/.*)?'        2> /dev/null || :
    semanage fcontext --add --type httpd_config_t      '%{_sysconfdir}/caddy(/.*)?'     2> /dev/null || :
    semanage fcontext --add --type httpd_var_lib_t     '%{_sharedstatedir}/caddy(/.*)?' 2> /dev/null || :
    restorecon -r %{_bindir}/caddy %{_datadir}/caddy %{_sysconfdir}/caddy %{_sharedstatedir}/caddy || :
fi
if [ -x /usr/sbin/semanage ]; then
    # QUIC
    semanage port --add --type http_port_t --proto udp 80   2> /dev/null || :
    semanage port --add --type http_port_t --proto udp 443  2> /dev/null || :
    # HTTP challenge alternate port
    semanage port --add --type http_port_t --proto tcp 5033 2> /dev/null || :
fi


%preun
%systemd_preun caddy.service


%postun
%systemd_postun_with_restart caddy.service

if [ $1 -eq 0 ]; then
    if [ -x /usr/sbin/getsebool ]; then
        # connect to ACME endpoint to request certificates
        setsebool -P httpd_can_network_connect off
    fi
    if [ -x /usr/sbin/semanage ]; then
        # file contexts
        semanage fcontext --delete --type httpd_exec_t        '%{_bindir}/caddy'               2> /dev/null || :
        semanage fcontext --delete --type httpd_sys_content_t '%{_datadir}/caddy(/.*)?'        2> /dev/null || :
        semanage fcontext --delete --type httpd_config_t      '%{_sysconfdir}/caddy(/.*)?'     2> /dev/null || :
        semanage fcontext --delete --type httpd_var_lib_t     '%{_sharedstatedir}/caddy(/.*)?' 2> /dev/null || :
        # QUIC
        semanage port     --delete --type http_port_t --proto udp 80   2> /dev/null || :
        semanage port     --delete --type http_port_t --proto udp 443  2> /dev/null || :
        # HTTP challenge alternate port
        semanage port     --delete --type http_port_t --proto tcp 5033 2> /dev/null || :
    fi
fi


%files
%license LICENSE.txt
%{?with_geoip:%license LICENSE-geoip}
%{?with_realip:%license LICENSE-realip}
%{?with_dnsproviders:%license LICENSE-dnsproviders}
%{?with_dnsproviders:%license LICENSE-lego}
%doc README.txt
%{_bindir}/caddy
%{_datadir}/caddy
%{_unitdir}/caddy.service
%dir %{_sysconfdir}/caddy
%dir %{_sysconfdir}/caddy/conf.d
%config(noreplace) %{_sysconfdir}/caddy/caddy.conf
%attr(0750,caddy,caddy) %dir %{_sharedstatedir}/caddy


%changelog
* Wed Mar 06 2019 Carl George <carl@george.computer> - 0.11.4-1
- Latest upstream
- Update bundled dnsproviders to 0.1.3
- Update bundled lego to 2.2.0
- Enable googlecloud, route53, and azure dns providers on epel7
- Allow custom http port with default config file rhbz#1685446

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 14 2018 Carl George <carl@george.computer> - 0.11.1-2
- Buildrequires at least golang 1.10

* Tue Nov 13 2018 Carl George <carl@george.computer> - 0.11.1-1
- Latest upstream
- Update bundled geoip

* Fri Oct 19 2018 Carl George <carl@george.computer> - 0.11.0-3
- Enable httpd_can_network_connect selinux boolean to connect to ACME endpoint rhbz#1641158
- Define UDP 80/443 as selinux http_port_t for QUIC rhbz#1608548
- Define TCP 5033 as selinux http_port_t for HTTP challenge rhbz#1641160

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat May 12 2018 Carl George <carl@george.computer> - 0.11.0-1
- Latest upstream

* Sat Apr 21 2018 Carl George <carl@george.computer> - 0.10.14-1
- Latest upstream
- Overhaul %%prep to extract everything with %%setup
- Edit lego providers to require acmev2 instead of acme
- Add provides for specific providers from %%import_path_dnsproviders and %%import_path_lego
- Add azure dns provider on f28+

* Fri Apr 20 2018 Carl George <carl@george.computer> - 0.10.11-6
- Enable geoip plugin on EL7
- Only provide bundled geoip/realip/dnsproviders/lego when the respective plugin is enabled

* Wed Apr 18 2018 Carl George <carl@george.computer> - 0.10.11-5
- Add geoip plugin

* Tue Apr 17 2018 Carl George <carl@george.computer> - 0.10.11-4
- Correct ExclusiveArch fallback

* Mon Apr 16 2018 Carl George <carl@george.computer> - 0.10.11-3
- Enable s390x
- Disable googlecloud and route53 dns providers on EL7 due to dependency issues

* Fri Mar 30 2018 Carl George <carl@george.computer> - 0.10.11-2
- Add googlecloud dns provider
- Add route53 dns provider
- Set minimum golang version to 1.9
- Set selinux labels in scriptlets

* Sat Feb 24 2018 Carl George <carl@george.computer> - 0.10.11-1
- Latest upstream

* Sat Feb 24 2018 Carl George <carl@george.computer> - 0.10.10-4
- Change ProtectSystem from strict to full in unit file on RHEL

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Carl George <carl@george.computer> - 0.10.10-2
- Add powerdns provider

* Mon Oct 09 2017 Carl George <carl@george.computer> - 0.10.10-1
- Latest upstream

* Mon Oct 02 2017 Carl George <carl@george.computer> - 0.10.9-6
- Add provides for bundled libraries

* Mon Oct 02 2017 Carl George <carl@george.computer> - 0.10.9-5
- Enable rfc2136 dns provider
- List plugins in description

* Mon Sep 18 2017 Carl George <carl@george.computer> - 0.10.9-4
- Exclude s390x

* Sun Sep 17 2017 Carl George <carl@george.computer> - 0.10.9-3
- Add realip plugin
- Add conditionals for plugins

* Sat Sep 16 2017 Carl George <carl@george.computer> - 0.10.9-2
- Add sources for caddyserver/dnsproviders and xenolf/lego
- Disable all dns providers that require additional libraries (dnsimple, dnspod, googlecloud, linode, ovh, route53, vultr)
- Rewrite default index.html

* Tue Sep 12 2017 Carl George <carl@george.computer> - 0.10.9-1
- Latest upstream
- Add config validation to unit file
- Disable exoscale dns provider https://github.com/xenolf/lego/issues/429

* Fri Sep 08 2017 Carl George <carl@george.computer> - 0.10.8-1
- Latest upstream
- Build with %%gobuild macro
- Move config subdirectory from /etc/caddy/caddy.conf.d to /etc/caddy/conf.d

* Tue Aug 29 2017 Carl George <carl@george.computer> - 0.10.7-1
- Latest upstream

* Fri Aug 25 2017 Carl George <carl@george.computer> - 0.10.6-2
- Use SIQQUIT to stop service
- Increase the process limit from 64 to 512
- Only `go get` in caddy/caddymain

* Fri Aug 11 2017 Carl George <carl@george.computer> - 0.10.6-1
- Latest upstream
- Add webserver virtual provides
- Drop tmpfiles and just own /var/lib/caddy directly
- Remove PrivateDevices setting from unit file, it prevents selinux process transitions
- Disable rfc2136 dns provider https://github.com/caddyserver/dnsproviders/issues/11

* Sat Jun 03 2017 Carl George <carl.george@rackspace.com> - 0.10.3-2
- Rename Envfile to envfile
- Rename Caddyfile to caddy.conf
- Include additional configs from caddy.conf.d directory

* Fri May 19 2017 Carl George <carl.george@rackspace.com> - 0.10.3-1
- Latest upstream

* Mon May 15 2017 Carl George <carl.george@rackspace.com> - 0.10.2-1
- Initial package
