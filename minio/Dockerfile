FROM minio/minio


# EXPOSE 9000

# RUN apk add bash
# RUN chmod a+x /tmp/*.sh

ENTRYPOINT ["/bin/sh"]

VOLUME ["/data"]

CMD ["-c", "minio server --address :9000 /data"]
