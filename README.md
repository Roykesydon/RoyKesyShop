# RoyKesyShop


## How To Create Your Own Bot

1. write config.yml

1. write .env
    
1. If you're not using docker with wsl2, you might need to change 
    ```
    upstream frontend{
        server host.docker.internal:8080;
    }

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

## Backend



### TODO
- 與資料庫的連線改成 connection pool 的形式



## Demo picture source
- unsplash.com