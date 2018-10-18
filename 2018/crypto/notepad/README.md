# Non-Spoilery Description

This is a simple SaaS Notepad application.
Find the flag.
During competition, competitors will interact only with the network service.
For evaulation, looking at the source or binary is cheating.

# Building The Flag

```bash
docker build --tag hackgt-cft-notepad .
```

# Running The Flag

```bash
docker run --rm --detach --publish 127.0.0.1:8000:8000/tcp --name hackgt-ctf-notepad hackgt-ctf-notepad
```

Then: <http://127.0.0.1:8000/>.

200
