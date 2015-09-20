## Intro
**What this guide covers**

* sample working config scripts
* how to setup a Scala collector
* how to setup a Kinesis to S3 Dump for Scala collector
* how to setup a EMR Enrichment process for any collector
* steps to obtain dependencies on a Linux platform

**Major Goals for the Upgrade**
1) Convert GET requests into POST to resolve long url issue
2) Address variable inundation
3) Streamlined Debugging Process

## Architecture Overview
![image](http://discourse.looker.com/uploads/default/original/2X/9/926790b0ec224820d3ce1e23d1147b3f0b074e69.png)

**Implementation Packages** 

| Step | Alternative | Script Status | Implemented | Config Source(s) | Description |
|------------|---------|---------|------------|---------|------------|
| Scala Collector | Clojure | Complete | No | [scala.config](https://gist.githubusercontent.com/segahm/86da99acbf2731e5715a/raw/670ab4b9bf454fcfe10feed73a47825a0c947cea/snowplow%2520scala%2520collector%2520config), [sample tracker javascript] (https://gist.github.com/segahm/a0b3a7db62f975c5f5a3) | Listens for events and dumps them  directly to Kinesis, avoiding bottleneck processing issues |
| Kinesis to S3 Dump | ... | Complete| No | [kinesis-s3.config](https://gist.githubusercontent.com/segahm/5f7eded472a1bf4eac95/raw/bbb84966e28ea2a3d53a6c6567c0311b150d3576/kinesis_to_emr) | One of the ways to fork Kinesis buffer |
| [S3 Enrichment + ETL to Redshift](https://github.com/snowplow/snowplow/wiki/Configure-Scala-Kinesis-Enrich) | [Kinesis Enrichment](https://github.com/snowplow/snowplow/wiki/Kinesis-Elasticsearch-Sink-Setup) | Working on It | No |[EmrEtlRunner.config](https://gist.githubusercontent.com/segahm/eb6a1443061877e772f1/raw/6874384981906d33050a19d7b4fe69cb47b5979f/EmrEtlRunner), [iglu_name_space_resolver.config](https://gist.githubusercontent.com/segahm/f0fda758af87ca3b8361/raw/772a42afb1bdbb3c342b1ef4c1f8822903f3170a/iglu_resolver), [iglu_schema.config](https://gist.githubusercontent.com/segahm/3d97558d29a0a7caa159/raw/e41f39ab9397a32a94d4e89d8ed17fd413e0649b/iglu_schema) | Same thing we were using with Cloudfront |
| Elastic Load Balancer | Cloudfront? | Not Started | No | ... | provides failover for the Scala (Clojure?) collector |
| Kinesis to DynamoDB | ... | Not Started | No | ... | Justa as Kinesis to S3 Dump, forks Kinesis Buffer |

## Prerequisites

* setup all the S3 buckets in [EmrEtlRunner.config] (https://gist.githubusercontent.com/segahm/eb6a1443061877e772f1/raw/6874384981906d33050a19d7b4fe69cb47b5979f/EmrEtlRunner) and change the S3 links accordingly
* Add new EC2 Key/Secret to YAML configs for both Scala and Kinesis to S3 processes
![image](https://cloud.githubusercontent.com/assets/1756903/9552904/5bdddf10-4d70-11e5-8179-252fb0e20d2b.png)
* Spin up at least a *medium* EC2 instance for EmrETLRunner
* Upload the [IGLU Schema] (https://gist.github.com/segahm/3d97558d29a0a7caa159) to S3 (this will be used to parse Looker-custom event attributes)
* Replace yum package installer with whatever is suitable for your *nix OS

## Scripts

**Scala Install**
```
#!/bin/bash
cd ~
git clone https://github.com/snowplow/snowplow.git
cd snowplow/2-collectors/scala-stream-collector/
# for Fedora distribution - for Ubuntu use apt-get
sudo yum install sbt
sbt assembly
mv target ../../../scala
cd ../../../scala
# change this to point to your version of the Scala config file
# https://github.com/snowplow/snowplow/wiki/Configure-the-Scala-Stream-Collector
wget https://gist.githubusercontent.com/segahm/86da99acbf2731e5715a/raw/670ab4b9bf454fcfe10feed73a47825a0c947cea/snowplow%2520scala%2520collector%2520config
mv snowplow%20scala%20collector%20config scala.config
nohup ./scala-2.10/snowplow-stream-collector-0.5.0 --config scala.config
# test the Collector
echo Pinging Scala Collector
curl http://localhost:8080/health
# Should get O.K.
# Test through the webpage
# try the following tracker: https://github.com/snowplow/snowplow/wiki/javascript-tracker-setup
# Open Segah's sample tracker as html in a webpage: https://gist.github.com/segahm/a0b3a7db62f975c5f5a3
```
**Kinesis to S3 Install**
```
cd ~
sudo yum install lzo-devel lzop
git clone https://github.com/snowplow/kinesis-s3.git
cd kinesis-s3/
sbt assembly
mv target ../kinesis-s3-build
cd ../kinesis-s3-build
wget https://gist.githubusercontent.com/segahm/5f7eded472a1bf4eac95/raw/bbb84966e28ea2a3d53a6c6567c0311b150d3576/kinesis_to_emr
mv kinesis_to_emr kinesis.config
nohup ./scala-2.10/snowplow-kinesis-s3-0.3.0 --config kinesis.config
```
**Enrichment/ETL Install**
(might be better to do this from an independent m1.medium EC2 instance)
```
aws configure
# specify your AWS Key and Secret
aws emr create-default-roles
cd ~
sudo yum install build-essential bison openssl libreadline5 \
    libreadline-dev curl git-core zlib1g zlib1g-dev libssl-dev \
    libxslt-dev libxml2-dev libpq-dev subversion autoconf 
curl -L https://get.rvm.io | bash -s stabl
rvm install 1.9.3 --default
source ~/.rvm/scripts/rvm
source ~/.profile
rvm use 1.9.3
rvm install jruby
rvm use jruby
# set & export AWS_SNOWPLOW_ACCESS_KEY, AWS_SNOWPLOW_SECRET_KEY, add them to your ~/.bashrc script
# export PATH=$PATH:$HOME/.rvm/scripts/rvm
cd snowplow/3-enrich/emr-etl-runner
gem install bundler
bundle install --deployment

wget https://gist.githubusercontent.com/segahm/eb6a1443061877e772f1/raw/6874384981906d33050a19d7b4fe69cb47b5979f/EmrEtlRunner
mv EmrEtlRunner config/EmrEtlRunner.config
wget https://gist.githubusercontent.com/segahm/f0fda758af87ca3b8361/raw/772a42afb1bdbb3c342b1ef4c1f8822903f3170a/iglu_resolver
mv iglu_resolver config/resolver.json
bundle exec bin/snowplow-emr-etl-runner --config config/EmrEtlRunner.config --resolver config/resolver.json
```


## Goals & Solutions
**Convert GET requests into POST to resolve long url issue**

As per #11403. Both Scala and Clojure collectors allow for POST requests. Failover is established with Scala using Elastic Load Balancer. Clojure runs as part of Elastic Beanstalk app.

**Address variable inundation**

We collect many types of events and even more attributes. In a non-EAV type schema, this means lots of columns. Creating a lot of columns in Redshift (very wide table) will make it in the long run: 1) expensive, 2) overwhelming to the analyst.

Solution: 
* continue collecting all of the events, but only ETL into Redshift the ones currently needed for Feature Usage and other modeled data. When a new columns is needed, re-run Snowplow's EMR enrichment with modified IGLU schema on the archived S3 files (entire data history). This can be done by moving archives to the raw input bucket or by specifying explicitly location with `--process-enrich LOCATION` flag.
* make the rest of the variables available in a NoSQL environment

**Streamlined Debugging Process**

Live NoSQL interface bypasses the delay in the ETL/Enrichment phase = fewer layers of separation from raw data.

## More on EMR Enrichment and Schema Design

![image](https://cloud.githubusercontent.com/assets/1756903/9549041/c3c0ac10-4d58-11e5-9b9c-0b1b5a6bf4da.png)

## More on DynamoDB Design (Future)
