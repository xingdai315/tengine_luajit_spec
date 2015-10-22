%define _prefix         /srv/tengine
%define _user           www
%define _user_uid       600
%define _group          www
%define _group_gid      600
%define _sbin_path      /usr/sbin
 
%define name      tengine
%define summary   High performance web server tengine
%define version   2.1.1
%define release   8
%define license   BSD
%define group     System Environment/Daemons
%define source    tengine-%{version}.tar.gz
%define url       http://tengine.taobao.org/
%define vendor    AZSY Co,Ltd
%define packager  xingdai
%define tengine_conf %{_prefix}/conf
 
Name:      %{name}
Version:   %{version}
Release:   %{release}
Packager:  %{packager}
Vendor:    %{vendor}
License:   %{license}
Summary:   %{summary}
Group:     %{group}
Source:    %{source}
Source1:   logrotate
Source2:   nginx.conf
Source10: ngx_cache_purge-2.1.tar.gz
URL:       %{url}
Prefix:    %{_prefix}
Buildroot: %{buildroot}
 
BuildRequires:  pcre-devel
BuildRequires:  zlib-devel
BuildRequires:  mhash-devel
BuildRequires:  openssl-devel
BuildRequires:  libxml2-devel 
BuildRequires:  libxslt-devel 
BuildRequires:  gd-devel 
BuildRequires:  luajit-devel 
BuildRequires:  geoip-devel
BuildRequires:  jemalloc
 
Requires: pcre
Requires: zlib
Requires: mhash
Requires: openssl
Requires: libxml2
Requires: libxslt
Requires: gd
Requires: luajit
Requires: geoip
 
%description
tengine for visitbeijing
 
%prep
%setup -q -n tengine-%{version}
cd %{_builddir}/%{name}-%{version}
%{__tar} -xzf %{SOURCE10}
 
%build
./configure \
--prefix=%{_prefix} \
--user=%{_user} \
--group=%{_group} \
--with-pcre \
--pid-path=/var/run/tengine.pid \
--with-syslog \
--with-http_stub_status_module \
--with-http_realip_module \
--with-http_ssl_module \
--with-http_dav_module \
--with-http_gzip_static_module \
--with-http_upstream_check_module \
--with-http_geoip_module=shared \
--with-http_sub_module=shared \
--with-http_concat_module=shared \
--with-http_sysguard_module=shared \
--with-http_footer_filter_module=shared \
--with-http_rewrite_module=shared \
--with-http_memcached_module=shared \
--with-http_limit_conn_module=shared \
--with-http_limit_req_module=shared \
--with-http_upstream_ip_hash_module=shared \
--with-http_upstream_least_conn_module=shared \
--with-http_upstream_session_sticky_module=shared \
--with-http_lua_module=shared \
--with-luajit-inc=/usr/include/luajit-2.0 \
--with-luajit-lib=/usr/lib64 \
--with-jemalloc \
--add-module=%{_builddir}/%{name}-%{version}/ngx_cache_purge-2.1 \
 
make
 
%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
make dso_install DESTDIR=%{buildroot}
 
