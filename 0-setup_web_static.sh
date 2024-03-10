#!/usr/bin/env bash
# Prepare servers to serve static pages

nginx='nginx'

#check if nginx is installed
if dpkg -s "$nginx" &> /dev/null;then
	echo "$nginx is already installed" 
else
	echo "$nginx is not installed. Installing..."
	sudo apt-get update
	sudo apt-get install -y "$nginx"
fi

# make a list of neccessary folders
dirs_=("/data/" "/data/web_static" "/data/web_static/releases/" "/data/web_static/shared" "/data/web_static/releases/test/")

# iterate through the dirs_ to check if each dir exists
for dir in "${dirs_[@]}";do
	if [ -d "$dir" ]
	then
		echo "$dir exists'"
	else
		echo "$dir does not exits: Creating..."
		mkdir "$dir"
	fi
done

# create a fake HTML file
touch /data/web_static/releases/test/index.html

# Create a symbolic link
source_path="/data/web_static/releases/test"
destination_path="/data/web_static/current"

# Remove existing symbolic link if it exists
if [ -L "$destination_path" ]
then
	echo "Removing existing symbolic"
	rm "$destination_path"
fi

# Create the new symbolic link
echo "Creating symbolic link: $destination_path -> $source_path"
ln -sfn "$source_path" "$destination_path"

# Grant ownership of data to ubuntu
sudo chown -R ubuntu:ubuntu /data/

# Create a new Nginx configuration file for serving hbnb_static
echo "server {
    listen 80;
    server_name nnoboa.tech;

    location /hbnb_static/ {
        alias /data/web_static/current/;
    }
}" | sudo tee /etc/nginx/sites-available/nnoboa_static

# Create a symbolic link to enable the configuration
sudo ln -s /etc/nginx/sites-available/nnoboa_static /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# If the configuration test is successful, reload Nginx to apply changes
if nginx -t; then
    sudo service nginx reload
    echo "Nginx configuration reloaded successfully."
else
    echo "Nginx configuration test failed. Please check the configuration file."
fi

