# Docker

If you want to save all that issues with setting it up on your own, you can
use the Docker container

   docker run --mount type=bind,source=/path/to/examples/config/sfw.yaml,target=/app/config.yml noqqe/nichtparasoup:latest

or Docker Compose

```yaml
services:
  nichtparasoup:
    image: noqqe/nichtparasoup:latest
    ports:
      - '80:5000'
    volumes:
      - './examples/config/sfw.yaml:/app/config.yml'
```

or NixOS Container

```nix
{ config, pkgs, ... }:

{
  virtualisation.podman.enable = true;
  virtualisation.podman.dockerCompat = true;
  virtualisation.oci-containers = {
    backend = "podman";
    containers = {
      nichtparasoup = {
        image = "noqqe/nichtparasoup:0.0.2";
        volumes = [
          "/data/nichtparasoup/sfw.yml:/app/config.yml"
        ];
        ports = [ "5000:5000" ];
        extraOptions = [
          "--ip=10.88.10.18"
        ];
      };
    };
  };
};
```
