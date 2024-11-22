#!/bin/bash

sudo yum install -y java-1.8.0-openjdk-devel

sudo rpm --import https://bazel.build/bazel-release.pub.gpg

sudo yum update -y

sudo yum install -y bazel

bazel version
