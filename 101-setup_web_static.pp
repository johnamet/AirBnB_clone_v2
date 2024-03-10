# Install Nginx package if not already installed
package { 'nginx':
  ensure => installed,
}

# Define necessary directories
$dirs = ['/data/', '/data/web_static', '/data/web_static/releases/', '/data/web_static/shared',
  '/data/web_static/releases/test/']

# Create directories if they don't exist
$dirs.each |$dir| {
  file { $dir:
    ensure => directory,
    owner  => 'ubuntu',
    group  => 'ubuntu',
    mode   => '0755',
  }
}

# Create a fake HTML file with updated content
file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
}

# Update Nginx configuration
file_line { 'hbnb_static_config':
  ensure  => present,
  path    => '/etc/nginx/sites-available/default',
  line    => 'location /hbnb_static/ { alias /data/web_static/current/; }',
  match   => '^(\s*server_name\s+\w+;$)',
  before  => '}',
  require => Package['nginx'],
}

# Reload Nginx service after updating configuration
service { 'nginx':
  ensure  => running,
  enable  => true,
  require => File_line['hbnb_static_config'],
}

# File: site.pp (or any other Puppet manifest file)

# Install Nginx package
package { 'nginx':
  ensure => installed,
}

# Create necessary directories
$dirs = [
  '/data/',
  '/data/web_static',
  '/data/web_static/releases/',
  '/data/web_static/shared',
  '/data/web_static/releases/test/',
]

file { $dirs:
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Create a fake HTML file with updated content
file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
}


# Create symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  force  => true,
}

# Configure Nginx to serve hbnb_static
file { '/etc/nginx/sites-available/default':
  content => template('my_module/nginx_config.erb'),
}

# Enable the configuration
file { '/etc/nginx/sites-enabled/default':
  ensure => link,
  target => '/etc/nginx/sites-available/default',
}

# Test Nginx configuration
exec { 'nginx-config-test':
  command => 'nginx -t',
  path    => '/usr/sbin:/usr/bin:/sbin:/bin',
  onlyif  => 'nginx -t',
}

# Reload Nginx if configuration test passes
service { 'nginx':
  ensure  => running,
  enable  => true,
  require => Exec['nginx-config-test'],
}
