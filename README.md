# Video-OCR-Search
Video OCR (Optical Ccharacter Recognition) and Search Sample

![Screenshot Video OCR Search](https://raw.githubusercontent.com/AzureMediaCognitiveDemos/Video-OCR-Search-Python/master/img/screenshot-video-ocr-demo.jpg)

Demo: [http://aka.ms/amcdemo_videoocr](http://aka.ms/amcdemo_videoocr)


## 1. Preparation

### 1-1. Configurations for Azure Services
You have to create the following Azure services accounts and configure the files for each service:

| Azure Services                | Config file    |
|-------------------------------|----------------|
| Azure Media Services          | ams.conf       |
| Azure Search                  | search.conf    |

### 1-2. Create Azure Search Index for OCR text search
There are 2 types of scritps for creating index schema: execute create_ocr_schema_ja.sh if OCR text is Japanese, and execute create_ocr_schema_en.sh if the text is English.
```
# run this if OCR text is Japanese
./create_ocr_schema_ja.sh
 
# run this if OCR text is English
./create_ocr_schema_en.sh
```

### 1-3. Setup Azure Media Processors Modules
Please install maven and git if not yet installed on your environment
```
# for Ubuntu,Debian
sudo apt-get install git
sudo apt-get install maven

# for CentOS,Fedora,Oracle Linux,Red Hat Enterprise Linux
sudo yum install git
sudo yum install maven
```

Also you need Java compiler, so please install JDK if not yet installed on your environment
```
# for Ubuntu,Debian
sudo apt-get install openjdk-7-jdk   (JDK7)
sudo apt-get install openjdk-8-jdk   (JDK8)

# for CentOS,Fedora,Oracle Linux,Red Hat Enterprise Linux
sudo yum install java-1.7.0-openjdk  (JDK7)
sudo yum install java-1.8.0-openjdk  (JDK8)
```

Finall Check out github repo and build the module in order to make it ready for batch execution
```
cd mediaprocessors
./setup.sh
```

## 2. Batch execution

### run-batch command Usages
```
usage: ./run-batch [WORKFLOW] [VIDEO_FILE] [BATCH_NAME] [BATCH_WORK_DIR]
This program generates webvtt file from your video leveraging Azure Media 
Services OCR Media processor and upload all dataset of extracted text 
and their appearing times into Azure search to make them searchable

WORKFLOW : ALL|OCR_MP|JSON2CC|SEARCH_UPLOAD
```

### Example1: Run all workflows
```
./run-batch ALL ../demo/azuresubs/video/TransferanAzuresubscriptionJP.mp4 azuresubs ../demo/azuresubs
```

### Example2: Run each workflow one by one

```
# (1) Extract text from Video by Azure Media Services OCR Media Processor
# AMS OCR Processor generates Json file output as a result
./run-batch OCR_MP ../demo/azuresubs/video/TransferanAzuresubscriptionJP.mp4 azuresubs ../demo/azuresubs

# (2) Parse the Json output obtained in (1) and generate Webvtt file for Closed Caption for the Video
./run-batch OCR_MP ../demo/azuresubs/video/TransferanAzuresubscriptionJP.mp4 azuresubs ../demo/azuresubs

# (3) Parse and extract text from the webvtt file obtained in (2) and upload them onto Azure Search
./run-batch OCR_MP ../demo/azuresubs/video/TransferanAzuresubscriptionJP.mp4 azuresubs ../demo/azuresubs
```

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/AzureMediaCognitiveDemos/Video-OCR-Search-Python.

