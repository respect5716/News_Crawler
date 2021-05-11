# News Crawler



## Objectives

지정된 검색어로 뉴스 수집 후 Dropbox에 업로드하는 프로그램



## Execute

1. Clone repository

```
git clone https://github.com/respect5716/News_Crawler.git
cd News_Crawler
```



2. Make config file

```
vim config.json

{
	"TIME": "20:00",
	"DROPBOX_TOKEN": "{dropbox access token}",
	"QUERY": {
		"domain1": ["query1", "query2", "query3"],
		"domain2": ["query1", "query2", "query3"]
	}
}
```



3. Build and run docker image

```
sudo docker-compose up -d
```

