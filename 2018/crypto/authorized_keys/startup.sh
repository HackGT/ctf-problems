#!/bin/sh -e

mkdir /run/sshd

/usr/sbin/sshd -D
