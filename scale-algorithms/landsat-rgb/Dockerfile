FROM landsat-base
MAINTAINER Eric Svendsen <eric.svendsen@appliedis.com>

RUN yum install -y ImageMagick libgeotiff

COPY landsat-rgb.sh ./
ENTRYPOINT ["./landsat-rgb.sh"]
