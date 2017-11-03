# build
docker build -t my-centos .

# run
docker run -i -t -d my-centos /bin/bash

# attach
docker attach ${container id}

# kill
docker kill ${container id} 
