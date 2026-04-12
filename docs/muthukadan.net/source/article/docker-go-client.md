---
title: Docker Go Client
layout: single
permalink: /article/docker-go-client.html
---

Docker provides a [remote API](https://docs.docker.com/reference/api/docker_remote_api/)
and there are many language specific client libraries built on top of that.
The [dockerclient](https://github.com/samalba/dockerclient) is one of them.

The below example shows creating a container then stopping and finally
removing that.

```go
// Init the client
docker, _ := dockerclient.NewDockerClient("unix:///var/run/docker.sock", nil)

// Create a container
b := make(map[string][]dockerclient.PortBinding)
b["5432/tcp"] = []dockerclient.PortBinding{dockerclient.PortBinding{HostPort: "5432"}}
hostConfig := &dockerclient.HostConfig{
	PortBindings: b}
containerConfig := &dockerclient.ContainerConfig{
	Image:        "postgres:9.4",
	Tty:          false,
	ExposedPorts: map[string]struct{}{"5432/tcp": {}}}
containerId, err := docker.CreateContainer(containerConfig, "pg")
if err != nil {
	log.Fatal(err)
}

// Start the container
err = docker.StartContainer(containerId, hostConfig)
if err != nil {
	log.Fatal(err)
}

time.Sleep(7 * time.Second)

// Stop the container (with 5 seconds timeout)
docker.StopContainer(containerId, 5)

// Remove the container
docker.RemoveContainer(containerId, false, false)
```

