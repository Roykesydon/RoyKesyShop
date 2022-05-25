# RoyKesyShop
A project composed of nginx + vue + flask + mariadb, the project is for practice use.

## How To Execute

1. write ./backend/config.yml

1. write .env
    
1. If you're not using docker with wsl2, you might need to change 
    ```
    upstream backend{
        server host.docker.internal:5000;
    }
    ```
    in nginx_conf/conf.d/default.conf

2. ```bat
    docker-compose up -d
    ```

3. When starting for the first time or want to clear the database, please execute the following command
```
cd ./backend
pipenv install
pipenv run python init_database.py
```
## How to Shut down
```
docker-compose down
```

## Frontend Demo Pictures
### Home Page
![](./demo_pictures/home_light.png)
![](./demo_pictures/home_dark.png)

### Login/Register
![](./demo_pictures/user_1.png)
![](./demo_pictures/user_2.png)

### Shop Page
![](./demo_pictures/shop_1.png)
![](./demo_pictures/shop_2.png)

### Clothing Detail
![](./demo_pictures/shop_detail.png)
![](./demo_pictures/shop_detail_2.png)

### Cart
![](./demo_pictures/cart.png)
### Personal Order
![](./demo_pictures/personal_1.png)
![](./demo_pictures/personal_2.png)

### Admin Dashboard
![](./demo_pictures/dash_1.png)
![](./demo_pictures/dash_2.png)
![](./demo_pictures/dash_3_1.png)
![](./demo_pictures/dash_3_2.png)
![](./demo_pictures/dash_3_3.png)

## Backend
![](./demo_pictures/apidocs.png)
get more information in http://localhost:5000/apidocs/

## Port
port | service
-- | --
3310 | Adminer
5000 | backend
80 | nginx

### TODO
- Set appropriate http status code


## Demo picture source
- unsplash.com