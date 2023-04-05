This tool automates the suggested verification steps in the [release helper guide](https://cwiki.apache.org/confluence/display/NIFI/How+to+help+verify+an+Apache+NiFi+release+candidate).

Current version uses maven 3.9.0 and Java 8 and requires Docker. If you want to change these defaults, you can do it in the Dockerfile. For now.

To start the verification process:
```
./start-build-env.sh <nifi_version> <sha256hash> <sha512hash>
```

eg.:
```
./start-build-env.sh 1.21.0 598bf8e90f871f4ca25709dd4ecf3da16c814c08c0d8b2c8744dbd34df34dea5 58c10976bc22fb5406d9d1d9b7ca7d90c2dbed99565d00f1172bb33b375e9e068da5003d9dbbd87d2b17626e4e310b999c8581718532934e855c2134be763f04
```

The script will create a directory next to `start-build-env.sh` with the following content:

- buildresult
  - assembly - content of the nifi-assembly directory
  - mvnversion - the output of mvn --version
  - testresult - surefire reports
