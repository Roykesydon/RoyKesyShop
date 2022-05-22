# RoyKesyShop
A project composed of nginx + vue + flask + mariadb, the project is for practice use.

## How To Create Your Own Bot

1. write config.yml

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
## How to Shut down
```
docker-compose down
```

## Demo Pictures
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


### TODO
- mariadb replication


## Demo picture source
- unsplash.com