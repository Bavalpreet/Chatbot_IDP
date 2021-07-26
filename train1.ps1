
docker run --rm --volume ${pwd}:/app \
          --workdir /app rasa/rasa:2.6.0 \
         --domain domain-grp/ train --fixed-model-name rasa-model \
          --config config.yml