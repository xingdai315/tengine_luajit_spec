# Build tengine whith luajit spec file

***
Build tengine rpm with Luajit

## Requirements
***
### Platforms
 * CentOS 6.X
 * CentOS 7
 
### Rpmbuild directory
SOURCE      
	---logrotate  
	---nginx.conf  
	---ngx_cache_purge-2.1.tar.gz
	---tengine-2.1.1.tar.gz  
SPECS  
	---tengine.spec

### Installation
 * Install epel and atomic repo  
`wget -q -O - http://www.atomicorp.com/installers/atomic | sh`  
`rpm -ivh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm`  

 * Install dependency packages  
`yum -y install pcre mhash mhash-devel luajit libxslt-devel luajit-devel geoip geo-devel jemalloc jemalloc-devel`  

 * Install tengine  
 `rpmbuild -bb tengine.spec`  
 `yum -y install tengine-2.1.1-8.x86_64.rpm`  
 
### Usage

/etc/init.d/tengine start

### Test luajit
http://ipaddr/lua-version

