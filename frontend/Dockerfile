FROM node:14.18

# make the 'app' folder the current working directory
WORKDIR /app

# copy 'package.json' to install dependencies
COPY . .

# install dependencies
RUN npm install



# copy files and folders to the current working directory (i.e. 'app' folder)
# COPY . .

EXPOSE 8080

# build app for production with minification
RUN npm install -g http-server
RUN npm run build
CMD [ "http-server", "dist" ]