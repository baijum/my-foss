---
layout: single
title: Paketo Bindings for Spring Boot Applications
date: 2021-07-07
categories: kubernetes binding
---

[Service Binding Specification](https://github.com/k8s-service-bindings/spec)
for Kubernetes standardizes exposing backing service secrets to applications.
The application should be prepared to use the bindings projected into the
container.  This article explains how to use [Cloud Native
Buildpacks](https://buildpacks.io) and [Spring Cloud
Bindings](https://github.com/spring-cloud/spring-cloud-bindings) Java library to
prepare a _Spring Boot_ application to consume the bindings.


_Cloud Native Buildpacks_ transform your application source code into [OCI
images](https://github.com/opencontainers/image-spec/blob/master/spec.md) that
can run on any cloud.  The [Paketo Spring Boot
Buildpack](https://github.com/paketo-buildpacks/spring-boot) is a _Cloud Native
Buildpack_ that helps to contribute _Spring Cloud Bindings_ as an application
dependency.

The _Spring Cloud Bindings_ library enable automatic _Spring Boot_ configuration
based on the `org.springframework.cloud.bindings.boot.enable` system property.
The [Paketo
buildpacks](https://paketo.io/docs/reference/configuration/#bindings) sets this
property value to `true` if the bindings exists in the `/platform/bindings`
directory at build-time.  The name of the sub-directory is considered as the
name of the binding.  Within each directory, there should be a file named `type`
with the name of the type of binding.  You can see the list of supported types
in the [Spring Cloud Bindings
README](https://github.com/spring-cloud/spring-cloud-bindings#auto-configurations).

For example, if you want to build the [PetClinic REST
server](https://github.com/spring-petclinic/spring-petclinic-rest) sample
application with PostgreSQL backend, create a directory with a file named `type`
like this:

```
mkdir /tmp/postgres
echo "postgresql" > /tmp/postgres/type
```

Now you can build the application image like this:

```
git clone https://github.com/spring-petclinic/spring-petclinic-rest
cd spring-petclinic-rest
pack build --path . --builder paketobuildpacks/builder:base\
--volume /tmp/postgres:/platform/bindings/postgres spring-petclinic-rest
```

The Paketo Buildpacks will look for bindings in `$SERVICE_BINDING_ROOT` at
runtime.  If an implementation of [Service Binding
Specification](https://github.com/k8s-service-bindings/spec) for Kubernetes
project the bindings, your Spring Boot Application should connect to PostgreSQL
database.

When running the abive application, set the active spring profile through an
environment variable like this: `SPRING_PROFILES_ACTIVE=postgres,spring-data-jpa`

If you want to test the above application, create these files with valid values:

```
/tmp/postgres/
├── database
├── host
├── password
├── port
├── type
└── username
```

For testing the connectivity, you can run the container using docker:
```
docker run --env SERVICE_BINDING_ROOT=/bindings --env SPRING_PROFILES_ACTIVE=postgres,spring-data-jpa\
--volume /tmp/postgres:/bindings/postgres --rm -p 9966:9966 spring-petclinic-rest:latest
```
