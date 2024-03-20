# Script that configures Nginx servers with puppet

exec {'update':
  provider => shell,
  command  => 'sudo apt-get -y update',
} ->

exec {'install Nginx':
  provider => shell,
  command  => 'sudo apt-get -y install nginx',
} ->

file { '/data':
  ensure => 'directory',
} ->

file { '/data/web_static':
  ensure => 'directory',
} ->

file { '/data/web_static/releases':
  ensure => 'directory',
} ->

file { '/data/web_static/releases/test':
  ensure => 'directory',
} ->

file { '/data/web_static/shared':
  ensure => 'directory',
} ->

file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "Holberton School Puppet\n",
} ->

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
} ->

exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/',
}

file { '/var/www':
  ensure => 'directory'
} ->

file { '/var/www/html':
  ensure => 'directory'
} ->

file { '/var/www/html/index.html':
  ensure  => 'present',
  content => "Hello World!"
} ->

file { '/var/www/html/404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page"
} ->

exec {'add location block':
  onlyif   => 'test -f /etc/nginx/sites-available/default',
  provider => shell,
  command  => 'sudo sed -i \'41i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}\n\' /etc/nginx/sites-available/default',
} ->

exec {'restart Nginx':
  provider => shell,
  command  => 'sudo service nginx restart',
}