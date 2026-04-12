---
layout: single
title: An Introduction to Go Programming
date: 2014-11-28
categories: golang
---

[Go], also commonly referred to as **golang**, is a statically typed,
compiled, garbage-collected, concurrent general purpose programming
language.  Go is considered as an object oriented programming language
and it uses [object composition] instead of class inheritance.  Go was
initially developed at Google by [Robert Griesemer], [Rob Pike], and
[Ken Thompson].  Go was publicly released as a free/open source
software in November 2009 by Google.

[Go]: http://golang.org
[object composition]: http://en.wikipedia.org/wiki/Composition_over_inheritance
[Robert Griesemer]: http://en.wikipedia.org/wiki/Robert_Griesemer
[Rob Pike]: http://en.wikipedia.org/wiki/Rob_Pike
[Ken Thompson]: http://en.wikipedia.org/wiki/Ken_Thompson

There are two major compilers available, *gc* & *gccgo*.  The official
compiler is *gc* and *gccgo* is a front-end to [gcc].  Go supports
major operating systems including Windows, GNU/Linux, Mac OS X and
various flavors of BSDs.  Through *gccgo* it supports more platforms.
And cross compilation is easy in Go.

[gcc]: https://gcc.gnu.org

![mascot](https://www.dropbox.com/s/sp2rbf1mv1onzcm/golang-mascot.png?raw=1)

The syntax of Go is very similar to C programming language.  There are
around 25+ keywords in the languages which is smaller compared to C,
C++, Python etc.

Go compilation is very fast, few seconds would be enough to compile
large programs.  In Go, unused imports and variables raise error
during compile time.  A variable starting with capital letter is
considered as exported and so it can be used from other packages.

Now I will move on to the details of installation of Go compiler.
First you will see instruction for installing in GNU/Linux.
The next section explains installation in a Windows system.

Finally I will show running a hello world program.  This will help you
to verify your installation.

## Linux Installation

Go project provides binaries for major operating systems including
GNU/Linux.  You can find 32 bit and 64 bit binaries for GNU/Linux
here: [https://golang.org/dl/](https://golang.org/dl/)

The following commands will download and install Go compiler in a
64 bit GNU/Linux system:

{% highlight bash %}
cd $HOME
wget -c https://storage.googleapis.com/golang/go1.7.1.linux-amd64.tar.gz
tar zxvf go1.7.1.linux-amd64.tar.gz
mkdir $HOME/mygo
{% endhighlight %}

The first line ensure that current working directory is the home
directory for the user.  The `$HOME` environment variable contains the
path to the user's home directory.

The second line download the 64 bit binary for GNU/Linux.  The `wget`
is a command line download manager.

The third line extract the downloaded tar ball in to `go` directory
inside the home.

The last line creates a directory named `mygo` as the workspace.  This
directory can be used to place binaries, third party packages and your
own Go source code.

You also need to set few environment variables.  Open the
`$HOME/.bashrc` file in a text editor and enter these lines:

{% highlight bash %}
export GOROOT=$HOME/go
export PATH=$GOROOT/bin:$PATH

export GOPATH=$HOME/mygo
export PATH=$GOPATH/bin:$PATH
{% endhighlight %}

The first line set `GOROOT` environment variable pointing to
`$HOME/go`.  This is required for proper functioning of Go tools.  You
can avoid setting the `GOROOT` environment variable if you install Go
inside `/usr/local/go`.

The second line append the `$GOROOT/bin` to the `PATH` environment
variable.  This will help you to run `go`, `godoc` & `gofmt` commands
from command line.

The third line set the `GOPATH` environment variable pointing to
`$HOME/mygo`.  The GOPATH environment variable specifies the location
of your Go workspace.

The last line append `$GOPATH/bin` to the `PATH` environment variable.
This will help you to run any binaries installed.


## Windows Installation

There are separate installers (MSI files) available for 32 bit & 64
bit versions of Windows.  The 32 bit version MSI file will be named
like this: ``go1.x.y.windows-386.msi`` (Replace `x.y` with the current
version).  Similarly for 64 bit version, the MSI file will be named
like this: ``go1.x.y.windows-amd64.msi`` (Replace `x.y` with the current
version).

You can download the installers (MSI files) from here:
[https://golang.org/dl/](https://golang.org/dl/)

After downloading the installer file, you can open the MSI file by
double clicking on that file.  This should prompts few things about
the installation of the Go compiler.  The installer place the
Go related files in the ``C:\Go`` directory.

The installer also put the ``C:\Go\bin`` directory in the system
`PATH` environment variable.  You may need to restart any open command
prompts for the change to take effect.

You also need to create a directory to download third party packages
from github.com or similar sites.  The directory can be created at
``C:\mygo`` like this:

{% highlight batch %}
mkdir C:\mygo
{% endhighlight %}

After this you can set `GOPATH` environment variable to point to this
location.  Temporarily you can set it like this:

{% highlight batch %}
set GOPATH=C:\mygo
{% endhighlight %}

You can also append ``C:\mygo\bin`` into the `PATH` environment
variable.

If you do not know how to set environment variable, just do a Google
search for: "set windows environment variable".

The `GOROOT` environment variable is not required here as you have
installed the `Go` inside `C:\Go` folder.  If you have changed that
location during the installation, set the `GOROOT` pointing to the
location you selected.


## Running a program

This section helps you to verify your installation by running a hello
world program.

As you know Go is a compiled programming language.  However, there is
a command which does both compilation and running the program.  The
command line syntax to run the program is like this:

{% highlight bash %}
go run <program.go>
{% endhighlight %}

To run a hello world program, you can copy-paste the below code to
your favorite text editor and save it as ``hello.go``:

{% highlight go %}
package main

import "fmt"

func main() {
     fmt.Println("Hello, World!")
}
{% endhighlight %}

Once you saved the above source code into a file.  You can open your
command line program (*bash* or *cmd.exe*) and run the above program like
this:

{% highlight bash %}
go run hello.go
{% endhighlight %}

If you are able to see the output as `Hello, World!`, you have
successfully installed Go compiler.

## Building and Running Program

As you can see above, you can run the program using `go run hello.go`
command.  You can also build (compile) and run the binary like this in
GNU/Linux:

{% highlight bash %}
go build hello.go
./hello
{% endhighlight %}

The first command produce a binary and second comand is executing that
binary.  You can do the same thing in Windows like this:

{% highlight batch %}
go build hello.go
hello.exe
{% endhighlight %}

The `go build` command produce a binary file native to the operating
system and the architecture of the CPU (i386, x86_64 etc.)
