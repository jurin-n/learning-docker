## build
docker build -t my-python-app .

## run
docker run -it --rm --name my-running-script -v "$PWD":/usr/src/myapp -w /usr/src/myapp my-python-app python your-daemon-or-script.py


