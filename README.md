# recipes

```
docker run -itd\
    --name=recipes\
    -v `pwd`:/home/recipes\
    -w /home/recipes\
    --env-file .env\
    sptkl/cook:latest bash -c 'pip3 install -r requirements.txt; pip3 install -e .; bash'
```