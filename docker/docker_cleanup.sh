#!/bin/bash
# Docker Cleanup Reference Commands

# 🚫 Stop all running containers (only if any are running)
if [ "$(sudo docker ps -q)" ]; then
    echo "Stopping all running containers..."
    sudo docker stop $(sudo docker ps -q)
else
    echo "No running containers to stop."
fi

# 🧹 Remove all containers (only if any exist)
if [ "$(sudo docker ps -aq)" ]; then
    echo "Removing all containers..."
    sudo docker rm $(sudo docker ps -aq)
else
    echo "No containers to remove."
fi

# 🧼 Remove all images (only if any exist)
if [ "$(sudo docker images -q)" ]; then
    echo "Removing all Docker images..."
    sudo docker rmi $(sudo docker images -q)
else
    echo "No Docker images to remove."
fi

# 🔎 Optional: Remove all unused Docker volumes
echo "Removing all unused volumes..."
sudo docker volume prune -f

# 🧯 Optional: Remove all unused networks
echo "Removing all unused networks..."
sudo docker network prune -f

# 📦 Optional: System-wide prune (CAUTION: removes everything unused)
# echo "Running full system prune..."
# sudo docker system prune -a --volumes -f

