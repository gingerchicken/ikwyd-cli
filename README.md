# ikwyd-cli

<div align="center">
    <img src="assets/ikwyd-icon.png" width="256px"/>
</div>

A simple CLI application wrapper for [I Know What You Download](https://iknowwhatyoudownload.com/), a site used to view torrents distributed from a given IP address.

## Installation
It is a small Python script, so to install it you should use pip via the following command:

```bash
pip3 install -r requirements.txt
```

## Usage
With the tool, you check a provided IP address or your own.
### Your own IP
You do not need to pass any arguments for finding out about your own IP address, for example you can just enter the following:

```bash
./cli.py
```

### Another IP
You can just pass an IP as the first argument, such as the following:

```bash
./cli.py 1.1.1.1