mkdir -p %{buildroot}/%{_initrddir}
(
cat <<'EOF'
#!/bin/bash
# tengine Startup script for the tengine HTTP Server
# this script create it by Luo Hui at 2008.11.11.
# if you find any errors on this scripts,please contact Luo Hui.
# and send mail to farmer.luo at gmail dot com.
#
# chkconfig: - 85 15
# description: tengine is a high-performance web and proxy server.
# processname: tengine
# tengine pidfile: /var/run/tengine.pid
# tengine config: /usr/local/tengine/conf/nginx.conf
 
 
nginxd=%{_prefix}/sbin/nginx
nginx_config=%{_prefix}/conf/nginx.conf
nginx_pid=/var/run/tengine.pid
 
RETVAL=0
prog="nginx"
 
# Source function library.
. /etc/rc.d/init.d/functions
 
# Source networking configuration.
. /etc/sysconfig/network
 
# Check that networking is up.
[ ${NETWORKING} = "no" ] && exit 0
 
[ -x $nginxd ] || exit 0
 
ulimit -HSn 65535
 
 
# Start tengine daemons functions.
nginx_start() {
 
        if [ -e $nginx_pid ];then
                echo "tengine already running...."
                exit 1
        fi
 
        if [ ! -d %{_prefix}/logs ];then
                mkdir -p %{_prefix}/logs
        fi
 
        if [ ! -d %{_prefix}/tmp ]; then
                mkdir -p %{_prefix}/tmp
        fi
 
        if [ -e $nginx_pid ];then
                echo "tengine already running...."
                exit 1
        fi
 
        echo -n $"Starting $prog: "
        daemon $nginxd -c ${nginx_config}
        RETVAL=$?
        echo
        [ $RETVAL = 0 ] && touch /var/lock/subsys/tengine
        return $RETVAL
 
}
 
 
# Stop tengine daemons functions.
nginx_stop() {
        echo -n $"Stopping $prog: "
        killproc $nginxd
        RETVAL=$?
        echo
        [ $RETVAL = 0 ] && rm -f /var/lock/subsys/tengine $nginx_pid
}
 
 
# reload tengine service functions.
nginx_reload() {
 
        echo -n $"Reloading $prog: "
        #kill -HUP `cat ${nginx_pid}`
        killproc $nginxd -HUP
        RETVAL=$?
        echo
 
}
 
# See how we were called.
case "$1" in
start)
        nginx_start
        ;;
 
stop)
        nginx_stop
        ;;
 
reload)
        nginx_reload
        ;;
 
restart)
        nginx_stop
        nginx_start
        ;;
 
status)
        status $prog
        RETVAL=$?
        ;;
*)
        echo $"Usage: tengine {start|stop|restart|reload|status|help}"
        exit 1
esac
 
exit $RETVAL
EOF
) >%{buildroot}/%{_initrddir}/tengine
 
chmod 755 %{buildroot}/%{_initrddir}/tengine
%{__install} -m 644 -p %{SOURCE2} %{buildroot}%{tengine_conf}
#install logrotate
%{__mkdir} -p %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name} 
 
%clean
rm -rf %{buildroot}
 
%pre
grep -q ^%{_group}: /etc/group || %{_sbin_path}/groupadd -g %{_group_gid} %{_group}
grep -q ^%{_user}: /etc/passwd || %{_sbin_path}/useradd -g %{_group} -u %{_user_uid} -d %{_prefix} -s /sbin/nologin -M %{_user}
 
%post
chkconfig --add tengine
chkconfig --level 345 tengine on
 
%preun
chkconfig --del tengine
 
%postun
if [ $1 = 0 ]; then
        userdel %{_user} > /dev/null 2>&1 || true
fi
 
%files
%defattr(-,root,root)
%dir %{_prefix}/
%attr(0755,%{_user},%{_group}) %dir %{_prefix}/logs
%dir %{_prefix}/modules
%dir %{_prefix}/sbin
%dir %{_prefix}/conf
%dir %{_prefix}/html
%{_prefix}/sbin/nginx
%{_prefix}/sbin/dso_tool
%{_prefix}/conf/module_stubs
%{_prefix}/conf/fastcgi.conf
%{_prefix}/conf/fastcgi_params.default
%{_prefix}/conf/win-utf
%{_prefix}/conf/koi-utf
%{_prefix}/conf/nginx.conf.default
%{_prefix}/conf/fastcgi.conf.default
%{_prefix}/conf/fastcgi_params
%{_prefix}/conf/koi-win
%{_prefix}/conf/mime.types
%{_prefix}/conf/nginx.conf
%{_prefix}/conf/mime.types.default
%{_prefix}/conf/scgi_params
%{_prefix}/conf/scgi_params.default
%{_prefix}/conf/uwsgi_params
%{_prefix}/conf/uwsgi_params.default
%{_prefix}/html/50x.html
%{_prefix}/html/index.html
%{_prefix}/modules/*
%{_initrddir}/tengine
 
%changelog
